# Research: OGG-Only Audio Output

**Feature**: 003-ogg-only-output
**Date**: March 3, 2026
**Purpose**: Resolve technical decisions for converting TTS output from MP3 to OGG/Opus format

## Research Questions

### 1. Audio Encoding Library for OGG/Opus

**Question**: Which Python library should be used to convert gTTS MP3 output to OGG/Opus format?

**Decision**: **pydub 0.25.1**

**Rationale**:
- Industry-standard Python library for audio manipulation
- Supports OGG container with Opus codec via ffmpeg backend
- Simple API for format conversion: `AudioSegment.from_mp3()` → `export(format='ogg', codec='libopus')`
- Well-maintained with 7.5k+ GitHub stars, active development
- Oracle Linux ARM64 compatible (pure Python with native dependency on ffmpeg)

**Alternatives Considered**:
- **soundfile**: Requires libsndfile, doesn't support Opus codec natively
- **audioread**: Read-only library, cannot encode OGG/Opus
- **pyrubberband**: Focused on pitch/tempo manipulation, not format conversion
- **Pure Python Opus encoder**: Does not exist (Opus is a complex codec requiring native libraries)

**Technical Details**:
```python
from pydub import AudioSegment

# Load MP3 from gTTS
audio = AudioSegment.from_mp3(mp3_bytes)

# Convert to mono and set sample rate
audio = audio.set_channels(1)
audio = audio.set_frame_rate(16000)

# Export as OGG/Opus
audio.export(output_path, format='ogg', codec='libopus', parameters=["-strict", "-2"])
```

### 2. OGG/Opus Format Specifications

**Question**: What are the exact audio specifications required for WhatsApp compatibility?

**Decision**: **OGG container, Opus codec, 16kHz sample rate, mono channel**

**Rationale**:
- WhatsApp officially supports Opus codec in OGG container
- 16kHz sample rate is WhatsApp's standard for voice messages (optimal for speech)
- Mono channel reduces file size and is sufficient for voice content
- Opus provides superior compression to MP3 for speech (30-50% smaller files)

**WhatsApp Audio Specifications**:
- **Container**: OGG (Ogg Vorbis container format)
- **Codec**: Opus (open-source audio codec designed for internet streaming)
- **Sample Rate**: 16000 Hz (16 kHz)
- **Channels**: 1 (mono)
- **Bit Rate**: Variable (Opus adapts automatically, typically 24-32 kbps for speech)
- **File Extension**: `.ogg`

**Compatibility**:
- ✅ WhatsApp Android: Full support
- ✅ WhatsApp iOS: Full support
- ✅ WhatsApp Web: Full support
- ✅ WhatsApp Desktop: Full support

### 3. System Dependencies - ffmpeg

**Question**: How should ffmpeg be installed and configured on Oracle Linux ARM64?

**Decision**: **Use system package manager (yum/dnf) to install ffmpeg**

**Rationale**:
- ffmpeg is available in Oracle Linux repositories (EPEL may be required)
- ARM64 builds are available and tested
- System package manager ensures proper dependency resolution
- Automatic security updates via yum

**Installation**:
```bash
# Enable EPEL repository if needed
sudo yum install -y epel-release

# Install ffmpeg
sudo yum install -y ffmpeg

# Verify installation
ffmpeg -version
```

**Version Requirements**:
- Minimum: ffmpeg 3.0+ (for Opus codec support)
- Recommended: ffmpeg 4.0+ (better Opus encoding)
- Oracle Linux 8/9 typically provides ffmpeg 4.2+

**Error Handling**:
- Script must check for ffmpeg availability before attempting conversion
- Provide clear installation instructions in error messages
- Exit with code 4 (EXIT_PROCESSING_ERROR) if ffmpeg not found

### 4. Audio Conversion Workflow

**Question**: What is the complete workflow for converting gTTS MP3 to OGG/Opus?

**Decision**: **Multi-step conversion pipeline**

**Workflow**:
```
1. Generate TTS (gTTS) → MP3 bytes in memory (BytesIO)
2. Load MP3 → AudioSegment object (pydub)
3. Convert to mono → AudioSegment.set_channels(1)
4. Set sample rate → AudioSegment.set_frame_rate(16000)
5. Export to OGG/Opus → audio.export(path, format='ogg', codec='libopus')
6. Validate output → Check file exists and size > 0
7. Return file path → Print absolute path to stdout
```

