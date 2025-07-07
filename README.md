# codex_test

This project contains a simple utility for downloading YouTube video transcripts.

## Usage

```
from youtube_transcript_downloader import YouTubeTranscriptDownloader

downloader = YouTubeTranscriptDownloader("https://youtu.be/dQw4w9WgXcQ")
file_path = downloader.download()
print(f"Transcript saved to {file_path}")
```

The transcript will be saved as a text file named after the video id in the
current directory (or the directory passed to `download`).
