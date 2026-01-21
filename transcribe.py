#!/usr/bin/env python3
"""
High-quality speech-to-SRT transcription pipeline.
Supports both local Whisper (free) and OpenAI API (pay-per-use).
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

import whisper
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def download_video(url: str, output_dir: str = "downloads") -> str:
    """Download video using yt-dlp and return the audio file path."""
    import subprocess

    os.makedirs(output_dir, exist_ok=True)
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    print(f"Downloading video from: {url}")

    # Download as audio only (best quality)
    cmd = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",  # best quality
        "-o", output_template,
        url
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error downloading video: {result.stderr}")
        sys.exit(1)

    # Find the downloaded file
    for line in result.stdout.split('\n'):
        if "Destination:" in line or "has already been downloaded" in line:
            # Extract filename from yt-dlp output
            pass

    # Get the most recent mp3 file in downloads
    files = list(Path(output_dir).glob("*.mp3"))
    if not files:
        print("Error: No audio file found after download")
        sys.exit(1)

    audio_file = max(files, key=lambda p: p.stat().st_mtime)
    print(f"Downloaded audio: {audio_file}")
    return str(audio_file)


def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"


def transcribe_with_local_whisper(
    audio_file: str,
    model_size: str = "large-v3",
    language: Optional[str] = None
) -> list:
    """
    Transcribe audio using local Whisper model.

    Args:
        audio_file: Path to audio file
        model_size: Whisper model size (tiny, base, small, medium, large, large-v2, large-v3)
                   large-v3 is SOTA for quality
        language: Language code (e.g., 'en', 'es'). Auto-detect if None.

    Returns:
        List of segments with timestamps and text
    """
    print(f"\nLoading Whisper model: {model_size}")
    print("This may take a few minutes on first run (downloading model)...")

    model = whisper.load_model(model_size)

    print(f"\nTranscribing: {audio_file}")
    print("This may take several minutes for a 40-min video...")

    # Transcribe with word-level timestamps for better accuracy
    result = model.transcribe(
        audio_file,
        language=language,
        task="transcribe",
        word_timestamps=True,  # More precise timing
        verbose=True
    )

    return result["segments"]


def transcribe_with_openai_api(
    audio_file: str,
    api_key: str,
    model: str = "gpt-4o-transcribe"
) -> list:
    """
    Transcribe audio using OpenAI API.

    SOTA Models (2025):
    - gpt-4o-transcribe: Best quality
    - gpt-4o-mini-transcribe: Good quality, faster/cheaper
    - whisper-1: Legacy model, good for SRT with timestamps

    Cost: ~$0.006/minute (~$0.24 for 40min)

    Args:
        audio_file: Path to audio file
        api_key: OpenAI API key
        model: Model to use (default: gpt-4o-transcribe)

    Returns:
        List of segments with timestamps and text
    """
    client = OpenAI(api_key=api_key)

    print(f"\nTranscribing with OpenAI API: {audio_file}")
    print(f"Model: {model}")
    print("Cost: approximately $0.006 per minute")

    # For whisper-1, use verbose_json for segment timestamps
    if model == "whisper-1":
        with open(audio_file, "rb") as audio:
            response = client.audio.transcriptions.create(
                model=model,
                file=audio,
                response_format="verbose_json",
                timestamp_granularities=["segment"]
            )

        segments = []
        for i, segment in enumerate(response.segments):
            segments.append({
                "id": i,
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            })
        return segments

    # For gpt-4o models, use streaming to get segments
    else:
        with open(audio_file, "rb") as audio:
            stream = client.audio.transcriptions.create(
                model=model,
                file=audio,
                response_format="text",
                stream=True
            )

        # Collect segments from stream
        segments = []
        segment_id = 0
        current_start = 0.0

        print("Streaming transcription...")
        full_text = ""
        for event in stream:
            if hasattr(event, 'text'):
                full_text += event.text

        # Since gpt-4o models don't provide segment timestamps in simple mode,
        # we'll create one segment with the full text
        # For proper SRT with timestamps, use whisper-1
        print("\nNote: gpt-4o models provide best quality but limited timestamp support.")
        print("For proper SRT with timestamps, use --api-model whisper-1")

        segments.append({
            "id": 0,
            "start": 0.0,
            "end": 0.0,  # Unknown duration
            "text": full_text.strip()
        })

        return segments


def generate_srt(segments: list, output_file: str):
    """Generate SRT subtitle file from segments."""
    print(f"\nGenerating SRT file: {output_file}")

    with open(output_file, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, 1):
            # SRT format:
            # 1
            # 00:00:00,000 --> 00:00:02,500
            # Subtitle text
            # (blank line)

            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])
            text = segment["text"].strip()

            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n")
            f.write("\n")

    print(f"SRT file created: {output_file}")
    print(f"Total segments: {len(segments)}")


def main():
    parser = argparse.ArgumentParser(
        description="High-quality speech-to-SRT transcription",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download from YouTube and transcribe with local Whisper (free)
  python transcribe.py --url "https://youtube.com/watch?v=..." --local

  # Use local audio/video file
  python transcribe.py --file "meeting.mp4" --local

  # Use OpenAI API (faster, ~$0.24 for 40min)
  python transcribe.py --file "meeting.mp4" --api --openai-key "sk-..."

  # Specify language for better accuracy
  python transcribe.py --file "meeting.mp4" --local --language en

  # Use smaller model for faster (but less accurate) results
  python transcribe.py --file "meeting.mp4" --local --model medium
        """
    )

    # Input source
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--url", help="URL to download video from (YouTube, etc)")
    input_group.add_argument("--file", help="Local audio/video file")

    # Transcription method
    method_group = parser.add_mutually_exclusive_group(required=True)
    method_group.add_argument("--local", action="store_true",
                             help="Use local Whisper model (free, slower)")
    method_group.add_argument("--api", action="store_true",
                             help="Use OpenAI API (fast, ~$0.006/min)")

    # Options
    parser.add_argument("--model", default="large-v3",
                       choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
                       help="Local Whisper model size (default: large-v3 for best quality)")
    parser.add_argument("--api-model", default="whisper-1",
                       choices=["gpt-4o-transcribe", "gpt-4o-mini-transcribe", "whisper-1"],
                       help="OpenAI API model (default: whisper-1 for SRT with timestamps)")
    parser.add_argument("--language", help="Language code (e.g., en, es). Auto-detect if not specified")
    parser.add_argument("--openai-key", help="OpenAI API key (or set in .env file)")
    parser.add_argument("--output", help="Output SRT file path (default: same as input)")

    args = parser.parse_args()

    # Get audio file
    if args.url:
        audio_file = download_video(args.url)
    else:
        audio_file = args.file
        if not os.path.exists(audio_file):
            print(f"Error: File not found: {audio_file}")
            sys.exit(1)

    # Transcribe
    if args.local:
        segments = transcribe_with_local_whisper(audio_file, args.model, args.language)
    else:
        # Use OpenAI API
        api_key = args.openai_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OpenAI API key required. Use --openai-key or set in .env file")
            sys.exit(1)
        segments = transcribe_with_openai_api(audio_file, api_key, args.api_model)

    # Generate SRT
    if args.output:
        output_file = args.output
    else:
        # Use same name as audio file but with .srt extension
        output_file = Path(audio_file).with_suffix(".srt")

    generate_srt(segments, str(output_file))

    print("\nDone! You can now use the SRT file with any video player.")


if __name__ == "__main__":
    main()
