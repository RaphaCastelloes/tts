# Data Model: OGG-Only Audio Output

**Feature**: 003-ogg-only-output
**Date**: March 3, 2026
**Purpose**: Define data entities and their relationships for OGG audio generation

## Entities

### 1. TextInput

Represents the text input to be converted to speech.

**Attributes**:
- `text` (string): The input text to convert to speech
- `length` (integer): Character count of the text
- `encoding` (string): Character encoding, always "UTF-8"
- `timestamp` (datetime): When the input was received

**Validation Rules**:
- `text` MUST NOT be empty or whitespace-only
- `length` MUST be between 1 and 1000 characters (inclusive)
- `text` MUST be valid UTF-8 encoded string
- Special characters (emojis, accents, punctuation) are allowed

**Example**:
```python
{
    "text": "Olá, como você está?",
    "length": 20,
    "encoding": "UTF-8",
    "timestamp": "2026-03-03T22:10:00Z"
}
```

### 2. AudioFile

Represents the generated OGG audio file output.

**Attributes**:
- `file_path` (string): Absolute path to the generated audio file
- `file_name` (string): Name of the file (e.g., `tts_20260303_221000_a3f2b1c8.ogg`)
- `format` (string): Audio format, always "ogg"
- `codec` (string): Audio codec, always "opus"
- `sample_rate` (integer): Sample rate in Hz, always 16000
- `channels` (integer): Number of audio channels, always 1 (mono)
- `file_size` (integer): File size in bytes
- `duration` (float): Audio duration in seconds
- `created_at` (datetime): Timestamp when file was created

**Validation Rules**:
- `file_path` MUST be absolute path
- `file_name` MUST match pattern `tts_YYYYMMDD_HHMMSS_<hash>.ogg`
- `format` MUST be "ogg"
- `codec` MUST be "opus"
- `sample_rate` MUST be 16000
- `channels` MUST be 1
- `file_size` MUST be > 0 bytes
- `duration` MUST be > 0 seconds
- File MUST exist at `file_path`

**Example**:
```python
{
    "file_path": "/home/user/tts/output/tts_20260303_221000_a3f2b1c8.ogg",
    "file_name": "tts_20260303_221000_a3f2b1c8.ogg",
    "format": "ogg",
    "codec": "opus",
    "sample_rate": 16000,
    "channels": 1,
    "file_size": 15432,
    "duration": 2.5,
    "created_at": "2026-03-03T22:10:02Z"
}
```

### 3. ConversionJob

Represents the process of converting text to OGG audio.

**Attributes**:
- `job_id` (string): Unique identifier (hash from filename)
- `text_input` (TextInput): Reference to input text entity
- `audio_file` (AudioFile): Reference to output audio file entity (null until complete)
- `state` (enum): Current state of the conversion job
- `error_message` (string): Error description if state is FAILED (null otherwise)
- `started_at` (datetime): When conversion started
- `completed_at` (datetime): When conversion finished (null if not complete)

**State Transitions**:
```
VALIDATING_INPUT → Input validation in progress
    ↓ (valid)
GENERATING_TTS → Calling gTTS API to generate MP3
    ↓ (success)
LOADING_AUDIO → Loading MP3 into pydub AudioSegment
    ↓ (success)
CONVERTING_FORMAT → Converting to mono 16kHz
    ↓ (success)
ENCODING_AUDIO → Encoding to OGG/Opus via ffmpeg
    ↓ (success)
SAVING_FILE → Writing OGG file to disk
    ↓ (success)
COMPLETE → Audio file successfully generated
    ↓ (on any error)
FAILED → Conversion failed with error

State Flow:
VALIDATING_INPUT → GENERATING_TTS → LOADING_AUDIO → CONVERTING_FORMAT → ENCODING_AUDIO → SAVING_FILE → COMPLETE
                     ↓                   ↓                  ↓                  ↓               ↓
                   FAILED              FAILED            FAILED            FAILED          FAILED
```

