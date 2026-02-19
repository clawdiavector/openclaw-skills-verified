#!/usr/bin/env python3
"""
Instagram Reel Summarizer
Downloads Instagram reel, extracts audio, transcribes, and summarizes.
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

WORKSPACE = os.environ.get("WORKSPACE", "/Users/fivefriday/.openclaw/workspace")

def run_command(cmd, check=True):
    """Run a shell command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{result.stderr}")
    return result.stdout.strip()

def download_reel(url, output_dir):
    """Download Instagram reel using yt-dlp."""
    print(f"📥 Downloading reel from {url}...")
    
    # yt-dlp command to download reel (use simple filename)
    os.chdir(output_dir)
    cmd = f"""
    yt-dlp \
        --format best \
        --output "reel.%(ext)s" \
        --write-info-json \
        {url}
    """
    run_command(cmd)
    
    # Find the downloaded files
    info_file = None
    video_file = None
    for f in Path(output_dir).iterdir():
        if f.suffix == ".info.json" or f.name.endswith(".info.json"):
            info_file = f
        elif f.suffix in [".mp4", ".webm"] and f.name.startswith("reel"):
            video_file = f
    
    return info_file, video_file

def extract_audio(video_file, audio_file):
    """Extract audio from video using ffmpeg."""
    print(f"🎵 Extracting audio...")
    cmd = f"ffmpeg -i '{video_file}' -vn -acodec pcm_s16le -ar 16000 -ac 1 '{audio_file}' -y"
    run_command(cmd)

def transcribe_audio(audio_file):
    """Transcribe audio using OpenAI Whisper."""
    print(f"🎤 Transcribing audio...")
    cmd = f"whisper '{audio_file}' --model medium --output_format txt"
    output = run_command(cmd)
    print(output)
    
    # Find the transcript file
    transcript_file = Path(audio_file).with_suffix(".txt")
    if transcript_file.exists():
        return transcript_file.read_text()
    return None

def get_reel_info(info_file):
    """Extract metadata from yt-dlp info.json."""
    data = json.loads(info_file.read_text())
    return {
        "id": data.get("id"),
        "title": data.get("title", ""),
        "uploader": data.get("uploader", "Unknown"),
        "upload_date": data.get("upload_date", ""),
        "view_count": data.get("view_count", 0),
        "like_count": data.get("like_count", 0),
        "caption": data.get("description", ""),
        "url": data.get("webpage_url", ""),
    }

def summarize_with_ai(transcript, reel_info):
    """Send transcript to AI for summarization."""
    print(f"🤖 Generating summary...")
    
    prompt = f"""
    Summarize this Instagram reel transcript. Provide:
    
    1. **Summary** (2-3 sentences)
    2. **Key Points** (bullet list)
    3. **Overall Assessment** (1-2 sentences)
    
    Reel Info:
    - Author: {reel_info.get('uploader', 'Unknown')}
    - Caption: {reel_info.get('caption', 'N/A')}
    
    Transcript:
    {transcript[:8000]}
    """
    
    # This would call the AI - for now return placeholder
    return "AI summarization would be called here."

def generate_markdown(reel_info, transcript, summary, output_file):
    """Generate markdown summary file."""
    content = f"""# Instagram Reel Summary

**Reel ID:** {reel_info['id']}  
**Author:** {reel_info['uploader']}  
**Date:** {reel_info['upload_date']}  
**Views:** {reel_info['view_count']:,} | **Likes:** {reel_info['like_count']:,}  
**URL:** {reel_info['url']}

---

## Caption

{reel_info['caption'] or '*No caption*'}

---

## Full Transcript

{transcript}

---

## AI Summary

{summary}

---

*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    output_file.write_text(content)
    print(f"💾 Saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Download and summarize Instagram reels")
    parser.add_argument("url", help="Instagram reel URL")
    parser.add_argument("--output", "-o", default=WORKSPACE, help="Output directory")
    args = parser.parse_args()
    
    reel_id = "reel_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(args.output) / "instagram_temp" / reel_id
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Step 1: Download
        info_file, video_file = download_reel(args.url, output_dir)
        
        # Step 2: Extract audio
        audio_file = output_dir / "audio.wav"
        extract_audio(video_file, audio_file)
        
        # Step 3: Transcribe
        transcript = transcribe_audio(audio_file)
        
        # Step 4: Get info
        reel_info = get_reel_info(info_file)
        
        # Step 5: Summarize (placeholder)
        summary = summarize_with_ai(transcript, reel_info)
        
        # Step 6: Save markdown
        output_file = Path(args.output) / f"instagram-{reel_info['id']}.md"
        generate_markdown(reel_info, transcript, summary, output_file)
        
        print(f"\n✅ Done! Summary saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
