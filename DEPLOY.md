# Deploy to Streamlit Cloud

## Quick Deploy (5 minutes)

### 1. Push to GitHub

```bash
# Create repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/speech-to-srt.git
git branch -M main
git push -u origin main
```

### 2. Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Select your GitHub repo: `YOUR_USERNAME/speech-to-srt`
4. Main file path: `app.py`
5. Click "Deploy"

**Done!** Your app will be live at: `https://YOUR_USERNAME-speech-to-srt.streamlit.app`

## Alternative: Test Locally First

```bash
# Install streamlit
pip install streamlit openai

# Run locally
streamlit run app.py

# Opens at http://localhost:8501
```

## App Features

- ✅ Upload any audio/video file (up to 25MB)
- ✅ User provides their own OpenAI API key
- ✅ Generates SRT subtitles
- ✅ Download SRT file
- ✅ Preview before download
- ✅ No files stored on server
- ✅ Secure (files processed in memory)

## Usage

Users need:
1. OpenAI API key (get from https://platform.openai.com/api-keys)
2. Audio/video file to transcribe

Cost: ~$0.006 per minute of audio

## Public Access

Once deployed to Streamlit Cloud, **anyone in the world** can use your app by:
1. Going to your app URL
2. Entering their own API key
3. Uploading a file
4. Downloading the SRT

No authentication required. Completely free to host on Streamlit Cloud.
