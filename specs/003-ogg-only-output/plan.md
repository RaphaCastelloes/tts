# Implementation Plan: OGG-Only Audio Output

**Branch**: `003-ogg-only-output` | **Date**: March 3, 2026 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-ogg-only-output/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Change the WhatsApp TTS script to output audio files exclusively in OGG/Opus format instead of MP3. This involves adding audio conversion from gTTS MP3 output to OGG container with Opus codec at 16kHz mono (WhatsApp standard). The change provides 30-50% file size reduction while maintaining full backward compatibility with existing command-line arguments and file naming conventions.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.8+ (Oracle Linux compatible)
**Primary Dependencies**: gTTS 2.5.0 (TTS), pydub 0.25.1 (audio conversion), ffmpeg (system dependency for Opus encoding)
**Storage**: Local file system (audio output files in `output/` directory)
**Testing**: pytest 7.4.3
**Target Platform**: Oracle Linux ARM 64-bit
**Project Type**: CLI script
**Performance Goals**: Generate audio in <10 seconds for typical messages (up to 500 characters)
**Constraints**: Headless execution (no GUI), ARM 64-bit compatible dependencies, WhatsApp audio format compliance (OGG/Opus, 16kHz, mono), Internet connection required (gTTS API)
**Scale/Scope**: Single-user command-line tool, processes 1-1000 character text inputs

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Skill-Centric Architecture
✅ **PASS** - Modifies existing tts.py script to add OGG conversion, SKILL.md will be updated

### Principle II: Text I/O Protocol  
✅ **PASS** - Maintains CLI with text I/O (stdin/stdout/stderr), no GUI dependencies

### Principle III: Minimal Dependencies
⚠️ **NEEDS JUSTIFICATION** - Adding 2 new dependencies (pydub, ffmpeg)
- **pydub 0.25.1**: Required for MP3→OGG/Opus conversion (no pure-Python alternative for Opus)
- **ffmpeg**: System dependency required by pydub for Opus codec encoding
- **Rationale**: OGG/Opus format requirement necessitates audio encoding beyond gTTS capabilities. pydub is the standard Python library for this, and ffmpeg provides Opus codec support.

### Principle IV: Error Handling & Observability
✅ **PASS** - Will add error handling for conversion failures, ffmpeg availability checks

### Principle V: Test-First Development
✅ **PASS** - Will add tests for OGG format validation, conversion process, error cases

### Platform & Runtime Constraints
✅ **PASS** - ffmpeg available via Oracle Linux yum repositories, all dependencies Oracle Linux compatible

**Overall Gate Status**: ✅ **PASS** (with justified dependency additions)

---

### Post-Phase 1 Re-evaluation

*After completing research.md, data-model.md, contracts/, and quickstart.md*

#### Principle I: Skill-Centric Architecture
✅ **PASS** - Single tts.py script with OGG conversion logic, comprehensive SKILL.md documentation planned

#### Principle II: Text I/O Protocol
✅ **PASS** - CLI maintained with text I/O, no GUI, all interaction via stdin/stdout/stderr

#### Principle III: Minimal Dependencies
✅ **PASS (JUSTIFIED)** - Dependencies remain justified:
- pydub: Only Python library supporting OGG/Opus conversion
- ffmpeg: Required by pydub for Opus codec, available via Oracle Linux yum
- No pure-Python alternatives exist for Opus encoding

#### Principle IV: Error Handling & Observability
✅ **PASS** - Design includes:
- ffmpeg availability check before conversion
- Clear error messages for encoding failures
- Exit code 4 for processing errors
- Structured error handling throughout conversion pipeline

#### Principle V: Test-First Development
✅ **PASS** - Testing strategy defined:
- OGG format validation tests
- Audio properties tests (16kHz, mono, Opus codec)
- Conversion pipeline tests
- Error scenario tests (ffmpeg missing, encoding failures)

#### Platform & Runtime Constraints
✅ **PASS** - Oracle Linux compatibility verified:
- ffmpeg available in EPEL repositories for Oracle Linux ARM64
- pydub compatible with Oracle Linux
- All dependencies ARM64 compatible
- Installation instructions documented in quickstart.md

**Final Gate Status**: ✅ **PASS** - All constitutional principles satisfied with proper justifications

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
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
tts/
├── tts.py                    # Main script (OGG conversion logic added)
├── SKILL.md                  # Documentation (updated for OGG format)
├── requirements.txt          # Dependencies (pydub added)
├── README.md                 # Quick start guide (updated)
└── output/                   # Generated OGG files
    └── tts_*.ogg

tests/
├── test_tts.py              # Unit tests (OGG validation added)
├── test_audio_format.py     # Format tests (OGG/Opus checks added)
└── test_integration.py      # Integration tests (updated)

specs/003-ogg-only-output/
├── spec.md
├── plan.md                  # This file
├── research.md              # Audio encoding research
├── data-model.md            # AudioFile entity updates
├── contracts/
│   └── cli-interface.md     # CLI contract updates
└── tasks.md                 # Implementation tasks
```

**Structure Decision**: Single-script CLI tool (existing structure). Only tts.py and documentation files are modified. No new source directories needed.

## Complexity Tracking

| Dependency Addition | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| pydub + ffmpeg | OGG/Opus encoding not available in pure Python | gTTS only outputs MP3; no pure-Python Opus encoder exists; pydub is industry standard for Python audio processing |
| ffmpeg system dependency | Required by pydub for Opus codec | Opus encoding requires native codec libraries; ffmpeg is standard on Oracle Linux |
