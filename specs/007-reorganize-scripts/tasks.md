# Tasks: Reorganize Scripts and Unify Documentation

**Input**: Design documents from `/specs/007-reorganize-scripts/`
**Prerequisites**: plan.md, spec.md, research.md

**Tests**: No new tests required. This is a pure refactoring task - existing tests must continue to pass after reorganization.

**Organization**: Tasks grouped by user story to enable independent implementation and testing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization - create new directory structure

- [ ] T001 Create c:\Users\caste\source\repos\tts\scripts directory
- [ ] T002 Verify git is in clean state before file moves (git status)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No foundational tasks needed - this is a pure refactoring with independent user stories

**Note**: All three user stories (US1, US2, US3) can be implemented independently after Setup phase completes.

---

## Phase 3: User Story 1 - Organize Scripts in Standard Location (Priority: P1) 🎯 MVP

**Goal**: Move all executable scripts to `/scripts` directory following Python project conventions

**Independent Test**: Run `python scripts/tts.py "test" --lang en` and verify it generates audio successfully. Verify `tts.py` no longer exists at root.

### Implementation for User Story 1

- [ ] T003 [US1] Move tts.py to scripts/ using git mv c:\Users\caste\source\repos\tts\tts.py c:\Users\caste\source\repos\tts\scripts\tts.py
- [ ] T004 [US1] Move convert_mp3_to_ogg.py to scripts/ using git mv c:\Users\caste\source\repos\tts\mp3-to-ogg\scripts\convert_mp3_to_ogg.py c:\Users\caste\source\repos\tts\scripts\convert_mp3_to_ogg.py
- [ ] T005 [US1] Update test imports in c:\Users\caste\source\repos\tts\tests\test_tts.py to reference scripts/ location
- [ ] T006 [US1] Update test imports in c:\Users\caste\source\repos\tts\tests\test_audio_format.py to reference scripts/ location
- [ ] T007 [US1] Update test imports in c:\Users\caste\source\repos\tts\tests\test_integration.py to reference scripts/ location
- [ ] T008 [US1] Verify all tests pass after script relocation: pytest tests/ -v
- [ ] T009 [US1] Test script execution from new location: python scripts/tts.py "hello" --lang en
- [ ] T010 [US1] Test OGG conversion from new location: python scripts/tts.py "hello" --format ogg --lang en

**Checkpoint**: User Story 1 complete - Scripts organized in standard `/scripts` directory, all tests passing

---

## Phase 4: User Story 2 - Unified Documentation (Priority: P2)

**Goal**: Merge README.md content into SKILL.md and simplify README.md to brief overview

**Independent Test**: Review SKILL.md and verify it contains Quick Start, Features, and all sections from both previous files. Verify README.md is under 50 lines with link to SKILL.md.

### Implementation for User Story 2

- [ ] T011 [P] [US2] Extract Quick Start section from c:\Users\caste\source\repos\tts\README.md (lines 7-33)
- [ ] T012 [P] [US2] Extract Features list from c:\Users\caste\source\repos\tts\README.md (lines 35-41)
- [ ] T013 [P] [US2] Extract Project Structure from c:\Users\caste\source\repos\tts\README.md (lines 56-69)
- [ ] T014 [US2] Insert Quick Start section into c:\Users\caste\source\repos\tts\SKILL.md after Purpose section (after line 26)
- [ ] T015 [US2] Insert Features section into c:\Users\caste\source\repos\tts\SKILL.md as new section before Usage
- [ ] T016 [US2] Update Project Structure diagram in c:\Users\caste\source\repos\tts\SKILL.md to show new scripts/ directory layout
- [ ] T017 [US2] Update all usage examples in c:\Users\caste\source\repos\tts\SKILL.md to reference scripts/tts.py instead of tts.py
- [ ] T018 [US2] Add Migration Notes section to c:\Users\caste\source\repos\tts\SKILL.md showing old vs new paths
- [ ] T019 [US2] Rewrite c:\Users\caste\source\repos\tts\README.md to simplified version (< 50 lines) with overview and link to SKILL.md
- [ ] T020 [US2] Verify SKILL.md contains all necessary sections and is self-contained
- [ ] T021 [US2] Verify README.md is concise and links correctly to SKILL.md

**Checkpoint**: User Story 2 complete - Documentation unified in SKILL.md, README.md simplified

---

## Phase 5: User Story 3 - Remove Obsolete mp3-to-ogg Folder (Priority: P3)

