# Implementation Tasks: OGG-Only Audio Output

**Feature**: 003-ogg-only-output  
**Branch**: `003-ogg-only-output`  
**Created**: March 3, 2026

## Overview

This document provides a complete task breakdown for implementing OGG/Opus audio output, organized by user story to enable independent implementation and testing.

## Task Summary

- **Total Tasks**: 25
- **Setup & Foundational**: 7 tasks
- **User Story 1 (P1)**: 9 tasks
- **User Story 2 (P2)**: 4 tasks  
- **User Story 3 (P3)**: 3 tasks
- **Polish**: 2 tasks

## Implementation Strategy

**MVP Scope**: Complete User Story 1 (P1) only for initial release
- Delivers core OGG conversion functionality
- Independently testable
- Provides immediate value (30-50% file size reduction)

**Incremental Delivery**:
1. Phase 3 (US1): OGG conversion - MVP
2. Phase 4 (US2): Custom output paths - Enhancement
3. Phase 5 (US3): File naming compatibility - Polish

---

## Phase 1: Setup & Dependencies

**Goal**: Install dependencies and update project configuration

**Tasks**:

- [x] T001 Update requirements.txt to add pydub==0.25.1 in c:\Users\caste\source\repos\tts\requirements.txt
- [ ] T002 Verify ffmpeg installation on Oracle Linux ARM64 (sudo yum install -y epel-release && sudo yum install -y ffmpeg)
- [x] T003 Update .gitignore to include *.ogg exclusion in c:\Users\caste\source\repos\tts\.gitignore

**Completion Criteria**:
- [ ] requirements.txt contains pydub==0.25.1
- [ ] ffmpeg installed and accessible
- [ ] .gitignore excludes .ogg files

---

## Phase 2: Foundational Components

**Goal**: Implement shared infrastructure needed by all user stories

**Tasks**:

- [x] T004 [P] Add pydub import to tts.py in c:\Users\caste\source\repos\tts\tts.py
- [x] T005 [P] Update generate_filename() to return .ogg extension in c:\Users\caste\source\repos\tts\tts.py
- [x] T006 Create encode_to_opus_ogg() function for MP3→OGG conversion in c:\Users\caste\source\repos\tts\tts.py
- [x] T007 Add ffmpeg availability check with error message in c:\Users\caste\source\repos\tts\tts.py

**Completion Criteria**:
- [ ] All imports added successfully
- [ ] File naming generates .ogg extension
- [ ] Conversion function implemented
- [ ] ffmpeg check provides clear error message

**Blocking**: Must complete before any user story implementation

---

## Phase 3: User Story 1 - Generate OGG Audio Files (P1)

**Story Goal**: Convert text to OGG/Opus audio files optimized for WhatsApp

**Independent Test**: `python tts.py "hello world"` creates valid OGG/Opus file with 16kHz mono audio

**Tasks**:

### Implementation
- [x] T008 [US1] Update main() to call encode_to_opus_ogg() after generate_speech() in c:\Users\caste\source\repos\tts\tts.py
- [x] T009 [US1] Implement audio loading (AudioSegment.from_mp3) in encode_to_opus_ogg() in c:\Users\caste\source\repos\tts\tts.py
- [x] T010 [US1] Implement mono conversion (set_channels(1)) in encode_to_opus_ogg() in c:\Users\caste\source\repos\tts\tts.py
- [x] T011 [US1] Implement sample rate conversion (set_frame_rate(16000)) in encode_to_opus_ogg() in c:\Users\caste\source\repos\tts\tts.py
- [x] T012 [US1] Implement OGG/Opus export with parameters in encode_to_opus_ogg() in c:\Users\caste\source\repos\tts\tts.py
- [x] T013 [US1] Add error handling for ffmpeg not found in encode_to_opus_ogg() in c:\Users\caste\source\repos\tts\tts.py
- [x] T014 [US1] Add error handling for audio encoding failures in encode_to_opus_ogg() in c:\Users\caste\source\repos\tts\tts.py
- [x] T015 [US1] Update SKILL.md to document OGG format and ffmpeg dependency in c:\Users\caste\source\repos\tts\SKILL.md
- [x] T016 [US1] Update README.md to document OGG format and installation steps in c:\Users\caste\source\repos\tts\README.md

