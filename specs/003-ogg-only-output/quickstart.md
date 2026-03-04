# Quickstart Guide: OGG-Only Audio Output

**Feature**: 003-ogg-only-output  
**Date**: March 3, 2026  
**Version**: 2.0.0

## Overview

This guide covers upgrading the WhatsApp TTS script from MP3 output to OGG/Opus format. The change provides 30-50% file size reduction while maintaining full backward compatibility with existing command-line arguments.

## Prerequisites

### System Requirements

- **Operating System**: Oracle Linux (ARM 64-bit) or compatible
- **Python**: 3.8 or higher
- **Internet**: Required for text-to-speech conversion
- **Disk Space**: ~100 MB for dependencies + space for audio files

### Verify Prerequisites

```bash
python3 --version
# Should show: Python 3.8.x or higher
```

## Installation

### Step 1: Install System Dependencies

```bash
# Enable EPEL repository (if not already enabled)
sudo yum install -y epel-release

# Install ffmpeg (required for OGG/Opus encoding)
sudo yum install -y ffmpeg

# Verify ffmpeg installation
ffmpeg -version

# Check for Opus codec support
ffmpeg -codecs 2>/dev/null | grep opus
# Should show: DEA.L. opus
```

**Note**: If ffmpeg is not available in default repositories, EPEL must be enabled:

```bash
# Alternative: Enable EPEL first
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
# Check Python packages
python3 -c "import gtts, pydub; print('Python packages: OK')"

# Check ffmpeg
ffmpeg -version > /dev/null && echo "ffmpeg: OK"
```

## Basic Usage

### Simple Text Conversion

```bash
# Convert text to speech (OGG output)
python3 tts.py "hello world"

# Output example:
# /home/user/tts/output/tts_20260303_221000_a3f2b1c8.ogg
```

The script will:
1. Convert your text to speech using Google TTS
2. Convert the MP3 output to OGG/Opus format
3. Optimize for WhatsApp (16kHz, mono)
4. Save the file to the `output/` directory
5. Print the absolute file path

### Using the Generated Audio

```bash
# Get the file path
AUDIO_FILE=$(python3 tts.py "hello world")

# Play the audio (if you have a media player)
ffplay "$AUDIO_FILE"

# Check file properties
ffprobe "$AUDIO_FILE" 2>&1 | grep -E "(Stream|Duration)"

# Send via WhatsApp API or copy to device
cp "$AUDIO_FILE" /path/to/whatsapp/
```

## Advanced Usage

### Custom Output Path

```bash
# Specify exact filename
python3 tts.py "hello" -o my_audio.ogg
# Output: /current/directory/my_audio.ogg

# Without extension (auto-adds .ogg)
python3 tts.py "hello" -o myfile
# Output: /current/directory/myfile.ogg

# Full absolute path
python3 tts.py "hello" -o /tmp/audio.ogg
# Output: /tmp/audio.ogg

# Extension replacement (.mp3 → .ogg)
python3 tts.py "hello" -o audio.mp3
# Output: /current/directory/audio.ogg
```

### Portuguese Language (Default)

The script defaults to Portuguese (Brazil) but works with any language:

```bash
# Portuguese (default)
python3 tts.py "Olá, como você está?"

# English
python3 tts.py "Hello, how are you?"

# Spanish
python3 tts.py "Hola, ¿cómo estás?"
```

### Batch Processing

```bash
# Process multiple messages
cat << EOF | while read -r text; do python3 tts.py "$text"; done
Welcome to the system
Your order has been confirmed
Thank you for your purchase
EOF

# From file
while IFS= read -r line; do
    python3 tts.py "$line" -o "message_$(date +%s).ogg"
done < messages.txt
```

## Migration from MP3 Version

### What Changed

| Aspect | Old (v1.x MP3) | New (v2.0 OGG) |
|--------|----------------|----------------|
| **File Extension** | `.mp3` | `.ogg` |
| **Audio Format** | MP3 | OGG/Opus |
| **File Size** | ~50 KB | ~30 KB (30-50% smaller) |
| **Dependencies** | gTTS only | gTTS + pydub + ffmpeg |
| **CLI Arguments** | Same | Same (fully compatible) |
| **File Naming** | `tts_*.mp3` | `tts_*.ogg` |

### What Stayed the Same

✅ All command-line arguments  
✅ `-o` / `--output` flag behavior  
✅ Input validation rules  
✅ Exit codes (0-4)  
✅ Error messages  
✅ Output directory structure  
✅ File naming pattern (only extension changed)

### Migration Steps

1. **Install new dependencies**:
   ```bash
   sudo yum install -y ffmpeg
   pip3 install pydub==0.25.1
   ```

2. **Update your automation** (if needed):
   ```bash
   # Old scripts looking for .mp3 files:
   # find output/ -name "*.mp3"
   
   # Update to:
   find output/ -name "*.ogg"
   ```

3. **No code changes needed**:
   ```bash
   # This still works exactly the same:
   python3 tts.py "hello" -o custom.ogg
   ```

