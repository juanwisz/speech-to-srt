# Quick Start Guide

## One-Command Transcription

### From YouTube URL
```bash
source .venv/bin/activate
python transcribe.py --url "YOUR_YOUTUBE_URL_HERE" --local
```

### From Local File
```bash
source .venv/bin/activate
python transcribe.py --file "your-video.mp4" --local
```

**That's it!** The script will:
1. Download the video (if URL)
2. Extract/use audio
3. Transcribe with Whisper large-v3 (SOTA quality)
4. Generate perfect .srt file

## Example Output

```
downloads/
  video-title.mp3          # Downloaded audio
  video-title.srt          # Generated subtitles ✓
```

## Quality Modes

### Maximum Quality (Recommended)
```bash
python transcribe.py --file "video.mp4" --local --model large-v3
```
- Best accuracy
- ~20-30 min for 40-min video
- Free

### Fast Mode
```bash
python transcribe.py --file "video.mp4" --local --model medium
```
- Good accuracy
- ~10-15 min for 40-min video
- Free

### Ultra-Fast Mode (API)
```bash
export OPENAI_API_KEY="sk-..."
python transcribe.py --file "video.mp4" --api
```
- Best accuracy
- ~2-5 min for 40-min video
- ~$0.24 for 40-min video

## Real-World Examples

### Podcast Interview
```bash
python transcribe.py --url "https://youtube.com/watch?v=..." --local --language en
```

### Business Meeting Recording
```bash
python transcribe.py --file "meeting-2025-01-21.mp4" --local --model large-v3
```

### Conference Talk
```bash
python transcribe.py --file "conference-keynote.mp4" --local
```

### Multi-Language Video
```bash
python transcribe.py --file "video.mp4" --local --language es
```

## Using the SRT File

The generated .srt file works with:
- **Video Players**: VLC, MPV, QuickTime
- **Web Platforms**: YouTube, Vimeo (upload as captions)
- **Video Editors**: Premiere Pro, Final Cut, DaVinci Resolve
- **Streaming**: Any HTML5 video player

## Tips

1. **First run**: Downloads 3GB model (one-time, cached)
2. **Specify language** for better accuracy: `--language en`
3. **Good audio** = better transcription
4. **API mode** if you need speed and willing to pay ~$0.006/min
