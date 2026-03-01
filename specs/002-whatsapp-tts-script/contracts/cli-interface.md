# CLI Interface Contract: WhatsApp TTS Script

**Feature**: 002-whatsapp-tts-script  
**Date**: March 1, 2026  
**Version**: 1.0.0  
**Contract Type**: Command-Line Interface

## Overview

This document defines the command-line interface contract for the WhatsApp TTS script. This contract specifies how users interact with the tool, what inputs are accepted, what outputs are produced, and what behaviors are guaranteed.

## Command Syntax

### Basic Usage

```bash
python tts.py <text>
```

**Parameters**:
- `<text>` (required): The text to convert to speech, provided as a single command-line argument

### Examples

```bash
# Simple text
python tts.py "hello world"

# Text with punctuation
python tts.py "Hello, how are you today?"

# Text with quotes (escaped)
python tts.py "She said \"hello\" to me"

# Portuguese text
python tts.py "Olá, como você está?"

# Multi-word text
python tts.py "This is a longer message for WhatsApp"
```

## Input Contract

### Required Arguments

| Argument | Position | Type | Required | Description |
|----------|----------|------|----------|-------------|
| `text` | 1 | string | Yes | Text to convert to speech |

### Input Constraints

- **Minimum length**: 1 character
- **Maximum length**: 1000 characters
- **Encoding**: UTF-8 (supports Unicode, emojis, special characters)
- **Format**: Plain text (no markup or formatting)

### Input Validation

The script MUST validate:
1. At least one argument is provided
2. Text is not empty (after trimming whitespace)
3. Text does not exceed 1000 characters

### Invalid Input Examples

```bash
# No argument provided
python tts.py
# Output: Error: No text provided. Usage: python tts.py "text"
# Exit code: 1

# Empty text
python tts.py ""
# Output: Error: No text provided. Usage: python tts.py "text"
# Exit code: 1

# Text too long (>1000 characters)
python tts.py "$(printf 'a%.0s' {1..1001})"
# Output: Error: Text exceeds maximum length of 1000 characters
# Exit code: 1
```

## Output Contract

### Success Output (stdout)

On successful conversion, the script MUST print to stdout:

```
<absolute_file_path>
```

**Format**:
- Single line containing the absolute file path
- POSIX path format (forward slashes)
- No additional text or formatting
- Newline at end

**Example**:
```
/home/user/tts/output/tts_20260301_140530_a3f2b1c8.ogg
```

### Error Output (stderr)

On error, the script MUST print to stderr:

```
Error: <error_message>
```

**Format**:
- Starts with "Error: " prefix
- Clear, actionable error message
- Single line (or multiple lines for detailed errors)
- Newline at end

**Example**:
```
Error: Cannot connect to TTS service. Check your internet connection.
```

### Exit Codes

The script MUST use the following exit codes:

| Exit Code | Category | Description |
|-----------|----------|-------------|
| `0` | Success | Audio file generated successfully |
| `1` | Input Error | Invalid or missing text input |
| `2` | Network Error | TTS service unavailable or network issue |
| `3` | File System Error | Cannot write file or insufficient disk space |
| `4` | Processing Error | Audio encoding or ffmpeg error |

### Exit Code Examples

```bash
# Success
python tts.py "hello"
echo $?  # Output: 0

# Input error
python tts.py ""
echo $?  # Output: 1

# Network error (simulated)
# Output: Error: Cannot connect to TTS service
echo $?  # Output: 2

# File system error (no write permission)
# Output: Error: Cannot write to output directory
echo $?  # Output: 3

# Processing error (ffmpeg missing)
# Output: Error: ffmpeg not installed (run: sudo yum install ffmpeg)
echo $?  # Output: 4
```

## File Output Contract

### Generated File Specifications

**File Location**:
- Directory: `output/` (relative to script location)
- Created automatically if not exists
- Permissions: 0755 (directory), 0644 (files)

**File Naming**:
- Pattern: `tts_YYYYMMDD_HHMMSS_<hash>.ogg`
- `YYYYMMDD`: Date (e.g., 20260301)
- `HHMMSS`: Time (e.g., 140530)
- `<hash>`: 8-character unique identifier
- Extension: `.ogg` (always lowercase)

**File Format**:
- Container: OGG
- Codec: Opus
- Sample rate: 16000 Hz
- Channels: 1 (mono)
- Bit rate: Variable (optimized by encoder)

**File Properties**:
- Playable in WhatsApp (Android and iOS)
- Typical size: 5-20 KB for 2-10 second audio
- Duration: Proportional to text length

### File Guarantees

The script MUST ensure:
1. File is fully written before printing path
2. File is valid Opus/OGG format
3. File is playable (basic validation)
4. File name is unique (no overwrites)
5. File permissions allow reading

## Behavior Contract

### Guaranteed Behaviors

1. **Idempotency**: Running the script multiple times with the same text produces independent audio files (different file names)
2. **Atomicity**: Either the file is fully created and path printed, or an error is reported (no partial success)
3. **Determinism**: Same text input produces audio with same content (but different file names)
4. **Isolation**: Each execution is independent (no shared state between runs)

