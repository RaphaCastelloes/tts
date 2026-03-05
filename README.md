# WhatsApp TTS Script

Convert text to speech and generate WhatsApp-compatible audio files in MP3 or OGG format.

**Purpose**: This skill is designed for **OpenClaw bot** integration with WhatsApp channels. It's triggered when users send audio messages to the bot, ensuring the bot responds with voice when users communicate via voice.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate MP3 (default)
python scripts/tts.py "hello world" --lang en

# Generate OGG for WhatsApp
python scripts/tts.py "hello world" --format ogg --lang en
```

## Features

- ✅ Text-to-speech using Google TTS
- ✅ MP3 and OGG output formats
- ✅ Multi-language support (en, pt-br)
- ✅ WhatsApp-compatible audio
- ✅ Direct OGG generation with Opus codec

## Documentation

See **[SKILL.md](SKILL.md)** for complete documentation including:
- Detailed usage examples and all command-line options
- Error codes, troubleshooting, and migration notes
- Platform requirements and performance characteristics
- Installation instructions for ffmpeg and dependencies

## Requirements

- Python 3.8+
- Internet connection (for TTS API)
- ffmpeg (for OGG format conversion)

## Version

**Version**: 1.1.0  
**Status**: Production Ready  
**Last Updated**: March 5, 2026
