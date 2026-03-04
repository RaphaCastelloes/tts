# WhatsApp TTS Script

## Purpose

Convert text to speech and generate WhatsApp-compatible audio files in OGG/Opus format. This command-line tool is designed to be used by an **OpenClaw bot** integrated with WhatsApp channels.

**Bot Integration Use Case**: 

This skill is triggered when a user sends an **audio message** (voice note) to the bot via WhatsApp. The bot workflow is:

1. **User sends audio** → WhatsApp channel receives voice message
2. **Bot detects audio input** → Triggers this TTS skill (not triggered for text messages)
3. **Bot generates response text** → Passes text to this skill
4. **Skill converts text to audio** → Generates WhatsApp-compatible `.ogg` file
5. **Bot sends audio back** → User receives voice response

This ensures the bot maintains the same communication mode as the user: when users send voice messages, they receive voice responses.

## Usage

### Basic Usage

```bash
python tts.py "your text here"
```

### Examples

```bash
# Simple English text
python tts.py "hello world"

# Portuguese text
python tts.py "Olá, como você está?"

# Text with punctuation
python tts.py "Good morning! Let's meet at 3 PM."

# Longer message
python tts.py "This is a longer message that will be converted to speech for WhatsApp."

# Custom output file path
python tts.py "hello" -o /path/to/my_audio.ogg

# Short form
python tts.py "hello" --output custom_name.ogg

# Auto-adds .ogg extension if missing
python tts.py "hello" -o myfile
# Creates: myfile.ogg
```

### Command-Line Options

```bash
# View help
python tts.py --help

# Required argument
python tts.py TEXT              # Text to convert to speech

# Optional arguments
python tts.py TEXT -o FILE      # Custom output file path
python tts.py TEXT --output FILE # Same as -o
```

## Inputs

| Parameter | Type | Required | Description | Constraints |
|-----------|------|----------|-------------|-------------|
| text | string | Yes | Text to convert to speech | 1-1000 characters, UTF-8 encoded |
| -o, --output | string | No | Custom output file path | Valid file path, .mp3 extension auto-added if missing |

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
- **Format**: OGG (Opus codec)
- **Sample Rate**: 16kHz
- **Channels**: Mono
- **Default Naming**: `tts_YYYYMMDD_HHMMSS_<hash>.ogg` (when no custom path specified)
- **Custom Naming**: Your specified filename (auto-adds `.ogg` if missing)
- **Compatibility**: WhatsApp (Android & iOS)

**Examples**:
```bash
# Default: auto-generated in output/
python tts.py "hello"
# Output: /path/to/tts/output/tts_20260303_221254_25f5558e.ogg

# Custom path:
python tts.py "hello" -o my_audio.ogg
# Output: /path/to/tts/my_audio.ogg

# Custom path without extension:
python tts.py "hello" -o my_audio
# Output: /path/to/tts/my_audio.ogg
```

## Dependencies

### Python Dependencies

Install via pip:

```bash
pip install -r requirements.txt
```

Required packages:
- `gTTS==2.5.0` - Google Text-to-Speech API
- `pydub==0.25.1` - Audio processing and format conversion
- `pytest==7.4.3` - Testing framework (development only)

### System Dependencies

**Required**:
- Python 3.8 or higher
- **ffmpeg** - Audio encoder with Opus codec support
- Internet connection (for TTS API)

**Install ffmpeg on Oracle Linux**:
```bash
# Enable EPEL repository
sudo yum install -y epel-release

# Install ffmpeg
sudo yum install -y ffmpeg

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
```

## Troubleshooting

### Audio file not created

**Check**:
1. Internet connection is active
2. Output directory has write permissions: `ls -ld output/`
3. Sufficient disk space: `df -h`

### Audio won't play in WhatsApp

**Verify**:
1. File format: `file output/tts_*.mp3` should show "MP3 audio"
2. File is not corrupted
3. File size is reasonable (10-50 KB for typical messages)

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
