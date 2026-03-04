# Data Model: Language Selection for TTS

**Feature**: 004-lang-selection  
**Date**: 2026-03-04  
**Status**: Complete

## Overview

This feature adds language selection capability to the TTS script. The data model is minimal as this is a stateless CLI tool with no persistent storage.

## Entities

### Language Configuration

**Description**: Represents the language setting for speech generation.

**Attributes**:
- `code` (string): ISO 639-1 language code with optional regional variant
  - Valid values: `'en'`, `'pt-br'`
  - Default: `'pt-br'`
  - Constraints: Must be one of the supported language codes
  
- `display_name` (string): Human-readable language name
  - Examples: "English", "Brazilian Portuguese"
  - Used in: Help text and documentation

**Validation Rules**:
- Language code must be in the allowed choices list
- Language code is case-sensitive (lowercase required)
- Invalid codes trigger immediate validation error before TTS generation

**State Transitions**: N/A (stateless, no state machine)

**Relationships**: None (single entity, no relationships)

## Data Flow

```
User Input (CLI)
    ↓
argparse validation (choices=['en', 'pt-br'])
    ↓
Language code (default='pt-br' if not specified)
    ↓
gTTS constructor (lang parameter)
    ↓
Audio generation with selected language
    ↓
MP3 file output
```

## Validation

### Input Validation

1. **Language Code Validation**:
   - Performed by: argparse `choices` parameter
   - When: During argument parsing, before any processing
   - Valid inputs: `'en'`, `'pt-br'`
   - Invalid input behavior: Exit with code 1, display error message listing valid choices

2. **Default Value Handling**:
   - When --lang not provided: Use `'pt-br'`
   - Ensures backward compatibility with existing scripts

### Error Cases

| Error Condition | Validation Point | Error Message | Exit Code |
|----------------|------------------|---------------|-----------|
| Invalid language code | argparse choices | "invalid choice: 'XX' (choose from 'en', 'pt-br')" | 1 |
| Missing language value | argparse | "argument --lang: expected one argument" | 1 |

## Implementation Notes

### No Persistent State

This feature does not introduce any persistent state:
- No configuration files
- No database or storage
- No caching of language preferences
- Each invocation is independent

### Memory Footprint

Language selection adds minimal memory overhead:
- Single string variable for language code (~10 bytes)
- No additional data structures required
- No impact on existing memory constraints

### Thread Safety

Not applicable - single-threaded CLI tool with no concurrent execution.

## Examples

### Default Language (Backward Compatible)

```bash
# User doesn't specify --lang
python tts.py "Hello world"

# Internal state:
# language_code = 'pt-br' (default)
# gTTS(text="Hello world", lang='pt-br', slow=False)
```

### Explicit English Selection

```bash
# User specifies --lang en
python tts.py "Hello world" --lang en

# Internal state:
# language_code = 'en'
# gTTS(text="Hello world", lang='en', slow=False)
```

### Explicit Brazilian Portuguese Selection

```bash
# User specifies --lang pt-br
python tts.py "Olá mundo" --lang pt-br

# Internal state:
# language_code = 'pt-br'
# gTTS(text="Olá mundo", lang='pt-br', slow=False)
```

### Invalid Language Code

```bash
# User specifies unsupported language
python tts.py "Hello" --lang fr

# Validation fails at argparse level
# Error: "argument --lang: invalid choice: 'fr' (choose from 'en', 'pt-br')"
# Exit code: 1
# No gTTS call made
```

## Summary

The data model for this feature is intentionally minimal:
- Single entity (Language Configuration) with two supported values
- No persistent storage or state management
- Validation handled entirely by argparse
- No relationships or complex data structures
- Stateless operation maintains simplicity and testability
