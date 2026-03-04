# WhatsApp TTS Script

Convert text to speech and generate WhatsApp-compatible audio files in OGG/Opus format.

**Purpose**: This skill is designed for **OpenClaw bot** integration with WhatsApp channels. It's triggered when users send audio messages to the bot, ensuring the bot responds with voice when users communicate via voice.

## Quick Start

### Installation

1. **Install system dependencies** (Oracle Linux):
```bash
# Enable EPEL repository
sudo yum install -y epel-release

# Install ffmpeg
sudo yum install -y ffmpeg
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```


### Usage

```bash
python tts.py "hello world"
```

The script will:
- Convert your text to speech
- Generate a WhatsApp-compatible audio file (OGG/Opus, 16kHz, mono)
- Print the absolute file path

### Example

```bash
$ python tts.py "Hello, this is a test message"
/home/user/tts/output/tts_20260301_140530_a3f2b1c8.ogg
```

## Features

- ✅ Text-to-speech conversion using Google TTS
- ✅ WhatsApp-compatible audio format (OGG/Opus, 16kHz, mono)
- ✅ 30-50% smaller file sizes compared to MP3
- ✅ Automatic unique file naming
- ✅ Custom output path support
- ✅ Multi-language support (Portuguese-Brazil default)
- ✅ Clear error messages with exit codes

## Requirements

- Python 3.8 or higher
- ffmpeg (with Opus codec support)
- Internet connection (for TTS API)

## Migration from MP3 Version

If you're upgrading from version 1.x (MP3 output):

### What Changed
- **Output Format**: MP3 → OGG/Opus
- **File Extension**: `.mp3` → `.ogg`
- **File Size**: ~50 KB → ~30 KB (30-50% reduction)
- **New Dependencies**: Added pydub, ffmpeg

### What Stayed the Same
- ✅ All CLI arguments unchanged
- ✅ `-o`/`--output` flag works the same way
- ✅ File naming pattern (only extension changed)
- ✅ Error codes (0-4)
- ✅ Output directory structure

### Migration Steps

1. **Install new dependencies**:
```bash
# System dependency
sudo yum install -y epel-release ffmpeg

# Python dependency
pip install pydub==0.25.1
```

2. **Update your scripts** (if you reference file extensions):
```bash
# Old: Find .mp3 files
# find output/ -name "*.mp3"

# New: Find .ogg files
find output/ -name "*.ogg"
```

3. **Test the upgrade**:
```bash
# Generate a test file
python tts.py "test message"

# Verify it's OGG format
file output/tts_*.ogg
# Should show: Ogg data, Opus audio
```

### Backward Compatibility Notes

- **Extension auto-replacement**: If you specify `-o file.mp3`, it will automatically create `file.ogg`
- **Existing MP3 files**: Not affected, remain in output directory
- **CLI commands**: Work exactly the same, just output .ogg instead

## Documentation

See [SKILL.md](SKILL.md) for complete documentation including:
- Detailed usage examples
- Error codes and troubleshooting
- Platform requirements
- Performance characteristics

## Project Structure

```
tts/
├── tts.py                    # Main executable script
├── SKILL.md                  # Complete documentation
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── tests/                    # Test suite
│   ├── test_tts.py
│   ├── test_audio_format.py
│   └── test_integration.py
└── output/                   # Generated audio files
```

## Development

### Running Tests

```bash
pytest tests/
```

### Installing Development Dependencies

```bash
pip install -r requirements.txt
```

## License

See LICENSE file for details.

## Version

**Version**: 2.0.0 (OGG/Opus output)  
**Status**: Production Ready  
**Last Updated**: March 3, 2026
