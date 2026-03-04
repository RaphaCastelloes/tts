# Research: WhatsApp TTS Script

**Feature**: 002-whatsapp-tts-script  
**Date**: March 1, 2026  
**Purpose**: Resolve technical unknowns and select appropriate TTS library for MP3 generation

## Research Tasks

### 1. TTS Library Selection for Python

**Question**: Which TTS library should be used for text-to-speech conversion on Oracle Linux ARM 64-bit?

**Options Evaluated**:

| Library | Pros | Cons | ARM 64 Support |
|---------|------|------|----------------|
| **gTTS** | - Simple API<br>- No system dependencies<br>- Multi-language support<br>- Pure Python | - Requires internet connection<br>- Uses Google TTS API<br>- Network latency | ✅ Yes (pure Python) |
| **pyttsx3** | - Offline operation<br>- Cross-platform<br>- No internet required | - Requires system TTS engines (espeak, etc.)<br>- More complex setup<br>- System dependencies | ⚠️ Requires espeak on Linux |
| **TTS (Coqui)** | - High quality voices<br>- Offline<br>- Modern neural TTS | - Large model files<br>- Higher resource usage<br>- Complex setup | ⚠️ May have ARM compatibility issues |

**Decision**: **gTTS (Google Text-to-Speech)**

**Rationale**:
- Pure Python library with no compiled dependencies (guaranteed ARM 64-bit compatibility)
- Simple installation via pip with no system-level dependencies
- Multi-language support out of the box (supports Portuguese and English per FR requirements)
- Minimal code complexity aligns with Constitution Principle III (Minimal Dependencies)
- Proven reliability and active maintenance
- Trade-off: Requires internet connection, but this is acceptable for the use case

**Alternatives Considered**:
- **pyttsx3**: Rejected due to system dependency requirements (espeak) which complicates Oracle Linux setup
- **Coqui TTS**: Rejected due to complexity, large model sizes, and uncertain ARM 64-bit support

### 2. Audio Format Selection

**Question**: What audio format should be used for WhatsApp compatibility?

**Decision**: **MP3 (native gTTS output)**

**Rationale**:
- gTTS natively outputs MP3 format - no conversion needed
- MP3 is fully supported by WhatsApp on Android and iOS
- No additional dependencies required (no ffmpeg, no pydub)
- Simpler implementation with fewer points of failure
- Faster generation (no conversion step)
- Aligns with Constitution Principle III (minimal dependencies)

**Trade-offs**:
- MP3 files are slightly larger than Opus/OGG (acceptable for typical messages)
- No sample rate optimization (gTTS default is sufficient for voice)

### 3. Audio Format Workflow

**Question**: What is the complete workflow from text to WhatsApp-compatible audio?

**Decision**: Direct MP3 generation

**Workflow**:
```
1. Text Input → gTTS → MP3 audio (in-memory BytesIO)
2. MP3 audio → Write to file → output/tts_*.mp3
3. Print absolute file path to stdout
```

**Rationale**:
- Simplest possible workflow with minimal steps
- gTTS natively outputs MP3 - no conversion needed
- In-memory buffer avoids temporary files
- Direct file write minimizes I/O operations

**Technical Details**:
- MP3 format is universally supported by WhatsApp
- No special encoding parameters needed
- File extension: `.mp3`

### 4. File Naming Strategy

**Question**: How to generate unique file names to avoid overwriting (FR-012)?

**Decision**: Timestamp-based naming with UUID fallback

**Format**: `tts_YYYYMMDD_HHMMSS_<hash>.mp3`

**Rationale**:
- Timestamp provides human-readable ordering
- Short hash (first 8 chars of UUID) ensures uniqueness
- Predictable format aids debugging
- Sortable by creation time

**Example**: `tts_20260301_140530_a3f2b1c8.mp3`

**Alternatives Considered**:
- Pure UUID: Rejected due to lack of human readability
- Sequential numbering: Rejected due to race condition risks

