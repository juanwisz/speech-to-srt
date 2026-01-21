import streamlit as st
import tempfile
import os
from pathlib import Path
from openai import OpenAI

st.set_page_config(
    page_title="Speech to SRT",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Speech to SRT Converter")
st.markdown("Convert any audio or video file to SRT subtitles using OpenAI Whisper")

# API Key input
api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    help="Get your API key from https://platform.openai.com/api-keys"
)

if not api_key:
    st.info("👆 Enter your OpenAI API key to get started")
    st.markdown("""
    ### How to use:
    1. Enter your OpenAI API key above
    2. Upload an audio or video file
    3. Click "Generate SRT"
    4. Download your subtitles

    **Cost**: ~$0.006 per minute of audio

    **Supported formats**: MP3, MP4, WAV, M4A, FLAC, OGG, WebM, and more
    """)
    st.stop()

# File upload
uploaded_file = st.file_uploader(
    "Upload audio or video file",
    type=["mp3", "mp4", "wav", "m4a", "flac", "ogg", "webm", "avi", "mov", "mkv"],
    help="Max file size: 25 MB"
)

# Model selection
model = st.selectbox(
    "Model",
    ["whisper-1", "gpt-4o-transcribe", "gpt-4o-mini-transcribe"],
    index=0,
    help="whisper-1 recommended for SRT with timestamps"
)

# Language (optional)
language = st.text_input(
    "Language code (optional)",
    placeholder="en, es, fr, etc.",
    help="Leave empty for auto-detection"
)

if uploaded_file:
    st.info(f"📁 **File**: {uploaded_file.name} ({uploaded_file.size / 1024 / 1024:.2f} MB)")

    if st.button("🚀 Generate SRT", type="primary", use_container_width=True):
        if uploaded_file.size > 25 * 1024 * 1024:
            st.error("❌ File too large. Maximum size is 25 MB.")
            st.stop()

        with st.spinner("Transcribing... This may take a few minutes."):
            try:
                # Save uploaded file to temp
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name

                # Transcribe
                client = OpenAI(api_key=api_key)

                with open(tmp_path, "rb") as audio_file:
                    if model == "whisper-1":
                        response = client.audio.transcriptions.create(
                            model=model,
                            file=audio_file,
                            response_format="verbose_json",
                            timestamp_granularities=["segment"],
                            language=language if language else None
                        )

                        # Generate SRT from segments
                        srt_content = ""
                        for i, segment in enumerate(response.segments, 1):
                            start = format_timestamp(segment.start)
                            end = format_timestamp(segment.end)
                            text = segment.text.strip()
                            srt_content += f"{i}\n{start} --> {end}\n{text}\n\n"

                    else:
                        # gpt-4o models with streaming
                        stream = client.audio.transcriptions.create(
                            model=model,
                            file=audio_file,
                            response_format="text",
                            stream=True,
                            language=language if language else None
                        )

                        full_text = ""
                        for event in stream:
                            if hasattr(event, 'text'):
                                full_text += event.text

                        # Create single segment
                        srt_content = f"1\n00:00:00,000 --> 00:00:00,000\n{full_text.strip()}\n\n"
                        st.warning("⚠️ GPT-4o models don't provide segment timestamps. Use whisper-1 for proper SRT.")

                # Clean up temp file
                os.unlink(tmp_path)

                # Show success
                st.success("✅ Transcription complete!")

                # Download button
                output_filename = Path(uploaded_file.name).stem + ".srt"
                st.download_button(
                    label="⬇️ Download SRT",
                    data=srt_content,
                    file_name=output_filename,
                    mime="text/plain",
                    use_container_width=True
                )

                # Preview
                with st.expander("Preview SRT"):
                    st.text(srt_content[:1000] + ("..." if len(srt_content) > 1000 else ""))

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                if "Incorrect API key" in str(e):
                    st.error("Invalid API key. Please check and try again.")
                elif "rate limit" in str(e).lower():
                    st.error("Rate limit exceeded. Please wait and try again.")

def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>Built with Streamlit • Powered by OpenAI Whisper</p>
    <p>Your files are processed securely and not stored</p>
</div>
""", unsafe_allow_html=True)