**Memory Efficiency**:
- MP3 from gTTS kept in BytesIO (no temp file)
- pydub processes in-memory where possible
- Only final OGG written to disk
- Expected memory usage: ~2-5 MB for typical voice message

**Performance**:
- TTS generation: 1-3 seconds (network-dependent)
- Audio conversion: <1 second for typical messages
- Total time: <10 seconds target (met with headroom)

### 5. File Naming and Extension Handling

**Question**: How should file extensions be handled when switching from MP3 to OGG?

**Decision**: **Auto-replace extension, maintain naming pattern**

**Rationale**:
- Existing pattern: `tts_YYYYMMDD_HHMMSS_<hash>.mp3`
- New pattern: `tts_YYYYMMDD_HHMMSS_<hash>.ogg`
- Preserves automation compatibility (only extension changes)
- Custom paths: replace `.mp3` with `.ogg`, add `.ogg` if missing

**Extension Logic**:
```python
# Default naming
filename = f"tts_{timestamp}_{hash}.ogg"

# Custom path handling
if custom_path.suffix == '.mp3':
    custom_path = custom_path.with_suffix('.ogg')
elif custom_path.suffix == '':
    custom_path = custom_path.with_suffix('.ogg')
# Keep .ogg if already specified
```

### 6. Backward Compatibility

**Question**: How to maintain compatibility with existing command-line arguments?

**Decision**: **Full backward compatibility, only format changes**

**Preserved Features**:
- ✅ Command-line argument parsing (argparse)
- ✅ `-o` / `--output` custom path support
- ✅ Input validation (1-1000 characters)
- ✅ Error codes (0-4)
- ✅ Output directory creation
- ✅ Unique filename generation

**Breaking Changes**:
- ❌ None - all existing functionality preserved
- ℹ️ Only change: output file extension .mp3 → .ogg

### 7. Error Scenarios and Handling

**Question**: What new error conditions are introduced by OGG conversion?

**Decision**: **Add ffmpeg availability check, conversion error handling**

**New Error Conditions**:

1. **ffmpeg not installed**:
   - Detection: Try subprocess or check pydub error message
   - Message: "Error: ffmpeg not installed. Run: sudo yum install ffmpeg"
   - Exit Code: 4 (EXIT_PROCESSING_ERROR)

2. **Audio conversion failure**:
   - Detection: Exception from pydub.export()
   - Message: "Error: Audio encoding failed. Check ffmpeg installation."
   - Exit Code: 4 (EXIT_PROCESSING_ERROR)

3. **Invalid audio data**:
   - Detection: pydub unable to load MP3
   - Message: "Error: TTS service temporarily unavailable. Please try again later."
   - Exit Code: 2 (EXIT_NETWORK_ERROR)

**Existing Error Handling** (preserved):
- Empty text input
- Text too long (>1000 chars)
- Network errors (gTTS API)
- Filesystem errors (permissions)

## Summary

### Technology Stack
- **TTS Library**: gTTS 2.5.0 (unchanged)
- **Audio Processing**: pydub 0.25.1 (new)
- **Audio Codec**: ffmpeg with libopus (new system dependency)
- **Testing**: pytest 7.4.3 (unchanged)

### Key Decisions
1. Use pydub for audio conversion (industry standard, well-supported)
2. Target OGG/Opus format: 16kHz mono (WhatsApp standard)
3. Install ffmpeg via yum on Oracle Linux (standard approach)
4. Maintain full backward compatibility (only extension changes)
5. Add ffmpeg availability check with clear error messages

### Implementation Impact
- **Dependencies**: +2 (pydub, ffmpeg)
- **Code Changes**: Moderate (add conversion function, update tests)
- **Documentation**: Moderate (update SKILL.md, README.md for OGG format)
- **Performance**: Negligible impact (<1s conversion time)
- **Compatibility**: 100% maintained (no breaking changes)

## Next Steps

Phase 1 will define:
- Updated AudioFile entity (OGG-specific attributes)
- CLI interface contract updates (OGG output examples)
- Integration quickstart guide
