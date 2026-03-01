# Implementation Tasks: WhatsApp TTS Script

**Feature**: 002-whatsapp-tts-script  
**Branch**: `002-whatsapp-tts-script`  
**Date**: March 1, 2026  
**Spec**: [spec.md](./spec.md) | [Plan](./plan.md)

## Overview

This document provides a complete, dependency-ordered task list for implementing the WhatsApp TTS script. Tasks are organized by user story to enable independent implementation and testing of each feature increment.

**Total Tasks**: 24  
**User Stories**: 3 (P1, P2, P3)  
**Parallel Opportunities**: 8 tasks can run in parallel within phases

## Implementation Strategy

### MVP Scope (Recommended First Delivery)
- **User Story 1 (P1)**: Basic Text-to-Speech Conversion
- Delivers core value: text → WhatsApp-compatible audio file
- Independently testable and deployable
- Estimated effort: ~8-12 hours

### Incremental Delivery
1. **Phase 1-3**: Setup + Foundational + US1 → MVP release
2. **Phase 4**: US2 → WhatsApp compatibility validation
3. **Phase 5**: US3 → Multi-language support
4. **Phase 6**: Polish → Production-ready

## User Story Summary

| Story | Priority | Goal | Independent Test |
|-------|----------|------|------------------|
| US1 | P1 | Basic text-to-speech conversion | Run script with text input, verify Opus/OGG file created and path printed |
| US2 | P2 | WhatsApp compatibility verification | Send generated file via WhatsApp, verify it plays correctly |
| US3 | P3 | Multi-language text support | Test with Portuguese/English text, verify correct pronunciation |

---

## Phase 1: Setup & Project Initialization

**Goal**: Establish project structure and dependencies

**Tasks**:

- [x] T001 Create project directory structure per plan.md (tts.py, SKILL.md, requirements.txt, tests/, output/)
- [x] T002 Create requirements.txt with gTTS==2.5.0 and pydub==0.25.1
- [x] T003 Create .gitignore file to exclude output/ directory and Python cache files
- [x] T004 Create output/ directory for generated audio files
- [x] T005 Create SKILL.md documentation file with template structure (purpose, usage, dependencies sections)

**Completion Criteria**:
- [ ] All directories and files exist
- [ ] requirements.txt contains correct dependencies
- [ ] .gitignore properly configured

---

## Phase 2: Foundational Components

**Goal**: Implement shared infrastructure needed by all user stories

**Tasks**:

- [x] T006 [P] Write test_tts.py test file structure with test classes for input validation
- [x] T007 [P] Write test_audio_format.py test file structure with test classes for audio format validation
- [x] T008 [P] Write test_integration.py test file structure with test classes for end-to-end testing
- [x] T009 Implement input validation function in tts.py (validate text length 1-1000 chars, non-empty)
- [x] T010 Implement error handling framework in tts.py (exit codes 0-4, stderr error messages)
- [x] T011 Implement file naming function in tts.py (format: tts_YYYYMMDD_HHMMSS_<hash>.ogg)
- [x] T012 Implement output directory creation in tts.py (create output/ if not exists)

**Completion Criteria**:
- [ ] Test structure complete for all test types
- [ ] Input validation handles all edge cases (empty, too long, special chars)
- [ ] Error handling uses correct exit codes per CLI contract
- [ ] File naming generates unique names per specification

**Blocking**: Must complete before any user story implementation

---

## Phase 3: User Story 1 - Basic Text-to-Speech Conversion (P1)

**Story Goal**: Convert text to WhatsApp-compatible audio file and print file path

**Independent Test**: `python tts.py "hello world"` creates valid Opus/OGG file and prints absolute path

**Tasks**:

### Tests (TDD Approach)
- [x] T013 [P] [US1] Write unit tests for text input validation in test_tts.py
- [x] T014 [P] [US1] Write unit tests for TTS generation in test_tts.py
- [x] T015 [P] [US1] Write unit tests for audio encoding in test_tts.py
- [x] T016 [P] [US1] Write integration test for complete conversion flow in test_integration.py

### Implementation
- [x] T017 [US1] Implement command-line argument parsing in tts.py (sys.argv handling)
- [x] T018 [US1] Implement gTTS integration in tts.py (text → MP3 audio generation)
- [x] T019 [US1] Implement pydub audio conversion in tts.py (MP3 → Opus/OGG with 16kHz mono)
- [x] T020 [US1] Implement file output in tts.py (save to output/ directory)
- [x] T021 [US1] Implement stdout path printing in tts.py (print absolute file path)
- [x] T022 [US1] Implement main execution flow in tts.py (orchestrate validation → TTS → encoding → output)

