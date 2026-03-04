# Tasks: Language Selection for TTS

**Input**: Design documents from `/specs/004-lang-selection/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-interface.md

**Tests**: Tests are included per Constitution Principle V (Test-First Development)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: No new infrastructure needed - modifying existing single-file CLI tool

- [x] T001 Review current tts.py implementation at c:\Users\caste\source\repos\tts\tts.py
- [x] T002 Review current test structure in c:\Users\caste\source\repos\tts\tests\

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core changes that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Add --lang argument to argparse in c:\Users\caste\source\repos\tts\tts.py with default='pt-br' and choices=['en', 'pt-br']
- [x] T004 Modify generate_speech() function signature in c:\Users\caste\source\repos\tts\tts.py to accept language parameter
- [x] T005 Update gTTS constructor call in c:\Users\caste\source\repos\tts\tts.py to use language parameter instead of hardcoded 'pt-br'
- [x] T006 Pass args.lang to generate_speech() in main() function in c:\Users\caste\source\repos\tts\tts.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Default Brazilian Portuguese Output (Priority: P1) 🎯 MVP

**Goal**: Ensure backward compatibility - users can run script without --lang argument and get pt-br audio

**Independent Test**: Run `python tts.py "Olá mundo"` without --lang argument and verify audio is in Brazilian Portuguese

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T007 [P] [US1] Write unit test for default language behavior in c:\Users\caste\source\repos\tts\tests\test_tts.py - verify args.lang defaults to 'pt-br' when not provided
- [x] T008 [P] [US1] Write integration test in c:\Users\caste\source\repos\tts\tests\test_integration.py - invoke script without --lang and verify gTTS called with lang='pt-br'

### Implementation for User Story 1

- [x] T009 [US1] Verify argparse default='pt-br' is set correctly in c:\Users\caste\source\repos\tts\tts.py
- [x] T010 [US1] Run unit tests to confirm default language behavior works
- [x] T011 [US1] Run integration test to confirm backward compatibility

**Checkpoint**: At this point, User Story 1 should be fully functional - existing scripts work without modification

---

## Phase 4: User Story 2 - Explicit Language Selection (Priority: P2)

**Goal**: Enable users to explicitly choose English or Brazilian Portuguese via --lang argument

**Independent Test**: Run `python tts.py "Hello world" --lang en` and verify audio is in English; run with `--lang pt-br` and verify Portuguese

### Tests for User Story 2

- [x] T012 [P] [US2] Write unit test for --lang en in c:\Users\caste\source\repos\tts\tests\test_tts.py - verify args.lang='en' when --lang en provided
- [x] T013 [P] [US2] Write unit test for --lang pt-br in c:\Users\caste\source\repos\tts\tests\test_tts.py - verify args.lang='pt-br' when --lang pt-br provided
- [x] T014 [P] [US2] Write integration test for English selection in c:\Users\caste\source\repos\tts\tests\test_integration.py - verify gTTS called with lang='en'
- [x] T015 [P] [US2] Write integration test for Portuguese selection in c:\Users\caste\source\repos\tts\tests\test_integration.py - verify gTTS called with lang='pt-br'

### Implementation for User Story 2

- [x] T016 [US2] Verify argparse choices=['en', 'pt-br'] restricts valid inputs in c:\Users\caste\source\repos\tts\tts.py
- [x] T017 [US2] Verify language parameter correctly passed from args.lang to generate_speech() in c:\Users\caste\source\repos\tts\tts.py
- [x] T018 [US2] Run all User Story 2 tests to confirm explicit language selection works
- [x] T019 [US2] Manual test: Generate English audio with --lang en and verify output
- [x] T020 [US2] Manual test: Generate Portuguese audio with --lang pt-br and verify output

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: Edge Cases & Error Handling

**Goal**: Handle invalid inputs gracefully with clear error messages

**Independent Test**: Run with invalid language codes and verify appropriate error messages

### Tests for Edge Cases

- [x] T021 [P] Write unit test for invalid language code in c:\Users\caste\source\repos\tts\tests\test_tts.py - verify exit code 1 and error message for --lang fr
- [x] T022 [P] Write unit test for missing language value in c:\Users\caste\source\repos\tts\tests\test_tts.py - verify error when --lang provided without value
- [x] T023 [P] Write unit test for case sensitivity in c:\Users\caste\source\repos\tts\tests\test_tts.py - verify --lang EN fails with error
- [x] T024 [P] Write unit test for help text in c:\Users\caste\source\repos\tts\tests\test_tts.py - verify --lang appears in help output with correct description

### Implementation for Edge Cases

- [x] T025 Verify argparse choices validation handles invalid codes automatically in c:\Users\caste\source\repos\tts\tts.py
- [x] T026 Run all edge case tests to confirm error handling works correctly
- [x] T027 Manual test: Verify error message quality for invalid language codes

**Checkpoint**: All error cases handled gracefully with helpful messages

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation and final validation

- [x] T028 [P] Update SKILL.md Usage section in c:\Users\caste\source\repos\tts\SKILL.md - add --lang examples
- [x] T029 [P] Update SKILL.md Inputs table in c:\Users\caste\source\repos\tts\SKILL.md - document --lang parameter with constraints
- [x] T030 [P] Update SKILL.md Examples section in c:\Users\caste\source\repos\tts\SKILL.md - show --lang en and --lang pt-br usage
- [x] T031 [P] Update SKILL.md Error Messages section in c:\Users\caste\source\repos\tts\SKILL.md - add invalid language code error example
- [x] T032 [P] Add language selection examples to SKILL.md Command-Line Options in c:\Users\caste\source\repos\tts\SKILL.md
- [x] T033 Run all tests to ensure nothing broken: pytest c:\Users\caste\source\repos\tts\tests\
- [x] T034 Validate against quickstart.md examples in c:\Users\caste\source\repos\tts\specs\004-lang-selection\quickstart.md
- [x] T035 Validate against CLI contract in c:\Users\caste\source\repos\tts\specs\004-lang-selection\contracts\cli-interface.md
- [x] T036 Manual end-to-end test: Run all examples from quickstart.md and verify outputs

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User Story 1 can proceed after Foundational
  - User Story 2 can proceed after Foundational (independent of US1)
  - Edge Cases can proceed after Foundational (independent of US1/US2)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on Foundational (Phase 2) - Independent of US1 (can run in parallel)
- **Edge Cases (Phase 5)**: Depends on Foundational (Phase 2) - Independent of US1/US2 (can run in parallel)

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Foundation changes before user story tests
- Tests before verification
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks (T001-T002) can run in parallel
- All Foundational tasks (T003-T006) are sequential (same file)
- All tests for User Story 1 (T007-T008) can run in parallel
- All tests for User Story 2 (T012-T015) can run in parallel
- All edge case tests (T021-T024) can run in parallel
- All documentation tasks (T028-T032) can run in parallel
- User Story 2 can be worked on in parallel with User Story 1 after Foundational phase

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Write unit test for default language behavior in tests/test_tts.py"
Task: "Write integration test - invoke script without --lang in tests/test_integration.py"
```

