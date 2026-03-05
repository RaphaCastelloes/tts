# Feature Specification: Reorganize Scripts and Unify Documentation

**Feature Branch**: `007-reorganize-scripts`  
**Created**: 2026-03-05  
**Status**: Draft  
**Input**: User description: "create a /scripts folder inside the skill main directory to include the tts.py and convert-mp3-to-ogg.py in this folder. Then merge the content of README.md and SKILL.md. This module documentation and script location must be uniform."

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Organize Scripts in Standard Location (Priority: P1)

As a developer, I want all executable scripts organized in a standard `/scripts` folder, so that the project structure follows common conventions and scripts are easy to locate.

**Why this priority**: Establishes proper project organization that makes the skill easier to understand, maintain, and use. This is foundational for project cleanliness.

**Independent Test**: Can be fully tested by verifying that `scripts/tts.py` and `scripts/convert_mp3_to_ogg.py` exist and are executable, and that running `python scripts/tts.py "test"` works correctly.

**Acceptance Scenarios**:

1. **Given** the TTS skill repository, **When** I navigate to the root directory, **Then** I see a `/scripts` folder containing all executable Python scripts
2. **Given** scripts are in the `/scripts` folder, **When** I run `python scripts/tts.py "hello"`, **Then** the script executes successfully and generates audio
3. **Given** the reorganized structure, **When** I check the project root, **Then** `tts.py` no longer exists at the root level

---

### User Story 2 - Unified Documentation (Priority: P2)

As a developer, I want a single comprehensive documentation file that merges README.md and SKILL.md content, so that I don't have to search multiple files for information.

**Why this priority**: Eliminates documentation fragmentation and provides a single source of truth for skill usage and reference.

**Independent Test**: Can be fully tested by reviewing SKILL.md and confirming it contains all essential information previously split between README.md and SKILL.md, including quick start, features, and detailed usage.

**Acceptance Scenarios**:

1. **Given** the merged documentation, **When** I open SKILL.md, **Then** I see Quick Start section (from README.md) merged with detailed documentation
2. **Given** unified SKILL.md, **When** I look for installation instructions, **Then** I find them without needing to check README.md
3. **Given** the reorganization, **When** README.md exists, **Then** it contains only a brief description and link to SKILL.md

---

### User Story 3 - Remove Obsolete mp3-to-ogg Folder (Priority: P3)

As a developer, I want the obsolete `/mp3-to-ogg` folder removed, so that the repository only contains actively used code and documentation.

**Why this priority**: Cleans up deprecated code now that OGG conversion is integrated into tts.py via `--format ogg` option.

**Independent Test**: Can be fully tested by verifying the `/mp3-to-ogg` folder no longer exists in the repository.

**Acceptance Scenarios**:

1. **Given** the feature implementation, **When** I list the root directory, **Then** I do not see an `mp3-to-ogg` folder
2. **Given** the cleanup, **When** I check git history, **Then** the removal is documented in commit message
3. **Given** the removed folder, **When** users need OGG conversion, **Then** they use `python scripts/tts.py --format ogg` instead

### Edge Cases

- What happens when documentation references old script paths?
  - All documentation must be updated to reference `scripts/tts.py` instead of `tts.py`
  - Examples in SKILL.md must show correct paths
- What happens to existing imports or references?
  - Test files must be updated to import from new script locations
  - Git history preserves file movement for traceability
- What happens to existing working directories in external scripts?
  - Users may have hardcoded paths to `tts.py` at root
  - Migration notes should be added to README.md

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: All executable Python scripts MUST be located in `/scripts` directory
- **FR-002**: SKILL.md MUST contain all documentation content previously split between README.md and SKILL.md
- **FR-003**: README.md MUST be simplified to contain only project overview and link to SKILL.md
- **FR-004**: All documentation examples MUST reference `scripts/tts.py` path
- **FR-005**: Project structure MUST follow standard Python project layout conventions
- **FR-006**: The `/mp3-to-ogg` folder MUST be removed from the repository
- **FR-007**: All tests MUST continue to pass after reorganization
- **FR-008**: Git history MUST preserve file movement (use `git mv` for tracking)
- **FR-009**: SKILL.md MUST include project structure diagram showing new layout
- **FR-010**: Migration notes MUST be added for users with existing references to old paths

### Key Entities

- **Scripts Directory**: Contains all executable Python files (tts.py, convert_mp3_to_ogg.py), serves as standard location for skill executables
- **Unified Documentation**: Single SKILL.md file containing complete skill documentation, combines content from previous README.md and SKILL.md
- **Project Structure**: Organized layout following Python project conventions with clear separation of scripts, tests, docs, and output

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: All executable scripts are located in `/scripts` directory (100% of Python executables moved)
- **SC-002**: SKILL.md contains all necessary documentation (no need to reference multiple files)
- **SC-003**: README.md is simplified to under 50 lines with clear link to SKILL.md
- **SC-004**: All existing tests pass after reorganization (100% test compatibility maintained)
- **SC-005**: Project structure follows standard Python conventions (passes structure validation)
- **SC-006**: No obsolete code remains in repository (`/mp3-to-ogg` folder removed)
- **SC-007**: All documentation references use correct script paths (`scripts/tts.py`)
