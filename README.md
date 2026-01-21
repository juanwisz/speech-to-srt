# Speech-to-SRT Transcription Pipeline

Production-ready pipeline for generating high-quality SRT subtitles from any video or audio file.

## Features

- **SOTA Quality**: Uses OpenAI's latest transcription models
- **Three API Options**:
  - **whisper-1** (legacy): Good quality, supports SRT timestamps
  - **gpt-4o-mini-transcribe**: Better quality, faster/cheaper
  - **gpt-4o-transcribe**: Best quality (SOTA 2025)
- **Local Option**: Free Whisper large-v3 (open-source SOTA)
- **Universal**: Works with any video/audio source
- **Multi-speaker**: Handles conversations, interviews, meetings, podcasts

## Quick Start

### 1. Activate Environment

```bash
cd /Users/juanwisznia/speech-meeting-to-text
source .venv/bin/activate
```

### 2. Set API Key (One-Time)

API key is already in `.env` file. If you need to change it:

```bash
echo "OPENAI_API_KEY=your-key-here" > .env
```

### 3. Transcribe

**Best Quality (OpenAI API with whisper-1 for SRT):**
```bash
python transcribe.py --url "https://youtube.com/..." --api
```

**Free Local Option:**
```bash
python transcribe.py --url "https://youtube.com/..." --local --model large-v3
```

**From Local File:**
```bash
python transcribe.py --file "video.mp4" --api
```

## Model Comparison

### OpenAI API Models (2025)

| Model | Quality | Speed | SRT Support | Cost/min |
|-------|---------|-------|-------------|----------|
| `whisper-1` | ★★★★☆ | Fast | ✅ Full | $0.006 |
| `gpt-4o-mini-transcribe` | ★★★★★ | Faster | ⚠️ Limited | $0.006 |
| `gpt-4o-transcribe` | ★★★★★ | Fast | ⚠️ Limited | $0.006 |

**For SRT generation**: Use `whisper-1` (supports segment timestamps)

### Local Whisper Models

| Model | Quality | Speed | Cost |
|-------|---------|-------|------|
| `large-v3` | ★★★★★ | Slow | Free |
| `medium` | ★★★☆☆ | Medium | Free |
| `base` | ★★☆☆☆ | Fast | Free |

## Usage Examples

### API Mode (Recommended for Quality)

```bash
# Use whisper-1 (best for SRT with timestamps)
python transcribe.py --url "https://youtube.com/..." --api

# Specify model explicitly
python transcribe.py --file "video.mp4" --api --api-model whisper-1

# With language hint for better accuracy
python transcribe.py --file "video.mp4" --api --language en
```

### Local Mode (Free, Private)

```bash
# Best quality local model
python transcribe.py --file "video.mp4" --local --model large-v3

# Faster local model
python transcribe.py --file "video.mp4" --local --model medium

# Specify language
python transcribe.py --file "video.mp4" --local --model large-v3 --language en
```

## Tested Quality Comparison

Tested on 16-minute TED talk:

**Local base model:**
- Errors: "chatter up" (should be "chat her up")
- Mixed spelling conventions
- 78 segments

**API whisper-1:**
- ✅ Correct: "chat her up"
- ✅ Proper British spelling (speaker was British)
- ✅ 112 segments (finer granularity)
- ✅ Better overall accuracy

## Cost Analysis

| Duration | whisper-1 API | Local (Free) |
|----------|---------------|--------------|
| 16 min (tested) | ~$0.10 | $0 |
| 40 min | ~$0.24 | $0 |
| 2 hours | ~$0.72 | $0 |

**No subscriptions needed. Pay only for what you use.**

## Advanced Usage

### Custom Output Location

```bash
python transcribe.py --file "video.mp4" --api --output "subtitles/final.srt"
```

### Batch Processing

```bash
for video in videos/*.mp4; do
  python transcribe.py --file "$video" --api
done
```

### Using Different API Models

```bash
# Note: gpt-4o models have limited SRT timestamp support
python transcribe.py --file "video.mp4" --api --api-model gpt-4o-transcribe
```

## Configuration

API key is stored in `.env` file:

```bash
# .env
OPENAI_API_KEY=sk-...
```

The script automatically loads from `.env`. No need to pass `--openai-key` every time.

## File Formats Supported

**Video**: MP4, AVI, MKV, MOV, WebM, FLV, etc.
**Audio**: MP3, WAV, M4A, FLAC, OGG, etc.
**Sources**: YouTube, Vimeo, local files, direct URLs

## SRT Output Format

Standard SRT format compatible with all video players:

```
1
00:00:17,000 --> 00:00:21,000
Let me start first with a brief story.

2
00:00:22,000 --> 00:00:26,000
Before attending a dinner at my rowing club, I went into the bar.
```

## Using Generated SRT Files

- **VLC Player**: Subtitle → Add Subtitle File
- **YouTube**: Upload in Studio → Subtitles
- **Web Players**: `<track kind="subtitles" src="video.srt">`
- **Video Editors**: Import subtitle file

## Tips for Best Results

1. **Use API whisper-1** for best quality SRT with timestamps
2. **Specify language** when known (`--language en`)
3. **API is recommended** for production (~$0.006/min)
4. **Local large-v3** for unlimited free transcription
5. **Good audio quality** = better transcription

## Troubleshooting

**"OpenAI API key required"**
```bash
# Check .env file exists
cat .env

# Or set manually
export OPENAI_API_KEY="sk-..."
```

**Out of memory (local mode)**
```bash
# Use smaller model
python transcribe.py --file "video.mp4" --local --model medium
```

**First run slow (local mode)**
- Downloads 3GB model on first use (one-time, cached)

## What's Different from Other Solutions

- ✅ **No subscriptions** (pay per use or free)
- ✅ **Production quality** (same as professional services)
- ✅ **Universal source support** (YouTube, local, any URL)
- ✅ **Multi-speaker support** (automatic)
- ✅ **90+ languages**
- ✅ **Standard SRT output** (works everywhere)
- ✅ **Two modes**: API (fast/paid) or Local (slow/free)

The pipeline is production-ready and universal.