### Non-Guaranteed Behaviors

1. **Voice consistency**: Voice may vary based on TTS service updates
2. **Processing time**: Time varies with network latency and text length
3. **File cleanup**: Old files are not automatically deleted
4. **Offline operation**: Requires internet connection (gTTS dependency)

## Error Handling Contract

### Error Categories and Messages

#### 1. Input Validation Errors (Exit Code 1)

```
Error: No text provided. Usage: python tts.py "text"
Error: Text exceeds maximum length of 1000 characters
```

#### 2. Network Errors (Exit Code 2)

```
Error: Cannot connect to TTS service. Check your internet connection.
Error: TTS service temporarily unavailable. Please try again later.
Error: TTS request timed out after 30 seconds
```

#### 3. File System Errors (Exit Code 3)

```
Error: Cannot write to output directory. Check permissions.
Error: Insufficient disk space to create audio file
Error: Output directory path is invalid
```

#### 4. Processing Errors (Exit Code 4)

```
Error: ffmpeg not installed. Run: sudo yum install ffmpeg
Error: Audio encoding failed. Check ffmpeg installation.
Error: Invalid audio format produced
```

### Error Message Requirements

All error messages MUST:
- Be clear and specific
- Suggest resolution when possible
- Avoid technical jargon
- Be single-line (or structured multi-line)
- Include actionable next steps

## Logging Contract

### Standard Error (stderr) Logging

The script MAY output informational logs to stderr:

```
[INFO] Generating speech for 11 characters...
[INFO] Converting audio to Opus/OGG format...
[INFO] Audio file created successfully
```

**Log Format**:
- Prefix: `[LEVEL]` where LEVEL is INFO, WARN, ERROR
- Message: Descriptive text
- Optional: Timestamp, progress indicators

**Log Levels**:
- `[INFO]`: Informational messages (optional, can be suppressed)
- `[WARN]`: Warnings (non-fatal issues)
- `[ERROR]`: Error messages (always shown)

### Quiet Mode (Future Enhancement)

Not implemented in v1.0.0, but reserved for future:
```bash
python tts.py --quiet "hello world"
# Suppresses [INFO] logs, only shows errors
```

## Environment Contract

### Required Environment

- **Operating System**: Linux (Oracle Linux 10 ARM 64-bit)
- **Python Version**: 3.8 or higher
- **Internet**: Required (for gTTS API)
- **System Dependencies**: ffmpeg

### Environment Variables (Optional)

Not used in v1.0.0, but reserved for future:
- `TTS_OUTPUT_DIR`: Override default output directory
- `TTS_LANGUAGE`: Force specific language (override auto-detection)

## Compatibility Contract

### Guaranteed Compatibility

- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Linux**: Oracle Linux 8+, RHEL 8+, CentOS 8+
- **Architecture**: ARM 64-bit, x86_64
- **WhatsApp**: Android and iOS (current versions)

### Not Guaranteed

- **Windows**: Not tested, may work with WSL
- **macOS**: Not tested, may work
- **Python 2.x**: Not supported
- **32-bit systems**: Not supported

## Versioning Contract

### Version Format

`MAJOR.MINOR.PATCH` (Semantic Versioning)

### Breaking Changes

Changes that break this contract require MAJOR version bump:
- Changing command syntax
- Changing exit codes
- Changing output format
- Removing features

### Non-Breaking Changes

Changes that preserve this contract (MINOR/PATCH):
- Adding optional arguments
- Improving error messages
- Performance improvements
- Bug fixes

## Testing Contract

### Contract Validation Tests

The following tests MUST pass to validate contract compliance:

```bash
# Test 1: Basic usage
python tts.py "hello world" && echo "PASS" || echo "FAIL"

# Test 2: Output is absolute path
OUTPUT=$(python tts.py "test")
[[ "$OUTPUT" = /* ]] && echo "PASS" || echo "FAIL"

# Test 3: File exists
OUTPUT=$(python tts.py "test")
[[ -f "$OUTPUT" ]] && echo "PASS" || echo "FAIL"

# Test 4: File is OGG format
OUTPUT=$(python tts.py "test")
file "$OUTPUT" | grep -q "Ogg" && echo "PASS" || echo "FAIL"

# Test 5: Error on empty input
python tts.py "" 2>&1 | grep -q "Error" && echo "PASS" || echo "FAIL"

# Test 6: Exit code on success
python tts.py "test" > /dev/null && [[ $? -eq 0 ]] && echo "PASS" || echo "FAIL"

# Test 7: Exit code on error
python tts.py "" > /dev/null 2>&1 || [[ $? -eq 1 ]] && echo "PASS" || echo "FAIL"
```

## Contract Compliance

This contract is enforced through:
1. Unit tests validating input/output behavior
2. Integration tests validating end-to-end flow
3. Contract tests validating CLI interface
4. Documentation tests validating examples

Any implementation MUST pass all contract tests to be considered compliant.
