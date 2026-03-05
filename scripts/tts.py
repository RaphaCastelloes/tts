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

try:
    from pydub import AudioSegment
except ImportError:
    # pydub is optional - only needed for OGG conversion
    AudioSegment = None



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


def validate_format(format_type):
    """
    Validate format argument.
    
    Args:
        format_type: Output format (mp3 or ogg)
        
    Returns:
        tuple: (is_valid, error_message)
    """
    valid_formats = ['mp3', 'ogg']
    if format_type not in valid_formats:
        return False, f"Invalid format '{format_type}'. Valid formats: {', '.join(valid_formats)}"
    return True, None


def generate_filename(format_type='mp3'):
    """
    Generate unique filename for audio file.
    
    Format: tts_YYYYMMDD_HHMMSS_<hash>.<format>
    
    Args:
        format_type: Output format (mp3 or ogg), default mp3
    
    Returns:
        str: Generated filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_hash = str(uuid.uuid4())[:8]
    return f"tts_{timestamp}_{unique_hash}.{format_type}"


def get_output_path_with_extension(file_path, format_type):
    """
    Auto-correct file extension to match output format.
    
    Args:
        file_path: User-provided file path (str or Path)
        format_type: Desired output format (mp3 or ogg)
        
    Returns:
        Path: Path with corrected extension
    """
    path = Path(file_path)
    correct_extension = f'.{format_type}'
    
    # If no extension or wrong extension, correct it
    if path.suffix.lower() != correct_extension:
        path = path.with_suffix(correct_extension)
    
    return path


def ensure_output_directory():
    """
    Ensure output directory exists.
    
    Returns:
        Path: Path to output directory
        
    Raises:
        OSError: If directory cannot be created
    """
    output_dir = Path(__file__).parent.parent / "output"
    
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


def convert_to_ogg(mp3_path, ogg_path):
    """
    Convert MP3 file to OGG format with Opus codec.
    
    Args:
        mp3_path: Path to input MP3 file
        ogg_path: Path to output OGG file
        
    Returns:
        Path: Path to generated OGG file
        
    Raises:
        ModuleNotFoundError: If pydub is not installed
        FileNotFoundError: If ffmpeg is not available
        Exception: If conversion fails
    """
    # Check if pydub is available
    if AudioSegment is None:
        raise ModuleNotFoundError(
            "pydub library not found. Install with: pip install pydub==0.25.1"
        )
    
    try:
        # Load MP3 file
        audio = AudioSegment.from_mp3(str(mp3_path))
        
        # Export as OGG with Opus codec
        audio.export(
            str(ogg_path),
            format="ogg",
            codec="libopus"
        )
        
        return Path(ogg_path)
        
    except FileNotFoundError as e:
        # ffmpeg not found
        if 'ffmpeg' in str(e).lower() or 'ffprobe' in str(e).lower():
            raise FileNotFoundError(
                "Cannot convert to OGG format. ffmpeg not found. "
                "Install with: yum install ffmpeg"
            )
        raise
    except Exception as e:
        raise Exception(f"OGG conversion failed: {e}")


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
    parser.add_argument(
        '--format',
        default='mp3',
        choices=['mp3', 'ogg'],
        help='Output audio format: mp3 or ogg (default: mp3)'
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
    
    # Determine output path based on format
    if args.file_path:
        # Use custom file path with format-corrected extension
        output_path = get_output_path_with_extension(args.file_path, args.format)
        # Create parent directory if needed
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print_error(f"Cannot create output directory. Check permissions.")
            sys.exit(EXIT_FILESYSTEM_ERROR)
    else:
        # Generate filename in default output/ directory with correct format
        filename = generate_filename(args.format)
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
    
    # Save MP3 audio to file (always generate MP3 first)
    mp3_path = output_path if args.format == 'mp3' else output_path.with_suffix('.mp3')
    try:
        with open(mp3_path, "wb") as f:
            f.write(mp3_audio.read())
    except Exception as e:
        print_error(f"Cannot write to output directory. Check permissions.")
        sys.exit(EXIT_FILESYSTEM_ERROR)
    
    # Convert to OGG if requested
    if args.format == 'ogg':
        try:
            ogg_path = convert_to_ogg(mp3_path, output_path)
            # Delete intermediate MP3 file after successful conversion
            if mp3_path != output_path:
                mp3_path.unlink()
            output_path = ogg_path
        except ModuleNotFoundError as e:
            print_error(str(e))
            sys.exit(EXIT_PROCESSING_ERROR)
        except FileNotFoundError as e:
            print_error(str(e))
            sys.exit(EXIT_PROCESSING_ERROR)
        except Exception as e:
            print_error(f"Audio format conversion failed: {e}")
            sys.exit(EXIT_PROCESSING_ERROR)
    
    # Print absolute file path to stdout
    print(output_path.absolute())
    sys.exit(EXIT_SUCCESS)


if __name__ == "__main__":
    main()
