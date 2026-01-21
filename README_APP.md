# Speech to SRT Web App

Live web app for converting audio/video files to SRT subtitles using OpenAI Whisper.

## 🌐 Use the App

**Live App**: [Deploy this to get a URL]

## Features

- 🎙️ **Upload any audio/video file** (MP3, MP4, WAV, M4A, etc.)
- 🤖 **Powered by OpenAI Whisper** (SOTA transcription)
- 📝 **Download SRT subtitles**
- 🔒 **Secure** - Files processed in memory, not stored
- 🆓 **Free to use** - Bring your own API key

## How to Use

1. **Get an OpenAI API Key**
   - Go to https://platform.openai.com/api-keys
   - Create a new API key
   - Cost: ~$0.006 per minute of audio

2. **Upload Your File**
   - Supported: MP3, MP4, WAV, M4A, FLAC, OGG, WebM, and more
   - Max size: 25 MB

3. **Generate SRT**
   - Click "Generate SRT"
   - Wait for transcription (few minutes)
   - Download your subtitle file

4. **Use Your Subtitles**
   - VLC Player
   - YouTube
   - Video editors
   - Any video player

## Cost

- **16 min video**: ~$0.10
- **40 min video**: ~$0.24
- **2 hour video**: ~$0.72

No subscriptions. Pay only for what you use.

## Privacy

- Your API key is not stored
- Files are processed in memory
- Nothing is saved on the server
- Files are deleted immediately after processing

## Support

- **Issues**: Open an issue on GitHub
- **Questions**: Check the main README

## Deploy Your Own

See [DEPLOY.md](DEPLOY.md) for instructions to deploy your own instance on Streamlit Cloud (free).
