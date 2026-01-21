# Usage Examples

## Basic Examples

### 1. YouTube Video (Most Common)

```bash
source .venv/bin/activate
python transcribe.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --local
```

**Output:**
- `downloads/VideoTitle.mp3` - Downloaded audio
- `downloads/VideoTitle.srt` - Perfect SRT subtitles

### 2. Local Video File

```bash
source .venv/bin/activate
python transcribe.py --file "meeting.mp4" --local
```

**Output:**
- `meeting.srt` - Generated subtitles

### 3. Local Audio File

```bash
source .venv/bin/activate
python transcribe.py --file "podcast.mp3" --local
```

## Quality Options

### Maximum Quality (SOTA)

```bash
python transcribe.py --file "video.mp4" --local --model large-v3
```
- Best transcription quality
- Recommended for final production
- ~20-30 min for 40-min video

### Balanced Quality & Speed

```bash
python transcribe.py --file "video.mp4" --local --model medium
```
- Good quality
- Faster processing
- ~10-15 min for 40-min video

### Ultra-Fast (API)

```bash
export OPENAI_API_KEY="sk-..."
python transcribe.py --file "video.mp4" --api
```
- Same quality as large-v3
- ~2-5 min for 40-min video
- ~$0.24 for 40-min video

## Language-Specific

### English Content

```bash
python transcribe.py --url "https://youtube.com/..." --local --language en
```

Specifying language improves accuracy by 5-15%

### Spanish Content

```bash
python transcribe.py --file "video.mp4" --local --language es
```

### Auto-Detect Language

```bash
python transcribe.py --file "video.mp4" --local
```

Omit `--language` for automatic detection

## Custom Output Location

### Specify Output Directory

```bash
python transcribe.py --file "video.mp4" --local --output "subtitles/final.srt"
```

### Organize by Project

```bash
python transcribe.py --file "video.mp4" --local --output "projects/project-A/video.srt"
```

## Real-World Scenarios

### Podcast Interview (2 hours)

```bash
# Download from YouTube
python transcribe.py \
  --url "https://youtube.com/watch?v=..." \
  --local \
  --model large-v3 \
  --language en \
  --output "podcasts/episode-001.srt"
```

**Cost:** $0 (free)
**Time:** ~45-60 minutes
**Quality:** Excellent

### Business Meeting Recording

```bash
python transcribe.py \
  --file "zoom-meeting-2025-01-21.mp4" \
  --local \
  --model large-v3
```

**Output:** `zoom-meeting-2025-01-21.srt`

### Conference Talk (40 minutes)

```bash
python transcribe.py \
  --url "https://youtube.com/watch?v=..." \
  --api \
  --openai-key "sk-..."
```

**Cost:** ~$0.24
**Time:** ~2-5 minutes
**Quality:** Excellent

### Batch Processing Multiple Videos

```bash
#!/bin/bash
source .venv/bin/activate

for video in videos/*.mp4; do
  echo "Processing: $video"
  python transcribe.py --file "$video" --local --model large-v3
done
```

### Interview with Multiple Speakers

```bash
python transcribe.py \
  --file "interview.mp4" \
  --local \
  --model large-v3 \
  --language en
```

Whisper handles multi-speaker content automatically

## Advanced Usage

### Using OpenAI API with Environment Variable

```bash
# Set API key once
export OPENAI_API_KEY="sk-your-key-here"

# Use without --openai-key flag
python transcribe.py --file "video.mp4" --api
```

### Processing Long Videos (2+ hours)

```bash
# Recommended: Use API for speed
python transcribe.py --file "long-video.mp4" --api

# Or use local with smaller model for faster processing
python transcribe.py --file "long-video.mp4" --local --model medium
```

### Non-YouTube URLs

```bash
# Vimeo
python transcribe.py --url "https://vimeo.com/..." --local

# Direct video URL
python transcribe.py --url "https://example.com/video.mp4" --local

# Facebook, Instagram, etc (if yt-dlp supports it)
python transcribe.py --url "https://facebook.com/..." --local
```

## Performance Comparison

| Video Length | Model | Method | Time | Cost | Quality |
|--------------|-------|--------|------|------|---------|
| 40 min | large-v3 | Local | 20-30 min | $0 | ★★★★★ |
| 40 min | medium | Local | 10-15 min | $0 | ★★★☆☆ |
| 40 min | whisper-1 | API | 2-5 min | $0.24 | ★★★★★ |
| 2 hours | large-v3 | Local | 45-60 min | $0 | ★★★★★ |
| 2 hours | whisper-1 | API | 5-10 min | $0.72 | ★★★★★ |

## Supported Languages

Whisper supports 90+ languages:

**Common:**
- English (`en`)
- Spanish (`es`)
- French (`fr`)
- German (`de`)
- Italian (`it`)
- Portuguese (`pt`)
- Dutch (`nl`)
- Russian (`ru`)
- Chinese (`zh`)
- Japanese (`ja`)
- Korean (`ko`)

**Full list:** https://github.com/openai/whisper#available-models-and-languages

## Tips for Best Results

1. **Specify language when known** - Improves accuracy
2. **Use large-v3 for final transcripts** - Best quality
3. **Good audio quality = better transcription**
4. **API mode for time-sensitive projects**
5. **Local mode for privacy/unlimited use**
6. **First run downloads model** (one-time, ~3GB)

## Using Generated SRT Files

### VLC Media Player

1. Open video in VLC
2. Menu: Subtitle → Add Subtitle File
3. Select `.srt` file
4. Subtitles appear automatically

### Web Video Player

```html
<video controls>
  <source src="video.mp4" type="video/mp4">
  <track kind="subtitles" src="video.srt" srclang="en" label="English">
</video>
```

### Upload to YouTube

1. Go to YouTube Studio
2. Select video → Subtitles
3. Upload → File → Select `.srt` file
4. Done

### Video Editing Software

- **Premiere Pro**: File → Import → SRT file
- **Final Cut Pro**: Import as captions
- **DaVinci Resolve**: Timeline → Import Subtitle
