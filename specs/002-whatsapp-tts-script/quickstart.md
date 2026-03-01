# Quickstart Guide: WhatsApp TTS Script

**Feature**: 002-whatsapp-tts-script  
**Date**: March 1, 2026  
**Version**: 1.0.0

## Overview

This script converts text to speech and generates WhatsApp-compatible audio files in Opus/OGG format. Perfect for creating voice messages from text that can be shared directly in WhatsApp.

## Prerequisites

### System Requirements

- **Operating System**: Oracle Linux 10 (ARM 64-bit) or compatible
- **Python**: 3.8 or higher
- **Internet**: Required for text-to-speech conversion
- **Disk Space**: ~50 MB for dependencies + space for audio files

### Check Python Version

```bash
python3 --version
# Should show: Python 3.8.x or higher
```

## Installation

### Step 1: Install System Dependencies

```bash
# Install ffmpeg (required for audio encoding)
sudo yum install -y ffmpeg

# Verify ffmpeg installation
ffmpeg -version
```

**Note**: If ffmpeg is not available in default repositories, enable EPEL:

```bash
# Enable EPEL repository
sudo yum install -y epel-release

# Then install ffmpeg
sudo yum install -y ffmpeg
```

### Step 2: Install Python Dependencies

```bash
# Navigate to the project directory
cd /path/to/tts

# Install Python packages
pip3 install -r requirements.txt

# Or install manually:
pip3 install gTTS==2.5.0 pydub==0.25.1
```

### Step 3: Verify Installation

```bash
# Check that Python packages are installed
python3 -c "import gtts, pydub; print('Dependencies OK')"
# Should output: Dependencies OK
```

## Basic Usage

### Simple Text Conversion

```bash
# Convert text to speech
python3 tts.py "hello world"

# Output example:
# /home/user/tts/output/tts_20260301_140530_a3f2b1c8.ogg
```

The script will:
1. Convert your text to speech using Google TTS
2. Encode the audio in WhatsApp-compatible format (Opus/OGG)
3. Save the file to the `output/` directory
4. Print the absolute file path

### Using the Generated Audio

```bash
# Get the file path
AUDIO_FILE=$(python3 tts.py "hello world")

# Play the audio (if you have a media player)
ffplay "$AUDIO_FILE"

# Copy to another location
cp "$AUDIO_FILE" ~/my-audio-messages/

# Send via WhatsApp (manual upload through WhatsApp interface)
```

## Common Examples

### English Text

```bash
python3 tts.py "Hello, how are you today?"
```

### Portuguese Text

```bash
python3 tts.py "Olá, como você está?"
```

### Text with Punctuation

```bash
python3 tts.py "Good morning! Let's meet at 3 PM."
```

### Text with Quotes

```bash
# Use escaped quotes or alternate quote style
python3 tts.py 'She said "hello" to me'
# or
python3 tts.py "She said \"hello\" to me"
```

### Longer Messages

```bash
python3 tts.py "This is a longer message that will be converted to speech. It can contain multiple sentences and will be saved as a single audio file."
```

## Output Files

### File Location

All generated audio files are saved in the `output/` directory:

```
tts/
├── tts.py
├── SKILL.md
├── requirements.txt
└── output/
    ├── tts_20260301_140530_a3f2b1c8.ogg
    ├── tts_20260301_140615_b7e9c2d1.ogg
    └── tts_20260301_141020_f3a8d4e6.ogg
```

### File Naming

Files are named with timestamp and unique identifier:
- Format: `tts_YYYYMMDD_HHMMSS_<hash>.ogg`
- Example: `tts_20260301_140530_a3f2b1c8.ogg`
- Guaranteed unique (no overwrites)

### File Format

- **Container**: OGG
- **Codec**: Opus
- **Sample Rate**: 16000 Hz
- **Channels**: Mono
- **Compatible**: WhatsApp (Android & iOS)

## Error Handling

### Common Errors and Solutions

#### Error: No text provided

```bash
$ python3 tts.py
Error: No text provided. Usage: python tts.py "text"
```

**Solution**: Provide text as an argument:
```bash
python3 tts.py "your text here"
```

#### Error: Cannot connect to TTS service

```bash
$ python3 tts.py "hello"
Error: Cannot connect to TTS service. Check your internet connection.
```

**Solution**: 
- Check internet connection
- Verify network allows access to Google TTS API
- Try again after a few moments

#### Error: ffmpeg not installed

```bash
$ python3 tts.py "hello"
Error: ffmpeg not installed. Run: sudo yum install ffmpeg
```

**Solution**:
```bash
sudo yum install -y ffmpeg
```

#### Error: Cannot write to output directory

