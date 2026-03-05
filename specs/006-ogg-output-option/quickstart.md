# Quickstart: OGG Output Option

**Feature**: 006-ogg-output-option  
**Date**: 2026-03-05

## What This Feature Does

Adds a `--format` command-line option to the TTS skill enabling direct OGG audio generation with Opus codec for WhatsApp compatibility. This eliminates the need for a separate mp3-to-ogg conversion step in bot workflows.

## Prerequisites

- Python 3.8+ installed
- Existing TTS skill dependencies: gTTS 2.5.0, pytest 7.4.3
- **New**: pydub library
- **New**: ffmpeg system package

## Quick Setup

### 1. Install Dependencies

```bash
# Python dependencies
pip install -r requirements.txt

# System dependency (Oracle Linux)
sudo yum install ffmpeg

# Or using EPEL repository
sudo yum install epel-release
sudo yum install ffmpeg
```

### 2. Verify Installation

```bash
# Test MP3 generation (existing functionality)
python tts.py "Hello world" --lang en

# Test OGG generation (new functionality)
python tts.py "Hello world" --format ogg --lang en
```

## Usage Examples

### Generate OGG Audio

```bash
# Basic OGG generation
python tts.py "Olá, como vai?" --format ogg

# OGG with English language
python tts.py "Hello, how are you?" --format ogg --lang en

# OGG with custom output path
python tts.py "Test message" --format ogg -o my_voice_note.ogg
```

### Generate MP3 Audio (Default)

```bash
# Default format (no change from existing behavior)
python tts.py "Olá mundo"

# Explicit MP3 format
python tts.py "Hello world" --format mp3 --lang en
```

## Integration with WhatsApp Bot

### Before (Old Workflow - 6 Steps)

```bash
# Step 1-3: Bot receives audio, generates text response
# Step 4: Generate MP3
python tts.py "Bot response text"
# Output: /path/to/tts/output/tts_20260305_120000_abc.mp3

# Step 5: Convert MP3 to OGG (separate skill)
python mp3-to-ogg.py /path/to/tts/output/tts_20260305_120000_abc.mp3
# Output: /path/to/tts/output/tts_20260305_120000_abc.ogg

# Step 6: Send OGG to user
```

### After (New Workflow - 5 Steps)

```bash
# Step 1-3: Bot receives audio, generates text response
# Step 4: Generate OGG directly
python tts.py "Bot response text" --format ogg
# Output: /path/to/tts/output/tts_20260305_120000_abc.ogg

# Step 5: Send OGG to user (no conversion needed!)
```

## Testing the Feature

### Manual Testing

```bash
# Run all tests
pytest tests/

# Test format functionality specifically
pytest tests/test_tts.py -k format

# Test OGG file validation
pytest tests/test_audio_format.py -k ogg
```

### Validation Checklist

- [ ] OGG file is generated when `--format ogg` is specified
- [ ] MP3 file is generated when no format specified (default)
- [ ] MP3 file is generated when `--format mp3` is specified
- [ ] File extension is `.ogg` for OGG format
- [ ] File extension is `.mp3` for MP3 format
- [ ] Extension auto-corrects (e.g., `-o file.mp3 --format ogg` creates `file.ogg`)
- [ ] Invalid format returns error with helpful message
- [ ] Generated OGG plays in WhatsApp on Android
- [ ] Generated OGG plays in WhatsApp on iOS
- [ ] Existing MP3 integrations still work without changes

## Troubleshooting

### Error: "Cannot convert to OGG format. ffmpeg not found"

**Cause**: ffmpeg system dependency not installed

**Solution**:
```bash
# Oracle Linux
sudo yum install ffmpeg

# Or use EPEL
sudo yum install epel-release
sudo yum install ffmpeg

# Verify installation
ffmpeg -version
```

### Error: "No module named 'pydub'"

**Cause**: pydub Python library not installed

**Solution**:
```bash
pip install pydub

# Or install all requirements
pip install -r requirements.txt
```

### Error: "Invalid format 'wav'. Valid formats: mp3, ogg"

**Cause**: Specified unsupported format

**Solution**: Use only `--format mp3` or `--format ogg`

### OGG file won't play in WhatsApp

**Cause**: May not be using Opus codec

**Check**:
```bash
# Verify file format
ffprobe output/your_file.ogg

# Should show: codec_name=opus
```

## Performance Notes

- **MP3 generation**: 1-10 seconds (unchanged)
- **OGG conversion**: +100-500ms overhead
- **Total OGG time**: 1.1-10.5 seconds
- Conversion time is negligible compared to TTS generation

## Files Modified

1. **tts.py**: Added `--format` argument, OGG conversion function
2. **requirements.txt**: Added `pydub==0.25.1`
3. **SKILL.md**: Updated with `--format` documentation and simplified workflow
4. **tests/**: New tests for format functionality

## Migration Guide for Existing Bots

### If Using MP3 (No Changes Needed)

Your existing code continues to work:
```bash
# Still works exactly as before
python tts.py "text"
python tts.py "text" --lang en
python tts.py "text" -o myfile.mp3
```

### If Migrating to Direct OGG

Replace your two-step process:
```bash
# Old way (2 commands)
mp3_path=$(python tts.py "text")
ogg_path=$(python mp3-to-ogg.py "$mp3_path")

# New way (1 command)
ogg_path=$(python tts.py "text" --format ogg)
```

## Next Steps

1. Update your bot integration to use `--format ogg` for WhatsApp voice responses
2. Remove dependency on separate mp3-to-ogg conversion skill
3. Test with real WhatsApp messages on both Android and iOS
4. Monitor performance (should be comparable to MP3-only workflow)
5. Update any documentation or scripts that reference the old 6-step workflow

## Support

For issues:
1. Check SKILL.md for detailed documentation
2. Run tests: `pytest tests/`
3. Verify ffmpeg: `ffmpeg -version`
4. Check error messages in stderr for specific guidance
