# CLI Interface Contract: OGG-Only Audio Output

**Feature**: 003-ogg-only-output
**Date**: March 3, 2026
**Purpose**: Define command-line interface contract for OGG audio generation

## Command Syntax

```bash
python tts.py <text> [-o|--output <file_path>]
```

### Required Parameters

| Parameter | Type | Description | Validation |
|-----------|------|-------------|------------|
| `text` | string | Text to convert to speech | 1-1000 characters, UTF-8, non-empty |

### Optional Parameters

| Parameter | Type | Description | Default | Validation |
|-----------|------|-------------|---------|------------|
| `-o`, `--output` | string | Custom output file path | Auto-generated in `output/` | Valid file path, .ogg extension added if missing |

## Input Constraints

### Text Input
- **Minimum length**: 1 character
- **Maximum length**: 1000 characters
- **Encoding**: UTF-8
- **Allowed characters**: All UTF-8 characters including:
  - Letters (any language)
  - Numbers
  - Punctuation
  - Emojis
  - Accented characters
- **Forbidden**: Empty string, whitespace-only

### Output Path (optional)
- **Format**: Any valid file path (absolute or relative)
- **Extension handling**:
  - If `.mp3` provided → replaced with `.ogg`
  - If `.ogg` provided → kept as-is
  - If no extension → `.ogg` added automatically
  - Any other extension → kept but `.ogg` appended
- **Directory creation**: Parent directories created automatically if needed
- **Permissions**: Write access required

## Output Formats

### Success Output (stdout)

Single line containing the absolute path to the generated OGG file:

```
/home/user/tts/output/tts_20260303_221000_a3f2b1c8.ogg
```

**Format**: Absolute file path (POSIX-style on Linux)
**Encoding**: UTF-8
**Line ending**: LF (Unix-style)

### Error Output (stderr)

Error messages follow the format:

```
Error: <descriptive_message>
```

**Examples**:
```
Error: No text provided. Usage: python tts.py "text"
Error: Text exceeds maximum length of 1000 characters
Error: Cannot connect to TTS service. Check your internet connection.
Error: Cannot write to output directory. Check permissions.
Error: ffmpeg not installed. Run: sudo yum install ffmpeg
Error: Audio encoding failed. Check ffmpeg installation.
```

## Exit Codes

| Code | Name | Condition | Example |
|------|------|-----------|---------|
| 0 | EXIT_SUCCESS | Audio file successfully generated | File created and path printed |
| 1 | EXIT_INPUT_ERROR | Invalid input parameters | Empty text, text too long |
| 2 | EXIT_NETWORK_ERROR | Network/API failure | gTTS API unreachable |
| 3 | EXIT_FILESYSTEM_ERROR | File system issue | No write permissions, disk full |
| 4 | EXIT_PROCESSING_ERROR | Audio processing failure | ffmpeg not installed, encoding failed |

## File Output Specification

### Default Output Location

```
tts/output/tts_YYYYMMDD_HHMMSS_<hash>.ogg
```

**Components**:
- `tts_`: Fixed prefix
- `YYYYMMDD`: Date (e.g., 20260303)
- `_`: Separator
- `HHMMSS`: Time (e.g., 221000)
- `_`: Separator
- `<hash>`: 8-character UUID-based unique identifier
- `.ogg`: File extension

**Example**: `tts_20260303_221000_a3f2b1c8.ogg`

### Custom Output Location

When using `-o` flag:

```bash
# Exact path with extension
python tts.py "hello" -o /path/to/my_audio.ogg
# Output: /path/to/my_audio.ogg

# Path without extension (auto-adds .ogg)
python tts.py "hello" -o /path/to/my_audio
# Output: /path/to/my_audio.ogg

# Path with .mp3 extension (replaces with .ogg)
python tts.py "hello" -o /path/to/my_audio.mp3
# Output: /path/to/my_audio.ogg

# Relative path
python tts.py "hello" -o custom_output.ogg
# Output: /current/directory/custom_output.ogg (absolute path printed)
```

### File Format

- **Container**: OGG (Ogg Vorbis container)
- **Codec**: Opus
- **Sample Rate**: 16000 Hz (16 kHz)
- **Channels**: 1 (mono)
- **Bit Rate**: Variable (Opus adaptive, typically 24-32 kbps for speech)
- **WhatsApp Compatible**: Yes (Android, iOS, Web, Desktop)

## Usage Examples

### Basic Usage

```bash
# Simple English text
$ python tts.py "hello world"
/home/user/tts/output/tts_20260303_221000_a3f2b1c8.ogg

# Portuguese text
$ python tts.py "Olá, como você está?"
/home/user/tts/output/tts_20260303_221015_b7e9c2d1.ogg

# Text with special characters
$ python tts.py "Good morning! Let's meet at 3 PM 🎉"
/home/user/tts/output/tts_20260303_221020_f3a8d4e6.ogg
```

### Custom Output Path

```bash
# Specify custom filename
$ python tts.py "hello" -o my_audio.ogg
/home/user/tts/my_audio.ogg

# Short form
$ python tts.py "hello" --output custom.ogg
/home/user/tts/custom.ogg

# Without extension (auto-adds .ogg)
$ python tts.py "hello" -o myfile
/home/user/tts/myfile.ogg

# Full absolute path
$ python tts.py "hello" -o /tmp/test_audio.ogg
/tmp/test_audio.ogg

# Replaces .mp3 with .ogg
$ python tts.py "hello" -o audio.mp3
/home/user/tts/audio.ogg
```

