# tts Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-28

## Active Technologies
- Python 3.8+ (Oracle Linux compatible) + NEEDS CLARIFICATION (TTS library selection: gTTS, pyttsx3, or other), NEEDS CLARIFICATION (Audio encoding library for Opus/OGG conversion) (002-whatsapp-tts-script)
- Local file system (audio output files) (002-whatsapp-tts-script)
- Python 3.8+ (Oracle Linux compatible) + gTTS 2.5.0 (TTS), pydub 0.25.1 (audio conversion), ffmpeg (system dependency for Opus encoding) (003-ogg-only-output)
- Local file system (audio output files in `output/` directory) (003-ogg-only-output)

- Python 3.8+ (Oracle Linux repository version) + pyttsx3 (offline TTS) or gTTS (online TTS), argparse (CLI parsing) (001-python-tts)

## Project Structure

```text
src/
tests/
```

## Commands

cd src; pytest; ruff check .

## Code Style

Python 3.8+ (Oracle Linux repository version): Follow standard conventions

## Recent Changes
- 003-ogg-only-output: Added Python 3.8+ (Oracle Linux compatible) + gTTS 2.5.0 (TTS), pydub 0.25.1 (audio conversion), ffmpeg (system dependency for Opus encoding)
- 002-whatsapp-tts-script: Added Python 3.8+ (Oracle Linux compatible) + NEEDS CLARIFICATION (TTS library selection: gTTS, pyttsx3, or other), NEEDS CLARIFICATION (Audio encoding library for Opus/OGG conversion)

- 001-python-tts: Added Python 3.8+ (Oracle Linux repository version) + pyttsx3 (offline TTS) or gTTS (online TTS), argparse (CLI parsing)

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