```bash
$ python3 tts.py "hello"
Error: Cannot write to output directory. Check permissions.
```

**Solution**:
```bash
# Check directory permissions
ls -ld output/

# Create directory if missing
mkdir -p output

# Fix permissions if needed
chmod 755 output
```

#### Error: Text exceeds maximum length

```bash
$ python3 tts.py "$(cat very-long-text.txt)"
Error: Text exceeds maximum length of 1000 characters
```

**Solution**: Split text into smaller chunks (max 1000 characters each)

## Advanced Usage

### Scripting and Automation

```bash
#!/bin/bash
# Generate multiple audio files from a list

MESSAGES=(
    "Good morning"
    "Good afternoon"
    "Good evening"
)

for msg in "${MESSAGES[@]}"; do
    echo "Generating: $msg"
    python3 tts.py "$msg"
done
```

### Processing Text from File

```bash
# Read text from file (ensure it's under 1000 chars)
TEXT=$(cat message.txt)
python3 tts.py "$TEXT"
```

### Error Handling in Scripts

```bash
#!/bin/bash
# Generate audio with error handling

if OUTPUT=$(python3 tts.py "$1" 2>&1); then
    echo "Success! Audio file: $OUTPUT"
    # Do something with the file
    cp "$OUTPUT" /destination/
else
    echo "Failed to generate audio"
    echo "$OUTPUT"
    exit 1
fi
```

### Checking Exit Codes

```bash
python3 tts.py "hello world"
EXIT_CODE=$?

case $EXIT_CODE in
    0) echo "Success" ;;
    1) echo "Input error" ;;
    2) echo "Network error" ;;
    3) echo "File system error" ;;
    4) echo "Processing error" ;;
esac
```

## Performance

### Expected Processing Time

- **Typical message** (50-500 chars): 2-5 seconds
- **Short message** (<50 chars): 1-3 seconds
- **Long message** (500-1000 chars): 5-10 seconds

**Note**: Processing time depends primarily on network latency to Google TTS API.

### File Sizes

- **Short audio** (1-5 seconds): 5-10 KB
- **Medium audio** (5-15 seconds): 10-20 KB
- **Long audio** (15-30 seconds): 20-40 KB

## Troubleshooting

### Audio Not Playing in WhatsApp

**Symptoms**: File generated but won't play in WhatsApp

**Solutions**:
1. Verify file format:
   ```bash
   file output/tts_*.ogg
   # Should show: Ogg data, Opus audio
   ```

2. Test audio locally:
   ```bash
   ffplay output/tts_*.ogg
   ```

3. Check file isn't corrupted:
   ```bash
   ffprobe output/tts_*.ogg
   ```

### Slow Performance

**Symptoms**: Takes longer than 10 seconds to generate audio

**Solutions**:
1. Check internet speed
2. Try shorter text
3. Check network latency to Google services

### Permission Denied Errors

**Symptoms**: Cannot create or write files

**Solutions**:
```bash
# Check current permissions
ls -la

# Fix script permissions
chmod +x tts.py

# Fix output directory permissions
chmod 755 output/
```

## Limitations

### Current Limitations

1. **Internet Required**: Cannot work offline (gTTS dependency)
2. **Text Length**: Maximum 1000 characters per conversion
3. **No Voice Selection**: Uses default Google TTS voice
4. **No Speed Control**: Default speech rate only
5. **No Batch Processing**: One text input per execution

### Future Enhancements

- Offline TTS support
- Voice selection options
- Speech rate control
- Batch processing mode
- Audio file cleanup utilities

## Getting Help

### Check Script Documentation

```bash
# View full documentation
cat SKILL.md
```

### Verify Installation

```bash
# Check all dependencies
python3 -c "import gtts, pydub; print('Python packages: OK')"
ffmpeg -version > /dev/null && echo "ffmpeg: OK"
```

### Debug Mode

```bash
# Run with Python verbose mode to see detailed errors
python3 -v tts.py "test"
```

## Next Steps

1. **Read SKILL.md**: Comprehensive documentation of the script
2. **Review contracts/**: Detailed CLI interface specifications
3. **Run tests**: Execute test suite to verify installation
4. **Customize**: Modify script for your specific needs

## Quick Reference

```bash
# Basic usage
python3 tts.py "your text here"

# Check dependencies
pip3 list | grep -E "gTTS|pydub"
ffmpeg -version

# View generated files
ls -lh output/

# Clean up old files
rm output/tts_*.ogg

# Get help
cat SKILL.md
```

## Support

For issues, bugs, or feature requests:
1. Check this quickstart guide
2. Review SKILL.md documentation
3. Check contracts/cli-interface.md for CLI details
4. Review error messages for specific guidance
