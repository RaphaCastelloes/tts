# Research: OGG Output Option

**Feature**: 006-ogg-output-option  
**Date**: 2026-03-05

## Overview

Research findings for adding OGG format output option to the TTS skill. This feature will use pydub to convert MP3 audio to OGG format with Opus codec for WhatsApp compatibility.

## Decisions

### Decision 1: Audio Conversion Library
**What was chosen**: pydub  
**Rationale**: 
- Industry-standard Python library for audio manipulation
- Simple API for format conversion
- Supports MP3 to OGG conversion via ffmpeg backend
- Actively maintained and well-documented
- Minimal overhead and dependencies

**Alternatives considered**:
- **soundfile**: Requires libsndfile, less straightforward for MP3→OGG conversion
- **audioread**: Read-only library, doesn't support writing OGG files
- **Direct ffmpeg subprocess calls**: More complex, less Pythonic, harder to test
- **mutagen**: Focused on metadata, not format conversion

### Decision 2: OGG Codec for WhatsApp Compatibility
**What was chosen**: Opus codec in OGG container  
**Rationale**:
- WhatsApp requires Opus codec for voice messages
- Opus provides better compression than Vorbis at low bitrates
- Standard for voice/speech applications
- Supported by pydub via ffmpeg

**Alternatives considered**:
- **Vorbis codec**: Older, less efficient for voice content
- **PCM in OGG**: Uncompressed, file sizes too large
- **Speex**: Deprecated in favor of Opus

### Decision 3: Conversion Workflow
**What was chosen**: Generate MP3 first, then convert to OGG if requested  
**Rationale**:
- gTTS only outputs MP3 format
- Leverage existing MP3 generation code (no changes needed)
- Conversion step is fast (~100-500ms additional time)
- Allows caching MP3 if needed in future
- Clean separation of concerns

**Alternatives considered**:
- **Direct OGG generation from gTTS**: Not supported by gTTS library
- **Generate both formats always**: Wasteful, doubles file I/O
- **Use different TTS library for OGG**: Major rewrite, breaks backward compatibility

### Decision 4: File Extension Handling
**What was chosen**: Auto-correct extension to match format  
**Rationale**:
- Prevents user confusion (e.g., file.mp3 containing OGG data)
- More intuitive user experience
- Follows principle of least surprise
- Easy to implement with Path manipulation

**Alternatives considered**:
- **Respect user-specified extension**: Could create .mp3 files with OGG content (confusing)
- **Error on extension mismatch**: Too strict, poor UX
- **Warn but proceed**: Added complexity for minimal benefit

### Decision 5: Backward Compatibility Strategy
**What was chosen**: MP3 as default when --format not specified  
**Rationale**:
- Existing integrations expect MP3 output
- No breaking changes to current workflows
- Explicit opt-in for OGG format
- Aligns with "make the change easy, then make the easy change" principle

**Alternatives considered**:
- **OGG as default**: Would break existing integrations
- **Require explicit format always**: Breaking change, poor UX
- **Auto-detect based on context**: Too complex, fragile

### Decision 6: Dependency Version Pinning
**What was chosen**: Pin pydub to latest stable version with compatible ffmpeg  
**Rationale**:
- Ensures reproducible builds
- Prevents breaking changes from dependency updates
- Follows existing pattern in requirements.txt (gTTS==2.5.0)
- Easy to update when needed

**Alternatives considered**:
- **Unpinned versions**: Risk of breakage on updates
- **Upper bound only**: Still allows minor breaking changes
- **No version constraint**: High risk of incompatibilities

## Technical Notes

### pydub Usage Pattern
```python
from pydub import AudioSegment

# Load MP3
audio = AudioSegment.from_mp3("input.mp3")

# Export as OGG with Opus codec
audio.export("output.ogg", format="ogg", codec="libopus")
```

### ffmpeg System Dependency
- pydub requires ffmpeg for format conversion
- Oracle Linux: Install via `yum install ffmpeg` or use EPEL repository
- Must document in SKILL.md with installation instructions

### Error Handling Considerations
- Check for ffmpeg availability before conversion
- Graceful fallback if pydub import fails
- Clear error messages for missing dependencies
- Distinguish between format errors (exit code 1) and conversion errors (exit code 4)

### Performance Impact
- MP3 generation: 1-10 seconds (existing)
- OGG conversion: +100-500ms (negligible overhead)
- Total time for OGG: 1.1-10.5 seconds (within acceptable range)

## Implementation Notes

### Key Files to Modify
1. **tts.py**:
   - Add `--format` argument to argparse
   - Add `convert_to_ogg()` function
   - Update file extension logic
   - Add format validation

2. **requirements.txt**:
   - Add `pydub==0.25.1` (latest stable as of research)

3. **SKILL.md**:
   - Document `--format` option
   - Update workflow diagram (remove mp3-to-ogg step)
   - Add OGG usage examples
   - Document ffmpeg installation

4. **tests/**:
   - Test format argument parsing
   - Test OGG file generation and validity
   - Test backward compatibility
   - Test error handling

### Testing Strategy
- Unit tests: Format validation, argument parsing
- Integration tests: End-to-end OGG generation, file validity
- Regression tests: Ensure MP3 functionality unchanged
- Manual tests: WhatsApp playback verification

## Completion Status

✅ All research complete  
✅ Library chosen: pydub  
✅ Codec chosen: Opus in OGG  
✅ Workflow defined: MP3 → OGG conversion  
✅ Backward compatibility strategy: MP3 default  
✅ Ready for Phase 1 design
