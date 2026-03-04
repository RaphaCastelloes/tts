#!/usr/bin/env python3
"""
WhatsApp TTS Script - Convert text to speech for WhatsApp

This script converts text input to speech and generates WhatsApp-compatible
audio files in MP3 format.

Usage: python tts.py "your text here"
"""

import sys
import argparse
from datetime import datetime
import uuid
from pathlib import Path
import io

try:
    from gtts import gTTS
except ImportError:
    print("Error: gTTS not installed. Run: pip install gTTS==2.5.0", file=sys.stderr)
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
    
    Format: tts_YYYYMMDD_HHMMSS_<hash>.mp3
    
    Returns:
        str: Generated filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_hash = str(uuid.uuid4())[:8]
    return f"tts_{timestamp}_{unique_hash}.mp3"


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


def generate_speech(text, lang='pt-br'):
    """
    Generate speech from text using gTTS.
    
    Args:
        text: Text to convert to speech
        lang: Language code for speech output (default: 'pt-br')
        
    Returns:
        io.BytesIO: MP3 audio data in memory
        
    Raises:
        Exception: If TTS generation fails
    """
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception as e:
        raise Exception(f"TTS generation failed: {e}")


def main():
    """Main execution function."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Convert text to speech for WhatsApp',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('text', help='Text to convert to speech')
    parser.add_argument(
        '-o', '--output',
        dest='file_path',
        help='Custom output file path (optional). If not provided, auto-generates in output/ directory'
    )
    parser.add_argument(
        '--lang',
        default='pt-br',
        choices=['en', 'pt-br'],
        help='Language for speech output (default: pt-br)'
    )
    
    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit(EXIT_INPUT_ERROR)
    
    # Get text input
    text = args.text
    
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
    
    # Determine output path
    if args.file_path:
        # Use custom file path
        output_path = Path(args.file_path)
        # Ensure .mp3 extension
        if output_path.suffix.lower() != '.mp3':
            output_path = output_path.with_suffix('.mp3')
        # Create parent directory if needed
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print_error(f"Cannot create output directory. Check permissions.")
            sys.exit(EXIT_FILESYSTEM_ERROR)
    else:
        # Generate filename in default output/ directory
        filename = generate_filename()
        output_path = output_dir / filename
    
    # Generate speech from text
    try:
        mp3_audio = generate_speech(text, args.lang)
    except Exception as e:
        error_msg = str(e)
        if "network" in error_msg.lower() or "connection" in error_msg.lower():
            print_error("Cannot connect to TTS service. Check your internet connection.")
            sys.exit(EXIT_NETWORK_ERROR)
        else:
            print_error(f"TTS service temporarily unavailable. Please try again later.")
            sys.exit(EXIT_NETWORK_ERROR)
    
    # Save MP3 audio to file
    try:
        with open(output_path, "wb") as f:
            f.write(mp3_audio.read())
    except Exception as e:
        print_error(f"Cannot write to output directory. Check permissions.")
        sys.exit(EXIT_FILESYSTEM_ERROR)
    
    # Print absolute file path to stdout
    print(output_path.absolute())
    sys.exit(EXIT_SUCCESS)


if __name__ == "__main__":
    main()
