# Data Model: WhatsApp TTS Script

**Feature**: 002-whatsapp-tts-script  
**Date**: March 1, 2026  
**Purpose**: Define data entities and their relationships for the TTS script

## Overview

This CLI script processes text input and produces audio file output. The data model is intentionally simple, reflecting the straightforward nature of the tool.

## Entities

### 1. TextInput

Represents the user-provided text to be converted to speech.

**Attributes**:
- `content` (string): The actual text to convert (1-1000 characters)
- `length` (integer): Character count of the content
- `language` (string, optional): Detected or specified language (e.g., "en", "pt")

**Validation Rules**:
- `content` MUST NOT be empty
- `content` MUST NOT exceed 1000 characters
- `content` SHOULD handle Unicode characters (emojis, special characters)
- `language` defaults to auto-detection by gTTS if not specified

**State Transitions**:
```
[Raw Input] → [Validated] → [Processed by TTS]
```

**Example**:
```python
{
    "content": "Hello world",
    "length": 11,
    "language": "en"
}
```

---

### 2. AudioFile

Represents the generated audio file output.

**Attributes**:
- `file_path` (string): Absolute path to the generated audio file
- `file_name` (string): Name of the file (e.g., `tts_20260301_140530_a3f2b1c8.mp3`)
- `format` (string): Audio format, always "mp3"
- `file_size` (integer): File size in bytes
- `duration` (float): Audio duration in seconds
- `file_size` (integer): File size in bytes
- `created_at` (datetime): Timestamp when file was created

**Validation Rules**:
- `file_path` MUST be absolute POSIX path
- `file_name` MUST follow pattern: `tts_YYYYMMDD_HHMMSS_<hash>.mp3`
- `format` MUST be "mp3"
- File MUST be playable in WhatsApp
- `file_size` MUST be > 0

**State Transitions**:
```
[Not Exists] → [Generating] → [Created] → [Validated] → [Ready for Use]
```

**Example**:
```python
{
    "file_path": "/home/user/tts/output/tts_20260301_140530_a3f2b1c8.mp3",
    "file_name": "tts_20260301_140530_a3f2b1c8.mp3",
    "format": "mp3",
    "file_size": 24576,
    "file_size": 12480,
    "created_at": "2026-03-01T14:05:30Z"
}
```

---

### 3. ConversionJob

Represents the complete text-to-speech conversion operation (runtime entity, not persisted).

**Attributes**:
- `input` (TextInput): The text input being processed
- `output` (AudioFile, optional): The generated audio file (null until complete)
- `status` (enum): Current status of the conversion
- `error` (string, optional): Error message if conversion failed
- `started_at` (datetime): When conversion started
- `completed_at` (datetime, optional): When conversion completed
- `duration_ms` (integer, optional): Total processing time in milliseconds

**Status Values**:
- `PENDING`: Job created, not yet started
- `VALIDATING`: Validating input text
- `GENERATING_SPEECH`: Calling TTS API
- `SAVING_FILE`: Writing MP3 to disk
- `COMPLETED`: Successfully generated audio file
- `FAILED`: Conversion failed with error

**State Transitions**:
```
PENDING → VALIDATING → GENERATING_SPEECH → ENCODING_AUDIO → COMPLETED
                ↓              ↓                  ↓
              FAILED        FAILED            FAILED
```

**Example**:
```python
{
    "input": {
        "content": "Hello world",
        "length": 11,
        "language": "en"
    },
    "output": {
        "file_path": "/home/user/tts/output/tts_20260301_140530_a3f2b1c8.mp3",
        "file_name": "tts_20260301_140530_a3f2b1c8.mp3",
        ...
    },
    "status": "COMPLETED",
    "error": null,
    "started_at": "2026-03-01T14:05:28Z",
    "completed_at": "2026-03-01T14:05:30Z",
    "duration_ms": 2340
}
```

---

## Relationships

```
TextInput (1) ──── processes to ──── (1) AudioFile
                        │
                    managed by
                        │
                        ▼
                 ConversionJob
```

**Relationship Rules**:
- One TextInput produces exactly one AudioFile per conversion
- ConversionJob manages the relationship between input and output
- AudioFile exists independently after creation (no dependency on TextInput)

---

## Data Flow

```
1. User provides text via CLI
   ↓
2. TextInput entity created and validated
   ↓
3. ConversionJob created (status: PENDING)
   ↓
4. TTS generation (gTTS) produces MP3 audio
   ↓
5. MP3 audio written to file
   ↓
6. AudioFile entity created with metadata
   ↓
7. File path printed to stdout
   ↓
8. ConversionJob marked COMPLETED
```

---

## File System Structure

```
output/
├── tts_20260301_140530_a3f2b1c8.mp3
├── tts_20260301_140615_b7e9c2d1.mp3
└── tts_20260301_141020_f3a8d4e6.mp3
```

**Rules**:
- All audio files stored in `output/` directory
- Directory created automatically if not exists
- Files never overwritten (unique naming ensures this)
- No automatic cleanup (user manages old files)

---

## Error States

### Input Validation Errors
- Empty text → No entities created, exit immediately
- Text too long → TextInput created but validation fails
- Invalid characters → Handled by gTTS (most Unicode supported)

### Processing Errors
- Network failure → ConversionJob status: FAILED, no AudioFile created
- Encoding failure → ConversionJob status: FAILED, partial AudioFile may exist
- File system error → ConversionJob status: FAILED, AudioFile creation blocked

### Error Handling Strategy
- All errors logged to stderr
- Exit codes indicate error category (1-4)
- Partial files cleaned up on failure
- Clear error messages guide user to resolution

---

## Performance Characteristics

**Memory Usage**:
- TextInput: ~1-2 KB (text content)
- AudioFile: ~10-50 KB (typical 2-10 second audio)
- ConversionJob: ~1 KB (metadata only)
- Peak memory: ~5-10 MB during encoding

**Disk Usage**:
- Per audio file: ~5-20 KB (depends on duration)
- No persistent storage of TextInput or ConversionJob
- Only AudioFile persists to disk

**Processing Time** (per SC-001):
- Target: <10 seconds for 500 characters
- Typical: 2-5 seconds
- Bottleneck: Network latency (gTTS API)

---

## Assumptions

1. **Single-threaded execution**: No concurrent conversions
2. **No persistence layer**: No database, all state is runtime
3. **No caching**: Each conversion is independent
4. **No audio editing**: Direct TTS output, no post-processing
5. **No batch processing**: One text input per execution
6. **No user sessions**: Stateless operation
