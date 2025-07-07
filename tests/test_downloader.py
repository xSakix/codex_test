import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from youtube_transcript_downloader import YouTubeTranscriptDownloader


@pytest.mark.parametrize(
    "url",
    [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "https://www.youtube.com/shorts/dQw4w9WgXcQ",
        "https://www.youtube.com/v/dQw4w9WgXcQ",
        "https://www.youtube.com/live/dQw4w9WgXcQ",
        "https://www.youtube.com/@rickastley/dQw4w9WgXcQ",
    ],
)
def test_extract_video_id(url):
    downloader = YouTubeTranscriptDownloader(url)
    assert downloader.video_id == "dQw4w9WgXcQ"


@pytest.mark.parametrize(
    "url,phrase",
    [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "Never gonna give you up"),
        ("https://www.youtube.com/watch?v=kJQP7kiw5Fk", "Despacito"),
        ("https://www.youtube.com/watch?v=1F2nZHM3nk0", "Papaoutai"),
    ],
)
def test_download_transcript_languages(url, phrase, tmp_path):
    downloader = YouTubeTranscriptDownloader(url)
    path = downloader.download(tmp_path)
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert phrase.lower() in content.lower()
