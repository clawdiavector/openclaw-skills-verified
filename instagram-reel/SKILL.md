---
name: instagram-reel
description: Download Instagram reels, extract audio, transcribe with Whisper, and summarize using AI.
metadata: {"version":"1.0.0","author":"OpenClaw","license":"MIT"}
---

# Instagram Reel Summarizer

Download Instagram reels, extract audio, transcribe with Whisper, and generate a markdown summary.

## Usage

```bash
instagram_reel_summarize "https://www.instagram.com/reel/XXXXX/"
```

## What It Does

1. **Download** - Uses yt-dlp to download the Instagram reel
2. **Extract Audio** - Extracts audio track using ffmpeg
3. **Transcribe** - Uses OpenAI Whisper to transcribe audio to text
4. **Summarize** - Uses AI to generate a concise summary
5. **Save** - Writes summary to markdown file in workspace

## Requirements

- `yt-dlp` installed (brew install yt-dlp)
- `ffmpeg` installed (brew install ffmpeg)
- Whisper skill installed (for transcription)
- Working AI model for summarization

## Output

Creates `instagram-{reel_id}.md` in the workspace with:
- Reel metadata (author, caption, date)
- Full transcript
- AI-generated summary
- Key points and takeaways
