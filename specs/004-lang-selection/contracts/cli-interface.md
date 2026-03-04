# CLI Interface Contract: Language Selection for TTS

**Feature**: 004-lang-selection  
**Date**: 2026-03-04  
**Contract Version**: 1.0.0

## Overview

This document defines the command-line interface contract for the language selection feature. This contract specifies the exact behavior users can depend on when invoking the TTS script with language options.

## Command Syntax

```bash
python tts.py TEXT [--lang LANGUAGE] [-o OUTPUT]
```

## Arguments

### Positional Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| TEXT | string | Yes | Text to convert to speech (1-1000 characters) |

### Optional Arguments

| Argument | Short | Type | Default | Choices | Description |
|----------|-------|------|---------|---------|-------------|
| --lang | N/A | string | pt-br | en, pt-br | Language for speech output |
| --output | -o | string | auto-generated | any valid path | Custom output file path |

## Language Codes

| Code | Language | Description |
|------|----------|-------------|
| en | English | English (US variant) |
| pt-br | Brazilian Portuguese | Portuguese (Brazilian variant) |

## Behavior Contract

### Default Behavior (Backward Compatible)

When `--lang` is **not** specified:
- Language defaults to `pt-br` (Brazilian Portuguese)
- Existing scripts continue to work without modification
- No breaking changes to current usage patterns

**Example**:
```bash
python tts.py "Hello world"
# Uses pt-br language (default)
```

### Explicit Language Selection

When `--lang` **is** specified:
- Specified language overrides the default
- Must be one of the valid choices: `en` or `pt-br`
- Case-sensitive (lowercase required)

**Examples**:
```bash
python tts.py "Hello world" --lang en
# Uses English language

python tts.py "Olá mundo" --lang pt-br
# Uses Brazilian Portuguese language
```

### Argument Order

The `--lang` argument can appear in any position after the required TEXT argument:

```bash
# All valid and equivalent:
python tts.py "text" --lang en
python tts.py "text" --lang en -o file.mp3
python tts.py "text" -o file.mp3 --lang en
```

## Output Contract

### Success Output (stdout)

On successful execution, prints the absolute path to the generated audio file:

```
/absolute/path/to/output/file.mp3
```

**Guarantees**:
- Always prints absolute path (not relative)
- Path is the only content on stdout (no additional text)
- File exists and is valid MP3 format
- File contains audio in the specified language

### Error Output (stderr)

On error, prints error message to stderr:

```
Error: <descriptive error message>
```

### Exit Codes

| Code | Condition | Description |
|------|-----------|-------------|
| 0 | Success | Audio file generated successfully |
| 1 | Input Error | Invalid language code, missing text, or text too long |
| 2 | Network Error | Cannot connect to TTS service |
| 3 | File System Error | Cannot write output file |
| 4 | Processing Error | Audio processing failed |

## Error Handling Contract

### Invalid Language Code

**Input**:
```bash
python tts.py "text" --lang fr
```

**Output** (stderr):
```
usage: tts.py [-h] [-o FILE_PATH] [--lang {en,pt-br}] text
tts.py: error: argument --lang: invalid choice: 'fr' (choose from 'en', 'pt-br')
```

**Exit Code**: 1

**Guarantees**:
- Error detected before any TTS processing
- No network calls made
- No files created
- Clear error message listing valid choices

### Missing Language Value

**Input**:
```bash
python tts.py "text" --lang
```

**Output** (stderr):
```
usage: tts.py [-h] [-o FILE_PATH] [--lang {en,pt-br}] text
tts.py: error: argument --lang: expected one argument
```

**Exit Code**: 1

### Case Sensitivity

**Input**:
```bash
python tts.py "text" --lang EN
```

**Output** (stderr):
```
tts.py: error: argument --lang: invalid choice: 'EN' (choose from 'en', 'pt-br')
```

**Exit Code**: 1

**Note**: Language codes are case-sensitive and must be lowercase.

## Help Text Contract

When invoked with `--help` or `-h`:

```bash
python tts.py --help
```

**Output** (stdout):
```
usage: tts.py [-h] [-o FILE_PATH] [--lang {en,pt-br}] text

Convert text to speech for WhatsApp

positional arguments:
  text                  Text to convert to speech

optional arguments:
  -h, --help            show this help message and exit
  -o FILE_PATH, --output FILE_PATH
                        Custom output file path (optional). If not provided,
                        auto-generates in output/ directory
  --lang {en,pt-br}     Language for speech output (default: pt-br)
```

**Exit Code**: 0

## Compatibility Guarantees

### Backward Compatibility

1. **Existing Scripts**: All scripts using `python tts.py "text"` continue to work without modification
2. **Default Language**: Default language is `pt-br` (matches current hardcoded behavior)
3. **Output Format**: Output format (stdout/stderr/exit codes) unchanged
4. **File Naming**: Auto-generated filenames follow same pattern when --output not specified

### Forward Compatibility

1. **Language Codes**: `en` and `pt-br` codes will remain supported in all future versions
2. **Argument Names**: `--lang` argument name will not change
3. **Default Value**: `pt-br` will remain the default language
4. **Exit Codes**: Exit code meanings will not change

### Non-Breaking Future Changes

The following changes may be added in future versions without breaking this contract:
- Additional language codes (e.g., `es`, `fr`) added to choices
- Additional optional arguments (e.g., `--speed`, `--voice`)
- Enhanced error messages (as long as exit codes remain the same)

## Testing Contract

To verify compliance with this contract, the following tests must pass:

1. **Default language test**: `python tts.py "test"` uses pt-br
2. **English selection test**: `python tts.py "test" --lang en` uses en
3. **Portuguese selection test**: `python tts.py "test" --lang pt-br` uses pt-br
4. **Invalid language test**: `python tts.py "test" --lang xx` exits with code 1
5. **Help text test**: `python tts.py --help` shows --lang option
6. **Backward compatibility test**: Existing scripts without --lang continue to work

## Version

**Contract Version**: 1.0.0  
**Effective Date**: 2026-03-04  
**Breaking Changes**: None (fully backward compatible)
