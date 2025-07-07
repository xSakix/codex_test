import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi


class YouTubeTranscriptDownloader:
    """Download YouTube video transcripts given a video URL."""

    def __init__(self, url: str) -> None:
        self.url = url
        self.video_id = self._extract_video_id(url)
        if not self.video_id:
            raise ValueError(f"Cannot extract video id from URL: {url}")

    def _extract_video_id(self, url: str) -> str | None:
        """Return the YouTube video id from the given URL."""
        parsed = urlparse(url)

        # Check query parameter v first as it is the most common form.
        qs = parse_qs(parsed.query)
        if "v" in qs:
            return qs["v"][0]

        # Short youtu.be URLs - the path directly contains the id.
        if parsed.netloc.endswith("youtu.be"):
            return parsed.path.lstrip("/")

        # Look for patterns like /embed/{id}, /shorts/{id}, /v/{id}, /live/{id}
        match = re.search(r"/(?:embed|shorts|v|live)/([\w-]{11})", parsed.path)
        if match:
            return match.group(1)

        # Some mobile or channel links can embed the id in the last path segment
        # e.g. https://www.youtube.com/@channelname/VIDEO_ID
        segments = [s for s in parsed.path.split("/") if s]
        if segments:
            candidate = segments[-1]
            if re.fullmatch(r"[\w-]{11}", candidate):
                return candidate

        return None

    def download(self, output_dir: str | Path = ".") -> Path:
        """Download the transcript and save it to ``output_dir``.

        The resulting file will be named ``{video_id}.txt``.
        """
        transcript = YouTubeTranscriptApi.get_transcript(self.video_id)
        text = "\n".join(chunk["text"] for chunk in transcript)

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{self.video_id}.txt"
        output_path.write_text(text, encoding="utf-8")
        return output_path