**Error States**:
- `FAILED` with `error_message` = "Invalid input: {reason}" (exit code 1)
- `FAILED` with `error_message` = "Network error: {reason}" (exit code 2)
- `FAILED` with `error_message` = "Filesystem error: {reason}" (exit code 3)
- `FAILED` with `error_message` = "Encoding error: {reason}" (exit code 4)

**Example**:
```python
{
    "job_id": "a3f2b1c8",
    "text_input": { ... },
    "audio_file": { ... },
    "state": "COMPLETE",
    "error_message": null,
    "started_at": "2026-03-03T22:10:00Z",
    "completed_at": "2026-03-03T22:10:02Z"
}
```

## Relationships

```
TextInput (1) ←──────→ (1) ConversionJob
ConversionJob (1) ───→ (0..1) AudioFile

One TextInput creates one ConversionJob
One ConversionJob produces zero or one AudioFile (zero if failed)
```

## Data Flow

```
1. User Input
   ↓
2. TextInput entity created and validated
   ↓
3. ConversionJob created (state: VALIDATING_INPUT)
   ↓
4. State: GENERATING_TTS → Call gTTS API
   ↓
5. State: LOADING_AUDIO → Load MP3 into pydub
   ↓
6. State: CONVERTING_FORMAT → Convert to mono 16kHz
   ↓
7. State: ENCODING_AUDIO → Encode to OGG/Opus
   ↓
8. State: SAVING_FILE → Write to disk
   ↓
9. AudioFile entity created
   ↓
10. State: COMPLETE → Print file path to stdout
```

## File System Structure

```
tts/
└── output/
    ├── tts_20260303_221000_a3f2b1c8.ogg  (AudioFile)
    ├── tts_20260303_221015_b7e9c2d1.ogg  (AudioFile)
    └── tts_20260303_221020_f3a8d4e6.ogg  (AudioFile)
```

**Rules**:
- All files stored in `output/` directory (relative to script location)
- Files never overwritten (unique timestamp + hash guarantee)
- No temp files (MP3 kept in memory)
- No cleanup needed (files persist indefinitely)

## Error States

### Input Validation Errors (Exit Code 1)
- Empty or whitespace-only text
- Text exceeds 1000 characters
- Invalid UTF-8 encoding

### Network Errors (Exit Code 2)
- gTTS API unreachable
- Network timeout
- TLS/SSL errors

### Filesystem Errors (Exit Code 3)
- Cannot create output directory
- No write permissions
- Disk full
- Invalid custom output path

### Processing Errors (Exit Code 4)
- ffmpeg not installed
- Audio encoding failed
- pydub conversion error
- Invalid audio data from gTTS

## Performance Characteristics

**Memory Usage**:
- TextInput: <1 KB (text string)
- MP3 bytes (in-memory): 50-200 KB
- AudioSegment (pydub): 1-5 MB (uncompressed audio in RAM)
- AudioFile (OGG): 15-75 KB (30-50% smaller than MP3)

**Processing Time** (typical 500-character message):
- Input validation: <10ms
- TTS generation (gTTS): 1-3 seconds (network-dependent)
- Audio loading: <100ms
- Format conversion: <200ms
- OGG encoding: <500ms
- File I/O: <50ms
- **Total**: 2-4 seconds (well under 10-second target)

**Storage**:
- Average voice message: ~30 KB OGG (vs ~50 KB MP3)
- 30-50% space savings compared to MP3
- 100 messages: ~3 MB
- 1000 messages: ~30 MB

## Assumptions

1. **Network Availability**: Internet connection required for gTTS API
2. **System Dependencies**: ffmpeg installed and in system PATH
3. **File Permissions**: Write access to output directory
4. **Disk Space**: Sufficient space for generated OGG files
5. **Python Version**: Python 3.8+ with required packages installed
6. **Platform**: Oracle Linux ARM64 or compatible
7. **Locale**: UTF-8 locale for proper text encoding
8. **gTTS Service**: Google TTS API available and responsive
9. **Opus Codec**: libopus available via ffmpeg
10. **Concurrent Access**: Single-user tool, no concurrent job handling needed
