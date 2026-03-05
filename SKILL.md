---
name: tts
description: Convert text to speech and generate WhatsApp-compatible audio files in MP3 or OGG format.
---

# WhatsApp TTS Script

## Purpose

Convert text to speech and generate WhatsApp-compatible audio files in MP3 or OGG format. This command-line tool is designed to be used by an **OpenClaw bot** integrated with WhatsApp channels.

**Bot Integration Use Case**: 

This skill is triggered when a user sends an **audio message** (voice note) to the bot via WhatsApp. The bot workflow is:

- Check the skill **whatsapp-audio-sender**

1. **User sends audio** → WhatsApp channel receives voice message
2. **Bot detects audio input** → Triggers this TTS skill (not triggered for text messages)
3. **Bot generates response text** → Passes text to this skill
4. **Skill converts text to audio** → Generates WhatsApp-compatible `.ogg` file (using `--format ogg`)
5. **Bot sends audio back** → User receives voice response

This ensures the bot maintains the same communication mode as the user: when users send voice messages, they receive voice responses.

**Note**: The skill now supports direct OGG generation via the `--format ogg` option, eliminating the need for a separate mp3-to-ogg conversion step.

## Usage

### Basic Usage

```bash
python tts.py "your text here"
```

### Examples

```bash
# Default language (Brazilian Portuguese) - generates MP3
python tts.py "Olá, como você está?"

# English text with explicit language selection
python tts.py "hello world" --lang en

# Generate OGG format for WhatsApp (NEW)
python tts.py "hello world" --format ogg --lang en

# Generate MP3 format (explicit)
python tts.py "hello world" --format mp3 --lang en

# Portuguese text with explicit language selection
python tts.py "Olá mundo" --lang pt-br

# Text with punctuation
python tts.py "Good morning! Let's meet at 3 PM." --lang en

# Longer message
python tts.py "This is a longer message that will be converted to speech for WhatsApp." --lang en

# Custom output file path with OGG format
python tts.py "hello" -o /path/to/my_audio.ogg --format ogg --lang en

# Custom output file path with MP3 format
python tts.py "hello" -o /path/to/my_audio.mp3 --lang en

# Short form
python tts.py "hello" --output custom_name.mp3 --lang en

# Auto-adds correct extension based on format
python tts.py "hello" -o myfile --format ogg --lang en
# Creates: myfile.ogg

# Auto-corrects extension to match format
python tts.py "hello" -o myfile.mp3 --format ogg --lang en
# Creates: myfile.ogg (extension corrected)

# Default language without --lang (backward compatible)
python tts.py "Olá mundo"
# Uses pt-br by default, generates MP3
```

### Command-Line Options

```bash
# View help
python tts.py --help

# Required argument
python tts.py TEXT                  # Text to convert to speech

# Optional arguments
python tts.py TEXT -o FILE          # Custom output file path
python tts.py TEXT --output FILE    # Same as -o
python tts.py TEXT --lang LANG      # Language for speech output (en or pt-br, default: pt-br)
python tts.py TEXT --format FORMAT  # Output format (mp3 or ogg, default: mp3)
```

## Inputs

| Parameter | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| text | string | Yes | Text to convert to speech | 1-1000 characters, UTF-8 encoded |
| -o, --output | string | No | Custom output file path | Valid file path, extension auto-corrected to match format |
| --lang | string | No | Language for speech output | Must be 'en' or 'pt-br' (default: pt-br) |
| --format | string | No | Output audio format | Must be 'mp3' or 'ogg' (default: mp3) |

## Outputs

### Success Output (stdout)

Prints the absolute file path of the generated audio file:

```
/path/to/tts/output/tts_20260301_140530_a3f2b1c8.mp3
```

### Error Output (stderr)

Error messages with actionable guidance:

```
Error: <error_message>
```

### Generated Audio Files

- **Default Location**: `output/` directory (created automatically)
- **Custom Location**: Use `-o` or `--output` to specify any file path
- **Format**: MP3
- **Default Naming**: `tts_YYYYMMDD_HHMMSS_<hash>.mp3` (when no custom path specified)
- **Custom Naming**: Your specified filename (auto-adds `.mp3` if missing)
- **Compatibility**: WhatsApp (Android & iOS)

**Examples**:
```bash
# Default: auto-generated in output/
python tts.py "hello"
# Output: /path/to/tts/output/tts_20260303_221254_25f5558e.mp3

# Custom path:
python tts.py "hello" -o my_audio.mp3
# Output: /path/to/tts/my_audio.mp3

# Custom path without extension:
python tts.py "hello" -o my_audio
# Output: /path/to/tts/my_audio.mp3
```

## Dependencies

### Python Dependencies

Install via pip:

```bash
pip install -r requirements.txt
```