## Parallel Example: User Story 2

```bash
# Launch all tests for User Story 2 together:
Task: "Write unit test for --lang en in tests/test_tts.py"
Task: "Write unit test for --lang pt-br in tests/test_tts.py"
Task: "Write integration test for English selection in tests/test_integration.py"
Task: "Write integration test for Portuguese selection in tests/test_integration.py"
```

## Parallel Example: Documentation

```bash
# Launch all documentation updates together:
Task: "Update SKILL.md Usage section"
Task: "Update SKILL.md Inputs table"
Task: "Update SKILL.md Examples section"
Task: "Update SKILL.md Error Messages section"
Task: "Add language selection examples to SKILL.md Command-Line Options"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T006) - CRITICAL
3. Complete Phase 3: User Story 1 (T007-T011)
4. **STOP and VALIDATE**: Test backward compatibility independently
5. Deploy/demo if ready - existing scripts work without modification

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (T001-T006)
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!) (T007-T011)
3. Add User Story 2 → Test independently → Deploy/Demo (T012-T020)
4. Add Edge Cases → Test independently (T021-T027)
5. Polish & Documentation → Final release (T028-T036)

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T006)
2. Once Foundational is done:
   - Developer A: User Story 1 (T007-T011)
   - Developer B: User Story 2 (T012-T020)
   - Developer C: Edge Cases (T021-T027)
3. All converge on Polish & Documentation (T028-T036)

---

## Task Summary

**Total Tasks**: 36

**By Phase**:
- Phase 1 (Setup): 2 tasks
- Phase 2 (Foundational): 4 tasks
- Phase 3 (User Story 1): 5 tasks
- Phase 4 (User Story 2): 9 tasks
- Phase 5 (Edge Cases): 7 tasks
- Phase 6 (Polish): 9 tasks

**By User Story**:
- User Story 1 (Default pt-br): 5 tasks
- User Story 2 (Explicit selection): 9 tasks
- Edge Cases: 7 tasks
- Infrastructure: 6 tasks
- Documentation: 9 tasks

**Parallel Opportunities**:
- 2 tasks in Setup (T001-T002)
- 2 test tasks in US1 (T007-T008)
- 4 test tasks in US2 (T012-T015)
- 4 test tasks in Edge Cases (T021-T024)
- 5 documentation tasks (T028-T032)
- **Total parallelizable**: 17 tasks

**Critical Path**: Setup → Foundational → User Story 1 → User Story 2 → Edge Cases → Polish

**MVP Scope**: Phases 1-3 (Tasks T001-T011) = 11 tasks

---

## Notes

- [P] tasks = different files or independent work, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Write tests first, ensure they fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Single-file modification keeps complexity minimal
- Backward compatibility is critical - User Story 1 validates this