## File Structure

### File Location

All generated audio files are saved in the `output/` directory:

```
tts/
├── tts.py
├── SKILL.md
├── requirements.txt
└── output/
    ├── tts_20260303_221000_a3f2b1c8.ogg
    ├── tts_20260303_221015_b7e9c2d1.ogg
    └── tts_20260303_221020_f3a8d4e6.ogg
```

### File Naming

Files are named with timestamp and unique identifier:
- Format: `tts_YYYYMMDD_HHMMSS_<hash>.ogg`
- Example: `tts_20260303_221000_a3f2b1c8.ogg`
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

**Solution**: Provide text as argument:
```bash
python3 tts.py "your text here"
```

#### Error: Text exceeds maximum length

```bash
$ python3 tts.py "$(python -c 'print("a" * 1001)')"
Error: Text exceeds maximum length of 1000 characters
```

**Solution**: Reduce text length to 1000 characters or less.

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
sudo yum install -y epel-release
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

# Fix permissions if needed
chmod 755 output/

# Or create directory
mkdir -p output
```

#### Error: Audio encoding failed

```bash
$ python3 tts.py "hello"
Error: Audio encoding failed. Check ffmpeg installation.
```

**Solution**:
```bash
# Verify ffmpeg has Opus support
ffmpeg -codecs 2>/dev/null | grep opus

# Reinstall ffmpeg if needed
sudo yum reinstall ffmpeg
```

## Troubleshooting

### Audio Not Playing in WhatsApp

**Symptoms**: File generated but won't play in WhatsApp

**Solutions**:
1. Verify file format:
   ```bash
   file output/tts_*.ogg
   # Should show: Ogg data, Opus audio
   ```

2. Check file properties:
   ```bash
   ffprobe output/tts_*.ogg 2>&1 | grep Stream
   # Should show: Audio: opus, 16000 Hz, mono
   ```

3. Check file isn't corrupted:
   ```bash
   ls -lh output/tts_*.ogg
   # File size should be > 0
   ```

### Slow Performance

**Symptoms**: Takes longer than 10 seconds to generate audio

**Solutions**:
1. Check internet speed
2. Try shorter text
3. Check network latency to Google services:
   ```bash
   ping -c 5 translate.google.com
   ```

### File Size Too Large

**Symptoms**: OGG files larger than expected

**Solutions**:
1. OGG files should be 30-50% smaller than MP3
2. Verify Opus codec is being used:
   ```bash
   ffprobe output/tts_*.ogg 2>&1 | grep codec
   # Should show: codec_name=opus
   ```

## Best Practices

### For Production Use

1. **Error Handling**: Always check exit codes
   ```bash
   if python3 tts.py "hello"; then
       echo "Success"
   else
       echo "Failed with exit code: $?"
   fi
   ```

2. **Logging**: Redirect errors for debugging
   ```bash
   python3 tts.py "hello" 2>> tts_errors.log
   ```

3. **Monitoring**: Track file generation
   ```bash
   ls -lt output/ | head -10
   ```

4. **Cleanup**: Manage disk space
   ```bash
   # Delete files older than 7 days
   find output/ -name "*.ogg" -mtime +7 -delete
   ```

### For Development

1. **View help**:
   ```bash
   python3 tts.py --help
   ```

2. **Check all dependencies**:
   ```bash
   python3 -c "import gtts, pydub; print('Python packages: OK')"
   ffmpeg -version > /dev/null && echo "ffmpeg: OK"
   ```

3. **Test with various inputs**:
   ```bash
   python3 tts.py "Short"
   python3 tts.py "Medium length message"
   python3 tts.py "Very long message..." # up to 1000 chars
   ```

## Quick Reference

```bash
# Basic usage
python3 tts.py "your text here"

# Custom output path
python3 tts.py "text" -o custom.ogg

# Check dependencies
pip3 list | grep -E "gTTS|pydub"
ffmpeg -version

# View generated files
ls -lh output/

# Clean up old files
find output/ -name "*.ogg" -mtime +7 -delete

# Get help
python3 tts.py --help
cat SKILL.md
```

## Next Steps

1. **Integrate with your bot**: Use the generated OGG files in your WhatsApp bot
2. **Monitor performance**: Track generation times and file sizes
3. **Set up automation**: Create scripts for batch processing
4. **Configure cleanup**: Set up cron jobs to manage disk space

## Support

For issues, bugs, or feature requests:
1. Check this quickstart guide
2. Review SKILL.md documentation
3. Verify all dependencies are installed
4. Check error messages and exit codes
5. Review Oracle Linux compatibility

## Changelog

**v2.0.0** (2026-03-03):
- Changed output format from MP3 to OGG/Opus
- Added ffmpeg system dependency
- Added pydub Python dependency
- Improved file size (30-50% reduction)
- Maintained full backward compatibility for CLI arguments

**v1.1.0** (2026-03-03):
- Added `-o`/`--output` flag for custom file paths

**v1.0.0** (2026-03-01):
- Initial release with MP3 output