**Acceptance Criteria**:
- [ ] Script accepts text as command-line argument
- [ ] Audio file generated in Opus codec with OGG container
- [ ] File saved to output/ directory with unique name
- [ ] Absolute file path printed to stdout
- [ ] Audio clearly speaks input text when played
- [ ] All US1 tests pass

**Dependencies**: Phase 2 must be complete

---

## Phase 4: User Story 2 - WhatsApp Compatibility Verification (P2)

**Story Goal**: Ensure generated audio files are fully compatible with WhatsApp

**Independent Test**: Send generated file via WhatsApp, verify it plays correctly on Android/iOS

**Tasks**:

### Tests
- [ ] T023 [P] [US2] Write audio format validation tests in test_audio_format.py (verify Opus codec, OGG container, 16kHz, mono)
- [ ] T024 [P] [US2] Write WhatsApp compatibility tests in test_audio_format.py (verify file format specs match WhatsApp requirements)

### Implementation
- [ ] T025 [US2] Add audio format validation in tts.py (verify output is valid Opus/OGG before returning)
- [ ] T026 [US2] Add sample rate verification in tts.py (ensure 16000 Hz)
- [ ] T027 [US2] Add channel verification in tts.py (ensure mono channel)
- [ ] T028 [US2] Update SKILL.md with WhatsApp compatibility testing instructions

**Acceptance Criteria**:
- [ ] Generated files use Opus codec in OGG container
- [ ] Sample rate is 16000 Hz
- [ ] Audio is mono (1 channel)
- [ ] Files successfully play in WhatsApp on Android and iOS
- [ ] All US2 tests pass

**Dependencies**: Phase 3 (US1) must be complete

---

## Phase 5: User Story 3 - Multi-language Text Support (P3)

**Story Goal**: Support text-to-speech conversion in multiple languages (English, Portuguese)

**Independent Test**: Run script with Portuguese text, verify correct pronunciation

**Tasks**:

### Tests
- [ ] T029 [P] [US3] Write multi-language tests in test_tts.py (test English and Portuguese text)
- [ ] T030 [P] [US3] Write special character handling tests in test_tts.py (test emojis, accents, punctuation)

### Implementation
- [ ] T031 [US3] Add language auto-detection support in tts.py (leverage gTTS auto-detection)
- [ ] T032 [US3] Add special character handling in tts.py (ensure UTF-8 encoding, handle emojis)
- [ ] T033 [US3] Update SKILL.md with multi-language usage examples (English, Portuguese)

**Acceptance Criteria**:
- [ ] Portuguese text generates audio with correct pronunciation
- [ ] English text generates audio with correct pronunciation
- [ ] Special characters (emojis, accents) handled without errors
- [ ] All US3 tests pass

**Dependencies**: Phase 3 (US1) must be complete (US2 is optional)

---

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Finalize documentation, error handling, and production readiness

**Tasks**:

- [ ] T034 [P] Complete SKILL.md documentation (purpose, usage, inputs, outputs, dependencies, error codes, troubleshooting)
- [ ] T035 [P] Add comprehensive error messages for all failure scenarios (network, file system, processing errors)
- [ ] T036 [P] Add logging to stderr for informational messages ([INFO], [WARN], [ERROR] levels)
- [ ] T037 Verify all exit codes match CLI contract (0=success, 1=input, 2=network, 3=filesystem, 4=processing)
- [ ] T038 Add performance optimization (use in-memory buffers, minimize temp file I/O)
- [ ] T039 Run full test suite and verify all tests pass
- [ ] T040 Create README.md with quick installation and usage guide
- [ ] T041 Verify Oracle Linux ARM 64-bit compatibility (test on target platform if available)

**Completion Criteria**:
- [ ] All documentation complete and accurate
- [ ] All error scenarios have clear, actionable messages
- [ ] All tests pass
- [ ] Performance meets <10 second goal for 500-character input
- [ ] Code follows PEP 8 style guidelines

---

## Dependency Graph

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational)
    ↓
    ├─→ Phase 3 (US1 - P1) ← MVP DELIVERY POINT
    │       ↓
    │       ├─→ Phase 4 (US2 - P2)
    │       │
    │       └─→ Phase 5 (US3 - P3)
    │
    └─→ Phase 6 (Polish) ← depends on all user stories
