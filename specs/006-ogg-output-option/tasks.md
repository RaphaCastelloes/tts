# Tasks: OGG Output Option

**Input**: Design documents from `/specs/006-ogg-output-option/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-interface.md

**Tests**: Tests will be written following TDD approach (per constitution Gate 5)

**Organization**: Tasks grouped by user story to enable independent implementation and testing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency setup

- [x] T001 Add pydub==0.25.1 to c:\Users\caste\source\repos\tts\requirements.txt
- [x] T002 Install dependencies via pip install -r requirements.txt
- [x] T003 Verify ffmpeg is installed on system (yum list installed ffmpeg)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Add --format argument to argparse in c:\Users\caste\source\repos\tts\tts.py (choices=['mp3', 'ogg'], default='mp3')
- [x] T005 Create format validation function in c:\Users\caste\source\repos\tts\tts.py (validate_format)
- [x] T006 Update file extension logic to auto-correct based on format in c:\Users\caste\source\repos\tts\tts.py (get_output_path_with_extension)

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Generate OGG Audio Directly (Priority: P1) 🎯 MVP

**Goal**: Enable direct OGG audio generation via --format ogg flag, eliminating separate mp3-to-ogg conversion step

**Independent Test**: Run `python tts.py "hello" --format ogg` and verify valid OGG file with Opus codec is generated and path returned on stdout

### Tests for User Story 1 (TDD Approach)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T007 [P] [US1] Create test_format_argument_parsing in c:\Users\caste\source\repos\tts\tests\test_tts.py
  - Test --format ogg is accepted
  - Test --format mp3 is accepted  
  - Test invalid format returns error
  - Test default format is mp3

- [x] T008 [P] [US1] Create test_ogg_file_generation in c:\Users\caste\source\repos\tts\tests\test_audio_format.py
  - Test OGG file is created when --format ogg specified
  - Test file has .ogg extension
  - Test file is valid OGG format
  - Test file contains Opus codec

- [x] T009 [P] [US1] Create test_extension_auto_correction in c:\Users\caste\source\repos\tts\tests\test_tts.py
  - Test .mp3 extension corrected to .ogg when --format ogg
  - Test .ogg extension preserved when --format ogg
  - Test extension auto-appended when missing

- [x] T010 [P] [US1] Create test_ogg_conversion_errors in c:\Users\caste\source\repos\tts\tests\test_tts.py
  - Test error when ffmpeg not available
  - Test error when pydub import fails
  - Test proper exit code 4 for conversion errors

### Implementation for User Story 1

- [x] T011 [US1] Implement convert_to_ogg function in c:\Users\caste\source\repos\tts\tts.py
  - Use pydub AudioSegment to load MP3
  - Export as OGG with Opus codec (libopus)
  - Handle pydub import errors
  - Handle ffmpeg availability errors
  - Return path to OGG file

- [x] T012 [US1] Update main execution flow in c:\Users\caste\source\repos\tts\tts.py
  - Check format argument after MP3 generation
  - If format == 'ogg', call convert_to_ogg()
  - Delete intermediate MP3 file after OGG conversion
  - Update output_path variable to OGG path

- [x] T013 [US1] Add error handling for OGG conversion in c:\Users\caste\source\repos\tts\tts.py
  - Catch pydub ModuleNotFoundError
  - Catch ffmpeg FileNotFoundError
  - Print helpful error messages to stderr
  - Exit with code 4 for conversion errors

- [x] T014 [US1] Add format validation in argument parser in c:\Users\caste\source\repos\tts\tts.py
  - Validate format in ['mp3', 'ogg']
  - Print error for invalid formats
  - Exit with code 1 for validation errors

**Checkpoint**: User Story 1 complete - OGG generation works independently

---

## Phase 4: User Story 2 - Maintain MP3 as Default Format (Priority: P2)

**Goal**: Ensure MP3 remains default format for backward compatibility, existing integrations work without modification

**Independent Test**: Run `python tts.py "hello"` without --format flag and verify MP3 file is generated (existing behavior preserved)

### Tests for User Story 2

- [x] T015 [P] [US2] Create test_backward_compatibility in c:\Users\caste\source\repos\tts\tests\test_tts.py
  - Test no --format flag defaults to MP3
  - Test MP3 file naming unchanged
  - Test existing --lang option works with both formats
  - Test existing -o option works with both formats

- [x] T016 [P] [US2] Create test_explicit_mp3_format in c:\Users\caste\source\repos\tts\tests\test_tts.py
  - Test --format mp3 generates MP3 file
  - Test MP3 file is valid
  - Test MP3 file path returned to stdout

### Implementation for User Story 2

- [x] T017 [US2] Verify default format logic in c:\Users\caste\source\repos\tts\tts.py
  - Ensure argparse default='mp3' for --format
  - Verify MP3 generation when format == 'mp3'
  - No conversion step when format == 'mp3'

- [x] T018 [US2] Run regression tests for existing functionality in c:\Users\caste\source\repos\tts\tests\
  - pytest tests/test_tts.py -k "not ogg"
  - Verify all existing tests still pass
  - Verify no breaking changes

**Checkpoint**: User Story 2 complete - Backward compatibility verified

---

## Phase 5: User Story 3 - Update Documentation for New Workflow (Priority: P3)

**Goal**: Update SKILL.md to document --format option and simplified 5-step workflow

**Independent Test**: Review SKILL.md and verify --format option documented with examples, workflow shows direct OGG generation

### Implementation for User Story 3

- [x] T019 [P] [US3] Update Usage section in c:\Users\caste\source\repos\tts\SKILL.md
  - Add --format option to command-line options table
  - Add OGG generation examples
  - Show both MP3 and OGG usage

- [x] T020 [P] [US3] Update Bot Integration Use Case in c:\Users\caste\source\repos\tts\SKILL.md
  - Remove step 5 (mp3-to-ogg conversion)
  - Update step 4 to show --format ogg option
  - Update workflow to be 5 steps instead of 6
  - Remove reference to separate mp3-to-ogg skill

- [x] T021 [P] [US3] Update Dependencies section in c:\Users\caste\source\repos\tts\SKILL.md
  - Add pydub to Python dependencies list
  - Add ffmpeg to system dependencies
  - Document ffmpeg installation: yum install ffmpeg

- [x] T022 [P] [US3] Add Error Messages section for OGG in c:\Users\caste\source\repos\tts\SKILL.md
  - Document invalid format error
  - Document ffmpeg missing error
  - Document pydub missing error
  - Show exit code 4 for conversion errors

**Checkpoint**: User Story 3 complete - Documentation updated

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements and validation across all user stories

- [x] T023 [P] Create integration test for WhatsApp compatibility in c:\Users\caste\source\repos\tts\tests\test_integration.py
  - Generate OGG file with --format ogg
  - Verify Opus codec using ffprobe
  - Verify file plays in audio player
  - Document manual WhatsApp testing steps

- [x] T024 [P] Add performance test for OGG conversion in c:\Users\caste\source\repos\tts\tests\test_integration.py
  - Measure MP3 generation time
  - Measure OGG conversion time
  - Verify total time within 1.1-10.5 seconds

- [x] T025 Run full test suite in c:\Users\caste\source\repos\tts\tests\
  - pytest tests/ -v
  - Verify all tests pass
  - Check test coverage

- [x] T026 Update SKILL.md frontmatter in c:\Users\caste\source\repos\tts\SKILL.md
  - Update description to mention OGG support
  - Keep name: tts

- [x] T027 [P] Commit all changes to branch 006-ogg-output-option
  - git add -A
  - git commit -m "Add OGG output format option with pydub"

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion - Core feature
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion - Can run in parallel with US1
- **User Story 3 (Phase 5)**: Depends on US1 and US2 completion - Documentation reflects implemented features
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent from US1 (regression testing)
- **User Story 3 (P3)**: Depends on US1 and US2 completion - Documents the implemented features

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Implementation tasks run sequentially (dependencies on previous tasks)
- Tests can run in parallel [P] with each other
- Documentation tasks can run in parallel [P]

### Parallel Opportunities

- All Setup tasks (T001-T003) can run in parallel [P]
- All Foundational tasks (T004-T006) can run in parallel [P]
- All test tasks within a user story can run in parallel [P]
- US1 implementation and US2 testing can overlap (different code paths)
- All US3 documentation tasks (T019-T022) can run in parallel [P]
- Polish tasks can run in parallel [P]

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (write tests first):
Task: "test_format_argument_parsing in tests/test_tts.py"
Task: "test_ogg_file_generation in tests/test_audio_format.py"
Task: "test_extension_auto_correction in tests/test_tts.py"
Task: "test_ogg_conversion_errors in tests/test_tts.py"

# Then implement sequentially (tests will fail, implement to pass):
Task: "Implement convert_to_ogg function"
Task: "Update main execution flow"
Task: "Add error handling"
Task: "Add format validation"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (install pydub, verify ffmpeg)
2. Complete Phase 2: Foundational (add --format argument, validation, extension logic)
3. Complete Phase 3: User Story 1 (write tests → implement OGG generation)
4. **STOP and VALIDATE**: Test `python tts.py "hello" --format ogg` independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test backward compatibility → Verify no breakage
4. Add User Story 3 → Update documentation → Deploy/Demo
5. Add Polish → Integration tests → Final validation
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (OGG generation)
   - Developer B: User Story 2 (backward compatibility tests)
   - Developer C: User Story 3 (documentation updates)
3. Stories complete and integrate independently
4. Final integration: Polish phase

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD approach per constitution)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Total task count: 27 tasks
  - Setup: 3 tasks
  - Foundational: 3 tasks  
  - User Story 1: 8 tasks (4 tests + 4 implementation)
  - User Story 2: 4 tasks (2 tests + 2 implementation)
  - User Story 3: 4 tasks (documentation)
  - Polish: 5 tasks
- Parallel opportunities: ~15 tasks can run in parallel (marked with [P])
- Suggested MVP: Complete through User Story 1 (11 tasks total)