Required packages:
- `gTTS==2.5.0` - Google Text-to-Speech API
- `pydub==0.25.1` - Audio format conversion (required for OGG output)
- `pytest==7.4.3` - Testing framework (development only)

### System Dependencies

**Required**:
- Python 3.8 or higher
- Internet connection (for TTS API)
- **ffmpeg** - Required for OGG format conversion

**Install ffmpeg on Oracle Linux**:
```bash
# Using yum
sudo yum install ffmpeg

# Or using EPEL repository
sudo yum install epel-release
sudo yum install ffmpeg

# Verify installation
ffmpeg -version
```


## Exit Codes

| Code | Category | Description |
|------|----------|-------------|
| 0 | Success | Audio file generated successfully |
| 1 | Input Error | Invalid or missing text input |
| 2 | Network Error | TTS service unavailable or network issue |
| 3 | File System Error | Cannot write file or insufficient disk space |
| 4 | Processing Error | Audio processing error |

## Error Messages

### Input Validation Errors (Exit Code 1)

```
Error: No text provided. Usage: python tts.py "text"
Error: Text exceeds maximum length of 1000 characters
usage: tts.py [-h] [-o FILE_PATH] [--lang {en,pt-br}] [--format {mp3,ogg}] text
tts.py: error: argument --lang: invalid choice: 'fr' (choose from 'en', 'pt-br')
tts.py: error: argument --format: invalid choice: 'wav' (choose from 'mp3', 'ogg')
```

### Network Errors (Exit Code 2)

```
Error: Cannot connect to TTS service. Check your internet connection.
Error: TTS service temporarily unavailable. Please try again later.
```

### File System Errors (Exit Code 3)

```
Error: Cannot write to output directory. Check permissions.
Error: Insufficient disk space to create audio file
```

### Processing Errors (Exit Code 4)

```
Error: Audio processing failed. Please try again.
Error: pydub library not found. Install with: pip install pydub==0.25.1
Error: Cannot convert to OGG format. ffmpeg not found. Install with: yum install ffmpeg
Error: Audio format conversion failed: [specific error details]
```

## Troubleshooting

### Audio file not created

**Check**:
1. Internet connection is active
2. Output directory has write permissions: `ls -ld output/`
3. Sufficient disk space: `df -h`

### Audio won't play in WhatsApp

**Verify**:
1. File format: 
   - MP3: `file output/tts_*.mp3` should show "MP3 audio"
   - OGG: `file output/tts_*.ogg` should show "Ogg data, Opus audio"
2. File is not corrupted
3. File size is reasonable (10-50 KB for typical messages)
4. For OGG files, verify Opus codec: `ffprobe output/tts_*.ogg`

### OGG conversion fails

**Check**:
1. ffmpeg is installed: `ffmpeg -version`
2. pydub is installed: `pip show pydub`
3. Sufficient disk space for conversion
4. Original MP3 file is valid

### Slow performance

**Causes**:
- Network latency to Google TTS API
- Very long text input (>500 characters)
- Slow internet connection

**Solutions**:
- Use shorter text inputs
- Check network speed
- Ensure stable internet connection

### Permission denied errors

**Fix permissions**:

```bash
# Make script executable
chmod +x tts.py

# Fix output directory permissions
chmod 755 output/
```

## Platform Requirements

**Supported**:
- Oracle Linux 8+ (ARM 64-bit and x86_64)
- RHEL 8+
- CentOS 8+
- Python 3.8, 3.9, 3.10, 3.11, 3.12

**Not Tested**:
- Windows (may work with WSL)
- macOS (may work)
- Python 2.x (not supported)

## Performance

**Expected Processing Time**:
- Short messages (<50 chars): 1-3 seconds
- Typical messages (50-500 chars): 2-5 seconds
- Long messages (500-1000 chars): 5-10 seconds

**File Sizes**:
- Short audio (1-5 seconds): 5-10 KB
- Medium audio (5-15 seconds): 10-20 KB
- Long audio (15-30 seconds): 20-40 KB

## Limitations

1. **Internet Required**: Cannot work offline (gTTS dependency)
2. **Text Length**: Maximum 1000 characters per conversion
3. **No Voice Selection**: Uses default Google TTS voice
4. **No Speed Control**: Default speech rate only
5. **No Batch Processing**: One text input per execution

## Development

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_tts.py

# Run with coverage
pytest --cov=tts tests/
```

### Project Structure

```
tts/
├── tts.py                    # Main executable script
├── SKILL.md                  # This file
├── requirements.txt          # Python dependencies
├── tests/
│   ├── test_tts.py          # Unit tests
│   ├── test_audio_format.py # Format validation tests
│   └── test_integration.py  # Integration tests
└── output/                   # Generated audio files
```

## Version

**Version**: 1.0.0  
**Last Updated**: March 1, 2026  
**License**: See project LICENSE file
