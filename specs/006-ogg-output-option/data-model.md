# Data Model: OGG Output Option

**Feature**: 006-ogg-output-option  
**Date**: 2026-03-05

## Overview

This feature adds format selection to the TTS skill. The data model is minimal as this is a CLI tool enhancement with file-based outputs.

## Entities

### AudioOutput

**Purpose**: Represents a generated audio file with its metadata

**Attributes**:
- `file_path` (string): Absolute path to the generated audio file
- `format` (enum: 'mp3' | 'ogg'): Audio file format
- `extension` (string): File extension (.mp3 or .ogg)
- `file_size` (integer): Size of the audio file in bytes
- `language` (string): Language code used for TTS (e.g., 'en', 'pt-br')
- `text_content` (string): Original text converted to speech
- `timestamp` (datetime): When the file was generated

**Relationships**: None (standalone entity)

**Validation Rules**:
- `file_path` must be absolute path
- `format` must be either 'mp3' or 'ogg'
- `extension` must match format (.mp3 for mp3, .ogg for ogg)
- `file_size` must be > 0
- `language` must be valid gTTS language code
- `text_content` must be 1-1000 characters

### FormatConfiguration

**Purpose**: User-specified format preference for audio output

**Attributes**:
- `format_type` (enum: 'mp3' | 'ogg'): Desired output format
- `is_default` (boolean): Whether this is the default format (MP3 = true)

**Relationships**: Determines which AudioOutput format is generated

**Validation Rules**:
- `format_type` must be 'mp3' or 'ogg' only
- Invalid format values should be rejected with error message

**State Transitions**:
1. **Not specified** → Default to 'mp3' (backward compatibility)
2. **User specifies `--format mp3`** → Set to 'mp3'
3. **User specifies `--format ogg`** → Set to 'ogg'
4. **User specifies invalid format** → Error state, exit with code 1

## File Naming Pattern

### MP3 Format (existing)
- Pattern: `tts_YYYYMMDD_HHMMSS_<hash>.mp3`
- Example: `tts_20260305_143000_a1b2c3d4.mp3`

### OGG Format (new)
- Pattern: `tts_YYYYMMDD_HHMMSS_<hash>.ogg`
- Example: `tts_20260305_143000_a1b2c3d4.ogg`

### Custom Output Path
- If user provides `-o myfile`, auto-append extension: `myfile.mp3` or `myfile.ogg`
- If user provides `-o myfile.mp3` with `--format ogg`, auto-correct to `myfile.ogg`

## Data Flow

```
User Input (text + format)
    ↓
Validate format argument
    ↓
Generate MP3 via gTTS (existing logic)
    ↓
[If format == 'ogg']
    Convert MP3 → OGG using pydub
    Delete intermediate MP3 (optional)
    ↓
Determine output filename
    ↓
Auto-correct extension to match format
    ↓
Save file to output/ directory
    ↓
Return absolute file path to stdout
```

## Error States

### Input Validation Errors (Exit Code 1)
- Invalid format specified (not 'mp3' or 'ogg')
- Text too long (>1000 characters)
- Invalid language code

### Conversion Errors (Exit Code 4)
- pydub import failure (library not installed)
- ffmpeg not available (system dependency missing)
- OGG conversion failure (corrupted MP3, codec error)
- Insufficient disk space for conversion

## Storage Location

**Output Directory**: `output/` (created automatically if not exists)

**File Permissions**: 644 (readable by all, writable by owner)

**Cleanup**: Files not automatically deleted (user responsibility)

## Notes

- No database or persistent storage required
- All state is ephemeral (exists only during command execution)
- Output files persist on filesystem but are not tracked by the application
- File format determined at generation time based on user input