### 5. System Dependencies

**Question**: What system-level packages are required on Oracle Linux?

**Decision**: Minimal system dependencies

**Required Packages**:
```bash
# Oracle Linux installation commands
sudo yum install -y python3 python3-pip
```

**Rationale**:
- Python 3.8+ available in Oracle Linux repositories
- No system dependencies required beyond Python
- Pure Python solution - no compilation needed
- All packages have ARM 64-bit builds

**Verification**:
- Python 3.8+ standard in Oracle Linux 8+
- No additional system packages required

### 6. Error Handling Strategy

**Question**: What error scenarios need handling per Constitution Principle IV?

**Decision**: Comprehensive error handling with clear messages

**Error Categories**:

1. **Input Validation Errors**:
   - Empty or missing text argument → Exit code 1, message: "Error: No text provided"
   - Text too long (>1000 chars) → Exit code 1, message: "Error: Text exceeds maximum length"

2. **Network Errors** (gTTS):
   - No internet connection → Exit code 2, message: "Error: Cannot connect to TTS service"
   - API rate limiting → Exit code 2, message: "Error: TTS service temporarily unavailable"

3. **File System Errors**:
   - No write permission → Exit code 3, message: "Error: Cannot write to output directory"
   - Disk full → Exit code 3, message: "Error: Insufficient disk space"

4. **Audio Processing Errors**:
   - TTS generation failure → Exit code 4, message: "Error: Audio processing failed"
   - File write failure → Exit code 4, message: "Error: Cannot save audio file"

**Rationale**:
- Distinct exit codes enable programmatic error detection
- Clear messages guide user to resolution
- Follows Constitution Principle IV (Error Handling & Observability)

### 7. Performance Considerations

**Question**: Can we meet the <10 second performance goal (SC-001)?

**Decision**: Yes, with expected performance breakdown

**Performance Analysis**:
- gTTS API call: 1-3 seconds (network dependent)
- Audio download: 0.5-1 second
- Opus encoding: 0.5-1 second
- File I/O: <0.1 second
- **Total estimated**: 2-5 seconds for typical 500-character input

**Optimizations**:
- Use in-memory buffers where possible (avoid temp file I/O)
- Stream audio data directly from gTTS to pydub
- No unnecessary audio processing steps

**Rationale**:
- Well within 10-second target
- Network latency is primary variable
- ARM 64-bit performance adequate for audio encoding

## Technology Stack Summary

### Python Dependencies (requirements.txt)
```
gTTS==2.5.0          # Text-to-speech conversion
pydub==0.25.1        # Audio format conversion
```

### System Dependencies
```
ffmpeg               # Audio codec support (Opus/OGG)
python3 (>=3.8)      # Runtime environment
```

### Justification per Constitution Principle III
- **gTTS**: Required for text-to-speech conversion (core functionality)
- **pydub**: Required for Opus/OGG encoding (WhatsApp compatibility requirement)
- **ffmpeg**: Required by pydub for codec support (no pure-Python alternative exists)

All dependencies are:
- Minimal (only 2 Python packages)
- Well-maintained and widely used
- ARM 64-bit compatible
- Installable via standard package managers

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Internet dependency for gTTS | High (offline usage blocked) | Document requirement clearly; consider offline TTS as future enhancement |
| ffmpeg not in default repos | Medium (installation friction) | Provide clear installation instructions with EPEL repo setup |
| Google TTS API changes | Low (API stability) | Pin gTTS version; monitor for deprecation notices |
| ARM 64-bit compatibility issues | Low (all deps confirmed) | Test on actual Oracle Linux ARM environment |

## Next Steps (Phase 1)

1. Create data-model.md defining audio file and text input entities
2. Create contracts/ defining CLI interface contract
3. Create quickstart.md with installation and usage instructions
4. Update agent context with selected technologies
