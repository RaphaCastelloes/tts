# Implementation Plan: OGG Output Option

**Branch**: `006-ogg-output-option` | **Date**: 2026-03-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-ogg-output-option/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Add `--format` command-line option to the TTS skill to enable direct OGG audio generation, eliminating the need for a separate mp3-to-ogg conversion step in the WhatsApp bot workflow. The feature will:
- Accept `--format mp3` or `--format ogg` argument
- Default to MP3 when no format specified (backward compatibility)
- Use pydub library to convert MP3 to OGG (Opus codec)
- Auto-append correct file extension based on format
- Maintain all existing functionality (language selection, custom paths, validation)

This consolidates the workflow from 6 steps to 5 steps while maintaining 100% backward compatibility.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.8+  
**Primary Dependencies**: gTTS 2.5.0 (existing), pydub (new), ffmpeg (system dependency)  
**Storage**: File system (output/ directory for generated audio files)  
**Testing**: pytest 7.4.3 (existing test framework)  
**Target Platform**: Oracle Linux (as per constitution)
**Project Type**: CLI tool / skill  
**Performance Goals**: Same as MP3 generation (1-10 seconds for 1-1000 character text)  
**Constraints**: Must maintain backward compatibility, WhatsApp OGG compatibility (Opus codec), same text length limit (1000 chars)  
**Scale/Scope**: Single Python script enhancement (tts.py), add format conversion logic, update argument parser

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: Skill-Centric Architecture ✅
- Feature enhances existing tts.py skill with new format option
- SKILL.md will be updated to document new --format parameter
- No new separate skills introduced (consolidates functionality)
- Dependencies will be documented in requirements.txt and SKILL.md

### Gate 2: Text I/O Protocol ✅
- Maintains command-line argument input via argparse
- Output remains stdout (file path) and stderr (errors)
- No GUI or interactive prompts added
- Text-based interface preserved

### Gate 3: Minimal Dependencies ✅
- New dependency: pydub (lightweight audio manipulation library)
- System dependency: ffmpeg (required by pydub for OGG conversion)
- Both dependencies justified: pydub is industry standard for audio format conversion, ffmpeg widely available
- Will be added to requirements.txt with version pinning

### Gate 4: Error Handling & Observability ✅
- Will add validation for --format argument
- Clear error messages for invalid formats
- Proper exit codes (1 for input errors, 4 for conversion errors)
- Error handling for pydub/ffmpeg failures

### Gate 5: Test-First Development ✅
- Will write tests before implementation:
  - Test format argument parsing
  - Test OGG file generation
  - Test backward compatibility (default MP3)
  - Test error handling for invalid formats
  - Test extension auto-correction
- Integration tests for OGG playback validation

**Result**: All gates passed. Feature aligns with constitutional principles.

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
├── tts.py                    # Main script - ADD format conversion logic
├── SKILL.md                  # UPDATE with --format documentation
├── requirements.txt          # ADD pydub dependency
├── tests/                    # ADD new tests for format option
│   ├── test_tts.py          # UPDATE with format tests
│   ├── test_audio_format.py # ADD OGG format validation tests
│   └── test_integration.py  # UPDATE with OGG integration tests
└── output/                   # Generated audio files (.mp3 and .ogg)
```

**Structure Decision**: Single project structure. This is an enhancement to the existing tts.py CLI tool. Changes are localized to:
1. **tts.py**: Add argparse --format option, add OGG conversion function using pydub
2. **requirements.txt**: Add pydub dependency
3. **tests/**: Add tests for new format functionality
4. **SKILL.md**: Update documentation with new --format option and simplified workflow

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

N/A - No constitutional violations. This feature:
- Adds minimal dependencies (pydub + ffmpeg) which are standard and justified
- Maintains single-script architecture
- Preserves text I/O protocol
- Includes comprehensive testing
- Updates documentation atomically with code