**Acceptance Criteria**:
- [x] Script accepts text as command-line argument
- [ ] Audio file generated in OGG container with Opus codec
- [ ] Audio sample rate is 16000 Hz
- [ ] Audio is mono (1 channel)
- [ ] File saved to output/ directory with .ogg extension
- [ ] Absolute file path printed to stdout
- [ ] Audio plays correctly in WhatsApp
- [ ] Clear error if ffmpeg not installed
- [ ] Documentation updated

**Dependencies**: Phase 2 must be complete

---

## Phase 4: User Story 2 - Maintain Custom Output Path Support (P2)

**Story Goal**: Preserve -o/--output flag functionality for OGG files

**Independent Test**: `python tts.py "hello" -o custom.ogg` creates OGG file at specified location

**Tasks**:

### Implementation
- [x] T017 [US2] Update custom path logic to replace .mp3 extension with .ogg in c:\Users\caste\source\repos\tts\tts.py
- [x] T018 [US2] Update custom path logic to add .ogg if no extension provided in c:\Users\caste\source\repos\tts\tts.py
- [x] T019 [US2] Update custom path logic to keep .ogg extension if already specified in c:\Users\caste\source\repos\tts\tts.py
- [x] T020 [US2] Update SKILL.md with custom output path examples for OGG in c:\Users\caste\source\repos\tts\SKILL.md

**Acceptance Criteria**:
- [ ] -o flag works with .ogg extension
- [ ] .mp3 extension automatically replaced with .ogg
- [ ] Missing extension automatically adds .ogg
- [ ] Existing .ogg extension preserved
- [ ] Documentation includes OGG examples

**Dependencies**: Phase 3 (US1) must be complete

---

## Phase 5: User Story 3 - Backward Compatible File Naming (P3)

**Story Goal**: Maintain existing filename pattern with only extension change

**Independent Test**: Generate multiple files and verify pattern `tts_YYYYMMDD_HHMMSS_<hash>.ogg`

**Tasks**:

### Implementation
- [x] T021 [US3] Verify generate_filename() maintains timestamp pattern in c:\Users\caste\source\repos\tts\tts.py
- [x] T022 [US3] Verify generate_filename() maintains unique hash generation in c:\Users\caste\source\repos\tts\tts.py
- [x] T023 [US3] Update documentation to show filename pattern with .ogg extension in c:\Users\caste\source\repos\tts\SKILL.md

**Acceptance Criteria**:
- [x] Filename follows pattern `tts_YYYYMMDD_HHMMSS_<hash>.ogg`
- [x] Each file has unique timestamp and hash
- [x] Existing automation compatible (only extension changed)
- [ ] Documentation shows OGG filename examples

**Dependencies**: Phase 3 (US1) must be complete (US2 is optional)

---

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Finalize documentation and production readiness

**Tasks**:

- [x] T024 [P] Create migration guide from MP3 to OGG in c:\Users\caste\source\repos\tts\README.md
- [x] T025 [P] Update all documentation examples to use .ogg instead of .mp3 across SKILL.md, README.md

**Completion Criteria**:
- [ ] Migration guide complete
- [ ] All documentation consistent with OGG format
- [ ] No references to MP3 output remain

---

## Dependencies & Execution Order

### Story Dependencies
```
Setup (Phase 1) → Foundational (Phase 2) → US1 (P1) → [US2 (P2), US3 (P3)] → Polish
                                              ↓
                                          US2 (P2) ─→ (optional dependency)
                                          US3 (P3) ─→ (independent)
```

