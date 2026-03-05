# CLI Interface Contract: TTS Skill with Format Option

**Feature**: 006-ogg-output-option  
**Date**: 2026-03-05  
**Interface Type**: Command-Line Interface

## Command Syntax

```bash
python tts.py TEXT [OPTIONS]
```

## Arguments

### Positional Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `TEXT` | string | Yes | Text to convert to speech (1-1000 characters, UTF-8) |

### Optional Arguments

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--format` | N/A | choice | `mp3` | Output audio format: `mp3` or `ogg` |
| `--lang` | N/A | string | `pt-br` | Language for speech output: `en` or `pt-br` |
| `--output` | `-o` | path | auto | Custom output file path (.mp3/.ogg auto-appended) |
| `--help` | `-h` | flag | N/A | Show help message and exit |

## Output Contract

### Success (Exit Code 0)

**stdout**: Absolute path to generated audio file
```
/absolute/path/to/output/tts_20260305_143000_a1b2c3d4.ogg
```

**stderr**: Empty (or optional logging if verbose mode enabled in future)

**Generated File**: Audio file in specified format at output path

### Error (Exit Code 1-4)

**stdout**: Empty

**stderr**: Error message with actionable guidance
```
Error: Invalid format 'wav'. Valid formats: mp3, ogg
```

## Usage Examples

### Example 1: Generate OGG audio (new feature)
```bash
python tts.py "Hello world" --format ogg --lang en
```
**Output**: `/path/to/tts/output/tts_20260305_143000_abc123.ogg`

### Example 2: Generate MP3 audio (default, backward compatible)
```bash
python tts.py "Olá mundo"
```
**Output**: `/path/to/tts/output/tts_20260305_143001_def456.mp3`

### Example 3: Explicit MP3 format
```bash
python tts.py "Hello" --format mp3 --lang en
```
**Output**: `/path/to/tts/output/tts_20260305_143002_ghi789.mp3`

### Example 4: OGG with custom output path
```bash
python tts.py "Test" --format ogg -o myaudio
```
**Output**: `/path/to/tts/myaudio.ogg` (extension auto-appended)

### Example 5: Extension auto-correction
```bash
python tts.py "Test" --format ogg -o myfile.mp3
```
**Output**: `/path/to/tts/myfile.ogg` (extension corrected to match format)

## Error Cases

### Invalid Format
```bash
python tts.py "hello" --format wav
```
**Exit Code**: 1  
**stderr**: `Error: Invalid format 'wav'. Valid formats: mp3, ogg`

### Missing Text
```bash
python tts.py --format ogg
```
**Exit Code**: 1  
**stderr**: `Error: No text provided. Usage: python tts.py "text"`

### Text Too Long
```bash
python tts.py "[1001+ character text]" --format ogg
```
**Exit Code**: 1  
**stderr**: `Error: Text exceeds maximum length of 1000 characters`

### OGG Conversion Failure (ffmpeg missing)
```bash
python tts.py "hello" --format ogg
# (when ffmpeg not installed)
```
**Exit Code**: 4  
**stderr**: `Error: Cannot convert to OGG format. ffmpeg not found. Install with: yum install ffmpeg`

### Network Error (gTTS service unavailable)
```bash
python tts.py "hello" --format ogg
# (when no internet connection)
```
**Exit Code**: 2  
**stderr**: `Error: Cannot connect to TTS service. Check your internet connection.`

## Backward Compatibility Guarantees

1. **Default behavior unchanged**: Running `python tts.py "text"` without `--format` flag produces MP3 output (same as before)
2. **Existing options preserved**: `--lang` and `-o/--output` work identically for both formats
3. **Exit codes unchanged**: Error codes remain the same (0, 1, 2, 3, 4)
4. **Output format unchanged**: stdout still outputs single line with absolute file path
5. **File naming unchanged**: Default MP3 files use same `tts_YYYYMMDD_HHMMSS_hash.mp3` pattern

## Contract Validation

### Automated Tests Must Verify

- [ ] `--format ogg` generates valid OGG file
- [ ] `--format mp3` generates valid MP3 file
- [ ] No `--format` defaults to MP3 (backward compatibility)
- [ ] Invalid format value returns exit code 1 with error message
- [ ] Extension auto-appended when missing
- [ ] Extension auto-corrected when mismatched with format
- [ ] All existing `--lang` and `-o` functionality works with both formats
- [ ] stdout contains only file path on success
- [ ] stderr contains error message on failure
- [ ] Generated files are playable in WhatsApp (manual test for OGG)

## Version History

- **v1.0** (current): Added `--format` option with mp3/ogg support
- **v0.x** (previous): Only MP3 output, no format option
