# Research: WhatsApp TTS Script

**Feature**: 002-whatsapp-tts-script  
**Date**: March 1, 2026  
**Purpose**: Resolve technical unknowns and select appropriate libraries for TTS and audio encoding

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

### 2. Audio Encoding Library for Opus/OGG

**Question**: How to convert audio to Opus codec in OGG container format for WhatsApp compatibility?

**Options Evaluated**:

| Approach | Pros | Cons | ARM 64 Support |
|----------|------|------|----------------|
| **pydub + ffmpeg** | - Simple Python API<br>- Flexible format conversion<br>- Well documented | - Requires ffmpeg system dependency<br>- Additional installation step | ✅ Yes (ffmpeg available for ARM) |
| **opuslib** | - Direct Opus encoding<br>- Python bindings | - Requires libopus system library<br>- More complex API<br>- Need separate OGG muxing | ⚠️ Requires compilation |
| **subprocess + ffmpeg** | - Direct control<br>- No Python audio library needed | - Less Pythonic<br>- Error handling complexity | ✅ Yes |

**Decision**: **pydub with ffmpeg**

**Rationale**:
- Clean Python API that abstracts audio format conversion complexity
- ffmpeg is widely available in Oracle Linux repositories (installable via yum)
- Handles both Opus encoding and OGG container muxing in one step
- Well-tested and maintained library
- Simpler error handling compared to raw subprocess calls
- Aligns with Constitution Principle III (minimal but justified dependencies)

**Alternatives Considered**:
- **opuslib**: Rejected due to compilation requirements and complexity
- **subprocess + ffmpeg**: Rejected due to increased code complexity for error handling

### 3. Audio Format Workflow

**Question**: What is the complete workflow from text to WhatsApp-compatible audio?

**Decision**: Three-stage pipeline

**Workflow**:
```
1. Text Input → gTTS → MP3 audio (in-memory or temp file)
2. MP3 audio → pydub → Audio object
3. Audio object → pydub.export() → Opus/OGG file
```

**Rationale**:
- gTTS natively outputs MP3 format
- pydub can read MP3 and export to any format supported by ffmpeg
- Single conversion step minimizes quality loss
- Temporary file handling keeps disk usage minimal

**Technical Details**:
- Opus codec parameters for WhatsApp: 16kHz sample rate, mono channel (standard voice message format)
- OGG container with Opus codec is WhatsApp's native format
- File extension: `.ogg` (not `.opus`)

### 4. File Naming Strategy

**Question**: How to generate unique file names to avoid overwriting (FR-012)?

**Decision**: Timestamp-based naming with UUID fallback

**Format**: `tts_YYYYMMDD_HHMMSS_<hash>.ogg`

**Rationale**:
- Timestamp provides human-readable ordering
- Short hash (first 8 chars of UUID) ensures uniqueness
- Predictable format aids debugging
- Sortable by creation time

**Example**: `tts_20260301_140530_a3f2b1c8.ogg`

**Alternatives Considered**:
- Pure UUID: Rejected due to lack of human readability
- Sequential numbering: Rejected due to race condition risks

### 5. System Dependencies

**Question**: What system-level packages are required on Oracle Linux?

**Decision**: Minimal system dependencies

**Required Packages**:
```bash
# Oracle Linux installation commands
sudo yum install -y python3 python3-pip ffmpeg
```

**Rationale**:
- Python 3.8+ available in Oracle Linux repositories
- ffmpeg available in EPEL or Oracle Linux repos
- No compilation required
- All packages have ARM 64-bit builds

**Verification**:
- ffmpeg ARM 64-bit support confirmed in Oracle Linux 8/9
- Python 3.8+ standard in Oracle Linux 8+

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
   - ffmpeg not found → Exit code 4, message: "Error: ffmpeg not installed (run: sudo yum install ffmpeg)"
   - Encoding failure → Exit code 4, message: "Error: Audio encoding failed"

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