**Critical Path**: Setup → Foundational → US1
**Parallel Opportunities**: US2 and US3 can be done in parallel after US1

### Task-Level Dependencies

**Phase 1 (Setup)**:
- T001, T002, T003: Can run in parallel

**Phase 2 (Foundational)**:
- T004, T005: Can run in parallel (different functions)
- T006: Must complete before T007
- All must complete before Phase 3

**Phase 3 (US1)**:
- T008: Depends on T006 (encode_to_opus_ogg exists)
- T009-T014: Sequential implementation of encode_to_opus_ogg
- T015, T016: Can run in parallel (different files)

**Phase 4 (US2)**:
- T017-T019: Sequential (modify same function)
- T020: Can run after T017-T019 complete

**Phase 5 (US3)**:
- T021, T022: Verification tasks (can run in parallel)
- T023: Documentation update

**Phase 6 (Polish)**:
- T024, T025: Can run in parallel (different sections)

## Parallel Execution Examples

### Setup Phase (All Parallel)
```bash
# Can execute simultaneously:
- T001: Update requirements.txt
- T002: Install ffmpeg
- T003: Update .gitignore
```

### Foundational Phase (Partial Parallel)
```bash
# Parallel group 1:
- T004: Add pydub import
- T005: Update generate_filename()

# Sequential:
- T006: Create encode_to_opus_ogg()
- T007: Add ffmpeg check
```

### US1 Implementation
```bash
# Sequential core implementation:
- T008-T014: encode_to_opus_ogg implementation

# Parallel documentation:
- T015: Update SKILL.md
- T016: Update README.md
```

## Testing Strategy

### Manual Testing

**US1 (P1) - OGG Generation**:
```bash
# Basic test
python tts.py "hello world"
file output/tts_*.ogg  # Should show: Ogg data, Opus audio

# Verify properties
ffprobe output/tts_*.ogg 2>&1 | grep Stream
# Should show: Audio: opus, 16000 Hz, mono

# Test in WhatsApp
# Send file via WhatsApp and verify playback
```

**US2 (P2) - Custom Paths**:
```bash
# Test custom path with .ogg
python tts.py "hello" -o test.ogg
ls test.ogg  # Should exist

# Test extension replacement
python tts.py "hello" -o test.mp3
ls test.ogg  # Should exist (mp3 replaced)

# Test no extension
python tts.py "hello" -o test
ls test.ogg  # Should exist (ogg added)
```

**US3 (P3) - File Naming**:
```bash
# Generate multiple files
python tts.py "test1"
python tts.py "test2"
python tts.py "test3"

# Verify pattern
ls output/tts_*.ogg
# Should show: tts_YYYYMMDD_HHMMSS_<hash>.ogg pattern
```

### Error Testing

```bash
# Test ffmpeg not installed (temporarily rename ffmpeg)
python tts.py "hello"
# Should show: Error: ffmpeg not installed. Run: sudo yum install ffmpeg

# Test network error (disconnect internet)
python tts.py "hello"
# Should show: Error: Cannot connect to TTS service

# Test invalid input
python tts.py ""
# Should show: Error: No text provided
```

## Verification Checklist

Before marking feature complete:

- [ ] All tasks marked as complete
- [ ] OGG files generated successfully
- [ ] File format verified (Ogg container, Opus codec)
- [ ] Audio properties verified (16kHz, mono)
- [ ] WhatsApp compatibility confirmed
- [ ] Custom output paths working
- [ ] File naming pattern maintained
- [ ] All documentation updated
- [ ] Migration guide complete
- [ ] ffmpeg error handling working
- [ ] No MP3 references in documentation

## Notes

- **Breaking Change**: Output format changes from MP3 to OGG (major version bump warranted)
- **Backward Compatibility**: CLI arguments remain identical
- **File Size Reduction**: Expect 30-50% smaller files compared to MP3
- **Dependencies**: Adds pydub (Python) and ffmpeg (system)
- **Performance**: No significant impact (<1s conversion time)
