# Implementation Plan: Reorganize Scripts and Unify Documentation

**Branch**: `007-reorganize-scripts` | **Date**: 2026-03-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/007-reorganize-scripts/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Reorganize the TTS skill project structure to follow Python conventions by:
- Creating a `/scripts` directory and moving all executable Python files into it (tts.py, convert_mp3_to_ogg.py)
- Unifying documentation by merging README.md quick start content into SKILL.md
- Simplifying README.md to a brief overview with link to SKILL.md
- Removing the obsolete `/mp3-to-ogg` folder (functionality now integrated in tts.py via `--format ogg`)
- Updating all documentation references to use new paths (`scripts/tts.py`)
- Using `git mv` to preserve file history and traceability

This is a pure refactoring task with no functional code changes—only file reorganization and documentation consolidation.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.8+ (no code changes)
**Primary Dependencies**: None (refactoring only—uses existing gTTS, pydub, pytest)
**Storage**: File system (no changes to storage)
**Testing**: pytest 7.4.3 (existing tests must continue to pass)
**Target Platform**: Oracle Linux (as per constitution)
**Project Type**: CLI tool / skill (no change to type)
**Performance Goals**: N/A (no performance impact—pure reorganization)
**Constraints**: Must preserve git history, maintain 100% test compatibility, zero downtime for users
**Scale/Scope**: Small refactoring—moving 2 scripts, updating documentation, removing 1 obsolete folder

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: Skill-Centric Architecture ✅
- SKILL.md will be enhanced to be the single comprehensive documentation source
- Scripts organized in standard `/scripts` directory improves clarity
- No changes to core skill functionality or architecture
- Documentation consolidation supports "documentation-first" principle

### Gate 2: Text I/O Protocol ✅
- No changes to input/output protocol
- Scripts remain command-line tools with text I/O
- File reorganization doesn't affect functionality

### Gate 3: Minimal Dependencies ✅
- No new dependencies added
- Existing dependencies remain unchanged (gTTS, pydub, pytest)
- requirements.txt not modified

### Gate 4: Error Handling & Observability ✅
- No changes to error handling or logging
- Exit codes remain the same
- Error messages unchanged

### Gate 5: Test-First Development ✅
- All existing tests must continue to pass after reorganization
- Test imports will be updated to reference new script locations
- No new tests required (functionality unchanged)

### Documentation Standards ✅
- SKILL.md will be enhanced with Quick Start section from README.md
- All examples updated to show correct paths
- Migration notes added for users
- Project structure diagram updated

**Result**: All gates passed. This is a pure refactoring that improves project organization and documentation without violating any constitutional principles.

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
# BEFORE (Current Structure)
tts/
├── tts.py                       # MOVE to scripts/
├── SKILL.md                     # UPDATE with README content
├── README.md                    # SIMPLIFY to brief overview
├── requirements.txt             # No changes
├── tests/                       # UPDATE imports
│   ├── test_tts.py
│   ├── test_audio_format.py
│   └── test_integration.py
├── output/                      # No changes
├── mp3-to-ogg/                  # REMOVE entire folder
│   ├── SKILL.md
│   ├── README.md
│   └── scripts/
│       └── convert_mp3_to_ogg.py
└── specs/                       # No changes

# AFTER (Target Structure)
tts/
├── scripts/                     # NEW directory
│   ├── tts.py                  # MOVED from root
│   └── convert_mp3_to_ogg.py   # MOVED from mp3-to-ogg/scripts/
├── SKILL.md                     # ENHANCED with README content
├── README.md                    # SIMPLIFIED (<50 lines)
├── requirements.txt             # No changes
├── tests/                       # UPDATED imports
│   ├── test_tts.py
│   ├── test_audio_format.py
│   └── test_integration.py
├── output/                      # No changes
└── specs/                       # No changes
```

**Structure Decision**: Standard Python CLI project structure. All executable scripts consolidated in `/scripts` directory following common conventions. Documentation unified in single SKILL.md file. Obsolete code removed.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

N/A - No constitutional violations. This refactoring:
- Improves project organization (aligns with Skill-Centric Architecture)
- Enhances documentation clarity (supports Documentation Standards)
- Removes obsolete code (simplification)
- Preserves all existing functionality and tests
