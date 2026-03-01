# Implementation Plan: WhatsApp TTS Script

**Branch**: `002-whatsapp-tts-script` | **Date**: March 1, 2026 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-whatsapp-tts-script/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Create a command-line Python script that converts text to speech and outputs WhatsApp-compatible audio files in Opus/OGG format. The script accepts text as a command-line argument, generates the audio file, and prints the absolute file path to the terminal. Must run on Linux Oracle 10 ARM 64-bit architecture.

## Technical Context

**Language/Version**: Python 3.8+ (Oracle Linux compatible)  
**Primary Dependencies**: gTTS 2.5.0 (text-to-speech), pydub 0.25.1 (audio format conversion)  
**Storage**: Local file system (audio output files in `output/` directory)  
**Testing**: pytest  
**Target Platform**: Linux Oracle 10 ARM 64-bit
**Project Type**: CLI script  
**Performance Goals**: Generate audio in <10 seconds for typical messages (up to 500 characters)  
**Constraints**: Headless execution (no GUI), ARM 64-bit compatible dependencies, WhatsApp audio format compliance (Opus codec in OGG container), Internet connection required (gTTS API)  
**Scale/Scope**: Single-user command-line tool, processes 1-1000 character text inputs
**System Dependencies**: ffmpeg (for Opus/OGG encoding via pydub)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Skill-Centric Architecture
- ✅ **PASS**: Single tts.py script with SKILL.md documentation
- ✅ **PASS**: Self-contained functionality (text-to-speech conversion)
- ✅ **PASS**: Clear inputs (command-line text) and outputs (audio file path)

### Principle II: Text I/O Protocol
- ✅ **PASS**: Command-line argument input (`python tts.py "text"`)
- ✅ **PASS**: Stdout output (file path printing)
- ✅ **PASS**: Stderr for errors/logs
- ✅ **PASS**: No GUI dependencies

### Principle III: Minimal Dependencies
- ✅ **PASS**: Only 2 Python dependencies (gTTS, pydub) + 1 system dependency (ffmpeg)
- ✅ **PASS**: All dependencies justified in research.md
- ✅ **PASS**: ARM 64-bit compatibility verified (pure Python + ffmpeg ARM support confirmed)

### Principle IV: Error Handling & Observability
- ✅ **PASS**: Error handling required (FR-011: clear error messages)
- ✅ **PASS**: Exit codes planned (0 for success, non-zero for errors)
- ✅ **PASS**: Input validation required (empty text, special characters)

### Principle V: Test-First Development
- ✅ **PASS**: Unit tests required before implementation
- ✅ **PASS**: Integration tests for audio generation
- ✅ **PASS**: Edge case testing (FR requirements cover this)

### Platform & Runtime Constraints
- ✅ **PASS**: Target platform is Oracle Linux (specified in requirements)
- ✅ **PASS**: Python 3.8+ compatible
- ✅ **PASS**: Headless execution (no GUI)
- ✅ **PASS**: System dependencies identified (ffmpeg, installable via yum)
- ✅ **PASS**: POSIX file paths (Linux environment)

**Overall Status (Initial)**: CONDITIONAL PASS - Proceed to Phase 0 to resolve dependency clarifications

---

## Constitution Check Re-evaluation (Post-Phase 1)

*Re-checked after Phase 1 design completion*

### Final Status: ✅ **FULL PASS**

All constitutional principles are satisfied:

1. **Skill-Centric Architecture**: Single tts.py script with comprehensive SKILL.md documentation
2. **Text I/O Protocol**: Pure CLI with stdin/stdout/stderr, no GUI dependencies
3. **Minimal Dependencies**: Only 2 Python packages + 1 system package, all justified and ARM-compatible
4. **Error Handling**: Comprehensive error handling with 4 distinct exit codes and clear messages
5. **Test-First Development**: Test structure defined, ready for TDD implementation
6. **Platform Constraints**: Oracle Linux compatible, Python 3.8+, headless execution verified

**Design artifacts complete**:
- ✅ research.md: All technical decisions documented with rationale
- ✅ data-model.md: Entities and relationships defined
- ✅ contracts/cli-interface.md: CLI contract fully specified
- ✅ quickstart.md: Installation and usage guide complete

**Ready for Phase 2**: Proceed to `/speckit.tasks` to generate implementation tasks

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
# Simple CLI script structure
tts.py              # Main executable script
SKILL.md            # Skill documentation
requirements.txt    # Python dependencies

tests/
├── test_tts.py           # Unit tests for TTS functionality
├── test_audio_format.py  # Audio format validation tests
└── test_integration.py   # End-to-end integration tests

output/             # Directory for generated audio files (gitignored)
```

**Structure Decision**: Single-file CLI script structure. This is a simple command-line tool with no need for complex module organization. The tts.py script contains all functionality, following the Skill-Centric Architecture principle. Tests are organized by concern (unit, format validation, integration).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