### Error Cases

```bash
# Empty text
$ python tts.py ""
Error: No text provided. Usage: python tts.py "text"
[Exit code: 1]

# Text too long
$ python tts.py "$(python -c 'print("a" * 1001)')"
Error: Text exceeds maximum length of 1000 characters
[Exit code: 1]

# No arguments
$ python tts.py
Error: No text provided. Usage: python tts.py "text"
[Exit code: 1]

# Network error (gTTS API down)
$ python tts.py "hello"
Error: Cannot connect to TTS service. Check your internet connection.
[Exit code: 2]

# Permission error
$ python tts.py "hello" -o /root/audio.ogg
Error: Cannot write to output directory. Check permissions.
[Exit code: 3]

# ffmpeg not installed
$ python tts.py "hello"
Error: ffmpeg not installed. Run: sudo yum install ffmpeg
[Exit code: 4]
```

### Scripting Usage

```bash
# Capture output path
AUDIO_FILE=$(python tts.py "Welcome to the system")
echo "Generated: $AUDIO_FILE"

# Check exit code
python tts.py "hello"
if [ $? -eq 0 ]; then
    echo "Success"
else
    echo "Failed"
fi

# Batch processing
while IFS= read -r line; do
    python tts.py "$line"
done < messages.txt

# With custom naming
python tts.py "Status update" -o "status_$(date +%Y%m%d).ogg"
```

## Environment Requirements

### System Dependencies

- **Python**: 3.8 or higher
- **ffmpeg**: 3.0 or higher (with libopus support)
- **Operating System**: Oracle Linux ARM 64-bit (or compatible)
- **Network**: Internet connection required (for gTTS API)

### Installation

```bash
# Install system dependencies
sudo yum install -y epel-release
sudo yum install -y ffmpeg python3

# Verify ffmpeg
ffmpeg -version | grep opus

# Install Python dependencies
pip3 install -r requirements.txt
```

### Python Packages

```
gTTS==2.5.0
pydub==0.25.1
pytest==7.4.3
```

## Behavior Guarantees

### Atomicity
- Files are written atomically (no partial files on failure)
- Either complete OGG file or no file at all
- No temporary files left behind

### Idempotency
- Same text input produces different filenames (timestamp + random hash)
- Running multiple times with same input is safe (no overwrites)
- Each execution is independent

### Determinism
- Same text → consistent audio quality
- Same text → different filenames (time-based uniqueness)
- Exit codes are deterministic based on error type

### Performance
- Typical execution time: 2-4 seconds
- Maximum execution time: 10 seconds (spec requirement)
- File size: 30-50% smaller than equivalent MP3

## Backward Compatibility

### Preserved from Previous Version
- ✅ Command-line argument structure
- ✅ `-o` / `--output` flag behavior
- ✅ Input validation rules
- ✅ Exit codes (0-4)
- ✅ Error message format
- ✅ Stdout/stderr separation
- ✅ File naming pattern (only extension changed)
- ✅ Output directory structure

### Changed from Previous Version
- ❌ File extension: `.mp3` → `.ogg`
- ❌ File format: MP3 → OGG/Opus
- ❌ File size: ~50 KB → ~30 KB (30-50% reduction)
- ❌ Dependencies: Added pydub, ffmpeg

### Migration from MP3 Version

```bash
# Old command (MP3 output)
python tts.py "hello"
# Output: /home/user/tts/output/tts_20260303_221000_a3f2b1c8.mp3

# New command (OGG output) - SAME SYNTAX
python tts.py "hello"
# Output: /home/user/tts/output/tts_20260303_221000_a3f2b1c8.ogg

# Custom path migration
# Old: -o audio.mp3 → creates audio.mp3
# New: -o audio.mp3 → creates audio.ogg (extension replaced)
# New: -o audio.ogg → creates audio.ogg (explicit extension)
```

## Test Contract

### Unit Test Requirements
- Input validation for all constraint boundaries
- Extension handling for all cases (.ogg, .mp3, none, other)
- Error code verification for each error condition
- File naming pattern validation

### Integration Test Requirements
- End-to-end conversion: text → OGG file
- File format verification (OGG container, Opus codec)
- Audio properties verification (16kHz, mono)
- WhatsApp compatibility verification

### Error Scenario Tests
- Missing text argument
- Empty/whitespace text
- Text exceeding 1000 characters
- Network unavailable (mock gTTS)
- ffmpeg not available
- No write permissions
- Invalid output path

## Versioning

**CLI Version**: 2.0.0
- Major version bump due to format change (MP3 → OGG)
- API remains compatible (same arguments)
- Breaking change: output file format only

**Changelog**:
```
2.0.0 (2026-03-03):
  - Changed output format from MP3 to OGG/Opus
  - Added automatic .ogg extension handling
  - Added ffmpeg dependency
  - Improved file size (30-50% reduction)
  - Maintained backward compatibility for CLI arguments

1.1.0 (2026-03-03):
  - Added -o/--output flag for custom file paths
  - Added automatic .mp3 extension handling

1.0.0 (2026-03-01):
  - Initial release with MP3 output
  - Basic TTS functionality with gTTS
```
