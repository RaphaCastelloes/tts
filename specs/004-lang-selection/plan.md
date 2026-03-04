# Implementation Plan: Language Selection for TTS

**Branch**: `004-lang-selection` | **Date**: 2026-03-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-lang-selection/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Add command-line language selection capability to the TTS script with Brazilian Portuguese (pt-br) as default and support for English (en) via --lang argument. This maintains backward compatibility while enabling multilingual speech generation.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.8+  
**Primary Dependencies**: gTTS 2.5.0, argparse (stdlib)  
**Storage**: N/A (stateless CLI tool)  
**Testing**: pytest 7.4.3  
**Target Platform**: Oracle Linux (POSIX-compliant, headless execution)
**Project Type**: CLI tool (single-file executable script)  
**Performance Goals**: 1-10 seconds per conversion (network-dependent)  
**Constraints**: Requires internet connection, max 1000 characters input  
**Scale/Scope**: Single-user CLI invocations, ~200 LOC modification

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Skill-Centric Architecture
✅ **PASS** - Modifying existing tts.py script with language parameter
✅ **PASS** - SKILL.md will be updated to document new --lang argument
✅ **PASS** - No new dependencies required (argparse is stdlib)
✅ **PASS** - Self-contained modification to existing skill

### Principle II: Text I/O Protocol
✅ **PASS** - Command-line argument --lang follows existing pattern
✅ **PASS** - Maintains stdout (file path) and stderr (errors) protocol
✅ **PASS** - No GUI or interactive prompts
✅ **PASS** - Backward compatible with existing text I/O

### Principle III: Minimal Dependencies
✅ **PASS** - No new external dependencies
✅ **PASS** - Uses stdlib argparse for argument parsing
✅ **PASS** - gTTS already supports multiple languages
✅ **PASS** - requirements.txt unchanged

### Principle IV: Error Handling & Observability
✅ **PASS** - Will validate language codes with clear error messages
✅ **PASS** - Maintains existing exit code structure
✅ **PASS** - Error messages guide users to supported languages
✅ **PASS** - Input validation for language parameter

### Principle V: Test-First Development
✅ **PASS** - Will write tests for language parameter validation
✅ **PASS** - Will test default language behavior (pt-br)
✅ **PASS** - Will test explicit language selection (en, pt-br)
✅ **PASS** - Will test error cases (invalid language codes)

### Platform & Runtime Constraints
✅ **PASS** - Python 3.8+ compatible (no new language features)
✅ **PASS** - Oracle Linux compatible (POSIX paths, headless)
✅ **PASS** - No new system dependencies
✅ **PASS** - Maintains LF line endings

**GATE STATUS**: ✅ ALL CHECKS PASSED - Proceed to Phase 0

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
├── tts.py                    # Main executable (MODIFIED: add --lang argument)
├── SKILL.md                  # Documentation (MODIFIED: document --lang usage)
├── requirements.txt          # Dependencies (UNCHANGED)
├── tests/
│   ├── test_tts.py          # Unit tests (MODIFIED: add language tests)
│   ├── test_audio_format.py # Format tests (UNCHANGED)
│   └── test_integration.py  # Integration tests (MODIFIED: test language selection)
└── output/                   # Generated audio files
```

**Structure Decision**: Single-file CLI tool structure. This is a minimal modification to existing tts.py script to add language parameter support. No new files or directories needed beyond test updates.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**Status**: No violations - this section is not applicable.

All constitutional principles are satisfied with the minimal design approach.

---

## Post-Phase 1 Constitution Re-Check

*Re-evaluation after design artifacts (research.md, data-model.md, contracts, quickstart.md) completed.*

### Principle I: Skill-Centric Architecture
✅ **PASS** - Design maintains single tts.py script structure
✅ **PASS** - SKILL.md update documented in quickstart.md
✅ **PASS** - No new dependencies introduced
✅ **PASS** - Self-contained language selection feature

### Principle II: Text I/O Protocol
✅ **PASS** - CLI contract specifies text-based I/O (contracts/cli-interface.md)
✅ **PASS** - Stdout/stderr protocol unchanged
✅ **PASS** - No GUI or interactive elements in design
✅ **PASS** - Backward compatible with existing text I/O patterns

### Principle III: Minimal Dependencies
✅ **PASS** - Zero new external dependencies confirmed in research.md
✅ **PASS** - Uses stdlib argparse (already in use)
✅ **PASS** - gTTS language support already present
✅ **PASS** - requirements.txt remains unchanged

### Principle IV: Error Handling & Observability
✅ **PASS** - Error handling strategy defined in research.md (argparse choices)
✅ **PASS** - Exit codes unchanged (documented in CLI contract)
✅ **PASS** - Error messages specified in contracts/cli-interface.md
✅ **PASS** - Input validation via argparse choices parameter

### Principle V: Test-First Development
✅ **PASS** - Test cases defined in research.md section 5
✅ **PASS** - Testing checklist in quickstart.md
✅ **PASS** - 6 test scenarios identified (default, explicit en/pt-br, invalid, help, backward compat)
✅ **PASS** - Test contract specified in contracts/cli-interface.md

### Platform & Runtime Constraints
✅ **PASS** - Python 3.8+ compatibility confirmed (no new features required)
✅ **PASS** - Oracle Linux compatible (POSIX, headless)
✅ **PASS** - No new system dependencies
✅ **PASS** - Design maintains LF line endings

### Documentation Standards
✅ **PASS** - SKILL.md update plan in quickstart.md
✅ **PASS** - Inline comments not needed (simple argparse addition)
✅ **PASS** - Version history will be updated with feature
✅ **PASS** - Examples provided in quickstart.md and CLI contract

**FINAL GATE STATUS**: ✅ ALL CHECKS PASSED - Design approved, ready for task generation

---

## Next Steps

Run `/speckit.tasks` to generate the implementation task list (tasks.md) based on this plan.
