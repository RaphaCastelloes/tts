#!/usr/bin/env python3
"""
WhatsApp TTS Script - Convert text to speech for WhatsApp

This script converts text input to speech and generates WhatsApp-compatible
audio files in Opus/OGG format.

Usage: python tts.py "your text here"
"""

import sys
import os
from datetime import datetime
import uuid
from pathlib import Path
import io

try:
    from gtts import gTTS
except ImportError:
    print("Error: gTTS not installed. Run: pip install gTTS==2.5.0", file=sys.stderr)
    sys.exit(4)

try:
    from pydub import AudioSegment
except ImportError:
    print("Error: pydub not installed. Run: pip install pydub==0.25.1", file=sys.stderr)
    sys.exit(4)


# Exit codes
EXIT_SUCCESS = 0
EXIT_INPUT_ERROR = 1
EXIT_NETWORK_ERROR = 2
EXIT_FILESYSTEM_ERROR = 3
EXIT_PROCESSING_ERROR = 4


def validate_input(text):
    """
    Validate text input.
    
    Args:
        text: Input text string
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not text or not text.strip():
        return False, "No text provided. Usage: python tts.py \"text\""
    
    if len(text) > 1000:
        return False, "Text exceeds maximum length of 1000 characters"
    
    return True, None


def generate_filename():
    """
    Generate unique filename for audio file.
    
    Format: tts_YYYYMMDD_HHMMSS_<hash>.ogg
    
    Returns:
        str: Generated filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_hash = str(uuid.uuid4())[:8]
    return f"tts_{timestamp}_{unique_hash}.ogg"


def ensure_output_directory():
    """
    Ensure output directory exists.
    
    Returns:
        Path: Path to output directory
        
    Raises:
        OSError: If directory cannot be created
    """
    output_dir = Path(__file__).parent / "output"
    
    try:
        output_dir.mkdir(exist_ok=True)
        return output_dir
    except OSError as e:
        raise OSError(f"Cannot create output directory: {e}")


def print_error(message):
    """
    Print error message to stderr.
    
    Args:
        message: Error message to print
    """
    print(f"Error: {message}", file=sys.stderr)


def generate_speech(text):
    """
    Generate speech from text using gTTS.
    
    Args:
        text: Text to convert to speech
        
    Returns:
        io.BytesIO: MP3 audio data in memory
        
    Raises:
        Exception: If TTS generation fails
    """
    try:
        # Use English as default, gTTS will auto-detect from text
        tts = gTTS(text=text, lang='en', slow=False)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception as e:
        raise Exception(f"TTS generation failed: {e}")


def encode_to_opus_ogg(mp3_data, output_path):
    """
    Convert MP3 audio to Opus/OGG format for WhatsApp.
    
    Args:
        mp3_data: MP3 audio data (BytesIO object)
        output_path: Path to save the output file
        
    Raises:
        Exception: If encoding fails
    """
    try:
        # Load MP3 audio
        audio = AudioSegment.from_mp3(mp3_data)
        
        # Convert to mono and set sample rate to 16kHz (WhatsApp standard)
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        
        # Export as Opus in OGG container
        audio.export(
            output_path,
            format="ogg",
            codec="libopus",
            parameters=["-strict", "-2"]
        )
    except FileNotFoundError as e:
        if "ffmpeg" in str(e).lower() or "avconv" in str(e).lower():
            raise Exception("ffmpeg not installed. Run: sudo yum install ffmpeg")
        raise Exception(f"Audio encoding failed: {e}")
    except Exception as e:
        raise Exception(f"Audio encoding failed: {e}")


def main():
    """Main execution function."""
    # Check for command-line arguments
    if len(sys.argv) < 2:
        print_error("No text provided. Usage: python tts.py \"text\"")
        sys.exit(EXIT_INPUT_ERROR)
    
    # Get text input
    text = sys.argv[1]
    
    # Validate input
    is_valid, error_msg = validate_input(text)
    if not is_valid:
        print_error(error_msg)
        sys.exit(EXIT_INPUT_ERROR)
    
    # Ensure output directory exists
    try:
        output_dir = ensure_output_directory()
    except OSError as e:
        print_error(f"Cannot write to output directory. Check permissions.")
        sys.exit(EXIT_FILESYSTEM_ERROR)
    
    # Generate filename
    filename = generate_filename()
    output_path = output_dir / filename
    
    # Generate speech from text
    try:
        mp3_audio = generate_speech(text)
    except Exception as e:
        error_msg = str(e)
        # Debug: print actual error
        print(f"[DEBUG] TTS Error: {type(e).__name__}: {error_msg}", file=sys.stderr)
        if "network" in error_msg.lower() or "connection" in error_msg.lower():
            print_error("Cannot connect to TTS service. Check your internet connection.")
            sys.exit(EXIT_NETWORK_ERROR)
        else:
            print_error(f"TTS service temporarily unavailable. Please try again later.")
            sys.exit(EXIT_NETWORK_ERROR)
    
    # Encode audio to Opus/OGG format
    try:
        encode_to_opus_ogg(mp3_audio, output_path)
    except Exception as e:
        error_msg = str(e)
        if "ffmpeg" in error_msg:
            print_error(error_msg)
        else:
            print_error("Audio encoding failed. Check ffmpeg installation.")
        sys.exit(EXIT_PROCESSING_ERROR)
    
    # Print absolute file path to stdout
    print(output_path.absolute())
    sys.exit(EXIT_SUCCESS)


if __name__ == "__main__":
    main()