**Goal**: Remove obsolete `/mp3-to-ogg` folder since OGG conversion is now integrated in tts.py

**Independent Test**: Verify `/mp3-to-ogg` folder no longer exists. Verify git history documents the removal.

### Implementation for User Story 3

- [ ] T022 [US3] Remove mp3-to-ogg folder using git rm -r c:\Users\caste\source\repos\tts\mp3-to-ogg
- [ ] T023 [US3] Verify folder is completely removed: ls c:\Users\caste\source\repos\tts\mp3-to-ogg should fail
- [ ] T024 [US3] Add note in c:\Users\caste\source\repos\tts\SKILL.md Migration Notes that mp3-to-ogg is replaced by --format ogg

**Checkpoint**: User Story 3 complete - Obsolete code removed, migration documented

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and commit

- [ ] T025 Run full test suite to verify 100% compatibility: pytest tests/ -v
- [ ] T026 Test MP3 generation: python scripts/tts.py "final test" --lang en
- [ ] T027 Test OGG generation: python scripts/tts.py "final test" --format ogg --lang en
- [ ] T028 Verify project structure matches plan.md diagram
- [ ] T029 Verify all documentation paths reference scripts/tts.py correctly
- [ ] T030 Verify git history preserved for moved files: git log --follow scripts/tts.py
- [ ] T031 Commit all changes with descriptive message

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **User Story 1 (Phase 3)**: Depends on Setup completion - Core reorganization
- **User Story 2 (Phase 4)**: Independent of US1 - Can run in parallel or after
- **User Story 3 (Phase 5)**: Independent of US1 and US2 - Can run in parallel
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Setup - No dependencies on other stories
- **User Story 2 (P2)**: Independent of US1 (different files) - Can run in parallel with US1
- **User Story 3 (P3)**: Independent of US1 and US2 - Can run in parallel with both

**Key Independence**: All three user stories work on different files and can be implemented/tested independently:
- US1: Scripts and test files
- US2: Documentation files (SKILL.md, README.md)
- US3: mp3-to-ogg folder removal

### Within Each User Story

- US1: Must move scripts before updating test imports
- US2: Must extract content before merging, merge before simplifying README
- US3: Single task - remove folder

### Parallel Opportunities

- T001-T002 (Setup) can run in parallel
- T011-T013 (Extract documentation sections) can run in parallel [P]
- After Setup: US1, US2, US3 can all run in parallel (different files)
- T025-T027 (Final testing) can run in parallel

---

## Parallel Example: User Stories

```bash
# After Setup completes, all user stories can proceed in parallel:

Developer A works on User Story 1:
- Move tts.py to scripts/
- Move convert_mp3_to_ogg.py to scripts/
- Update test imports
- Verify tests pass

Developer B works on User Story 2:
- Extract sections from README.md
- Merge into SKILL.md
- Simplify README.md

Developer C works on User Story 3:
- Remove mp3-to-ogg folder
- Update migration notes

All three can work simultaneously without conflicts.
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (create scripts directory)
2. Complete Phase 3: User Story 1 (move scripts, update imports)
3. **STOP and VALIDATE**: Test `python scripts/tts.py "test"` independently
4. Verify all tests pass
5. MVP complete - can use reorganized structure

### Incremental Delivery

1. Complete Setup → Scripts directory ready
2. Add User Story 1 → Test independently → Scripts reorganized (MVP!)
3. Add User Story 2 → Test independently → Documentation unified
4. Add User Story 3 → Test independently → Obsolete code removed
5. Polish → Final validation → Complete

### Parallel Team Strategy

With multiple developers:

1. One person completes Setup (T001-T002)
2. Once Setup is done:
   - Developer A: User Story 1 (scripts reorganization)
   - Developer B: User Story 2 (documentation unification)
   - Developer C: User Story 3 (cleanup)
3. Stories complete independently
4. Final integration: Polish phase validates everything together

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No new tests required - existing tests must pass after refactoring
- Use `git mv` to preserve file history (critical for traceability)
- Commit after completing each user story
- Stop at any checkpoint to validate story independently
- Total task count: 31 tasks
  - Setup: 2 tasks
  - User Story 1: 8 tasks (script reorganization)
  - User Story 2: 11 tasks (documentation unification)
  - User Story 3: 3 tasks (cleanup)
  - Polish: 7 tasks (final validation)
- Parallel opportunities: ~15 tasks can run in parallel
- Suggested MVP: Complete through User Story 1 (10 tasks total)
- Estimated time: 45 minutes total (per quickstart.md)
