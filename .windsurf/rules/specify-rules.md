# tts Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-28

## Active Technologies
- Python 3.8+ (Oracle Linux compatible) + NEEDS CLARIFICATION (TTS library selection: gTTS, pyttsx3, or other), NEEDS CLARIFICATION (Audio encoding library for Opus/OGG conversion) (002-whatsapp-tts-script)
- Local file system (audio output files) (002-whatsapp-tts-script)
- Python 3.8+ + gTTS 2.5.0, argparse (stdlib) (004-lang-selection)
- N/A (stateless CLI tool) (004-lang-selection)
- N/A (documentation only) + N/A (documentation only) (005-update-workflow-docs)
- Python 3.8+ + gTTS 2.5.0 (existing), pydub (new), ffmpeg (system dependency) (006-ogg-output-option)
- File system (output/ directory for generated audio files) (006-ogg-output-option)
- Python 3.8+ (no code changes) + None (refactoring only—uses existing gTTS, pydub, pytest) (007-reorganize-scripts)
- File system (no changes to storage) (007-reorganize-scripts)

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
- 007-reorganize-scripts: Added Python 3.8+ (no code changes) + None (refactoring only—uses existing gTTS, pydub, pytest)
- 006-ogg-output-option: Added Python 3.8+ + gTTS 2.5.0 (existing), pydub (new), ffmpeg (system dependency)
- 005-update-workflow-docs: Added N/A (documentation only) + N/A (documentation only)


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
