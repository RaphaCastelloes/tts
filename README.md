# WhatsApp TTS Script

Convert text to speech and generate WhatsApp-compatible audio files in MP3 format.

**Purpose**: This skill is designed for **OpenClaw bot** integration with WhatsApp channels. It's triggered when users send audio messages to the bot, ensuring the bot responds with voice when users communicate via voice.

## Quick Start

### Installation

1. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```


### Usage

```bash
python tts.py "hello world"
```

The script will:
- Convert your text to speech
- Generate a WhatsApp-compatible audio file (MP3)
- Print the absolute file path

### Example

```bash
$ python tts.py "Hello, this is a test message"
/home/user/tts/output/tts_20260301_140530_a3f2b1c8.mp3
```

## Features

- ✅ Text-to-speech conversion using Google TTS
- ✅ WhatsApp-compatible audio format (MP3)
- ✅ Automatic unique file naming
- ✅ Multi-language support (Portuguese-Brazil default)
- ✅ Clear error messages with exit codes

## Requirements

- Python 3.8 or higher
- Internet connection (for TTS API)

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

**Version**: 1.0.0 (MVP)  
**Status**: Production Ready  
**Last Updated**: March 1, 2026