```

**User Story Dependencies**:
- US1 (P1): No dependencies (can implement after foundational)
- US2 (P2): Depends on US1 (needs basic audio generation)
- US3 (P3): Depends on US1 (needs basic audio generation)
- US2 and US3 are independent of each other

---

## Parallel Execution Opportunities

### Within Phase 2 (Foundational)
**Can run in parallel**:
- T006, T007, T008 (test file creation - different files)

### Within Phase 3 (US1)
**Can run in parallel**:
- T013, T014, T015, T016 (test writing - different test functions)

### Within Phase 4 (US2)
**Can run in parallel**:
- T023, T024 (test writing - different test functions)

### Within Phase 5 (US3)
**Can run in parallel**:
- T029, T030 (test writing - different test functions)

### Within Phase 6 (Polish)
**Can run in parallel**:
- T034, T035, T036 (documentation and error handling - different concerns)

**Total Parallel Tasks**: 14 tasks can be executed in parallel with others

---

## Task Execution Examples

### Example 1: MVP Implementation (US1 Only)

```bash
# Phase 1: Setup
Execute T001-T005 sequentially

# Phase 2: Foundational
Execute T006, T007, T008 in parallel
Then execute T009-T012 sequentially

# Phase 3: US1
Execute T013-T016 in parallel (write all tests)
Then execute T017-T022 sequentially (implement features)

# Verify MVP
python tts.py "hello world"
# Should output: /path/to/output/tts_YYYYMMDD_HHMMSS_hash.ogg
```

### Example 2: Full Feature Implementation

```bash
# Execute Phases 1-3 (MVP)
# Then add US2
Execute T023, T024 in parallel (tests)
Execute T025-T028 sequentially (implementation)

# Then add US3
Execute T029, T030 in parallel (tests)
Execute T031-T033 sequentially (implementation)

# Finally polish
Execute T034-T036 in parallel
Execute T037-T041 sequentially
```

---

## Testing Strategy

### Test Organization (per plan.md)

```
tests/
├── test_tts.py           # Unit tests for TTS functionality
├── test_audio_format.py  # Audio format validation tests
└── test_integration.py   # End-to-end integration tests
```

### Test Coverage Requirements

**test_tts.py** (Unit Tests):
- Input validation (empty, too long, special chars)
- TTS generation (gTTS integration)
- Audio encoding (pydub conversion)
- File naming (unique name generation)
- Error handling (all exit codes)

**test_audio_format.py** (Format Validation):
- Opus codec verification
- OGG container verification
- Sample rate (16000 Hz)
- Channel count (mono)
- WhatsApp compatibility

**test_integration.py** (End-to-End):
- Complete conversion flow (text → audio file)
- File path output verification
- Multi-language support
- Error scenarios (network, filesystem, processing)

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_tts.py

# Run with coverage
pytest --cov=tts tests/
```

---

## File Paths Reference

### Source Files
- `tts.py` - Main executable script
- `SKILL.md` - Skill documentation
- `requirements.txt` - Python dependencies
- `README.md` - Quick start guide

### Test Files
- `tests/test_tts.py` - Unit tests
- `tests/test_audio_format.py` - Format validation tests
- `tests/test_integration.py` - Integration tests

### Output
- `output/` - Generated audio files directory
- `output/tts_YYYYMMDD_HHMMSS_<hash>.ogg` - Audio file pattern

---

## Constitution Compliance Checklist

- [x] **Skill-Centric Architecture**: Single tts.py script with SKILL.md
- [x] **Text I/O Protocol**: CLI args input, stdout/stderr output
- [x] **Minimal Dependencies**: Only gTTS, pydub, ffmpeg
- [x] **Error Handling**: Exit codes 0-4, clear error messages
- [x] **Test-First Development**: Tests written before implementation
- [x] **Platform Constraints**: Oracle Linux compatible, Python 3.8+

---

## Success Metrics (from spec.md)

- [ ] **SC-001**: Audio generation in <10 seconds for 500-character input
- [ ] **SC-002**: Files playable in WhatsApp on Android and iOS
- [ ] **SC-003**: Processes 1-1000 character inputs without errors
- [ ] **SC-004**: Users can copy printed file path without manual searching
- [ ] **SC-005**: Runs on Oracle Linux ARM 64-bit without compilation

---

## Notes

- **TDD Approach**: Tests are written before implementation per Constitution Principle V
- **Independent Stories**: Each user story can be tested independently
- **MVP First**: US1 (P1) delivers complete, usable functionality
- **Incremental Value**: US2 and US3 add enhancements without breaking US1
- **Parallel Work**: 14 tasks can run in parallel to speed up development
