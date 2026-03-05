# Feature Specification: OGG Output Option

**Feature Branch**: `006-ogg-output-option`  
**Created**: 2026-03-05  
**Status**: Draft  
**Input**: User description: "merge mp3-to-ogg skill and scripts in the workflow of the tts skill as a new configuration of output"

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

### User Story 1 - Generate OGG Audio Directly (Priority: P1)

As a bot developer, I want to generate OGG format audio files directly from the TTS skill using a command-line flag, so that I can eliminate the need for a separate mp3-to-ogg conversion step in the WhatsApp bot workflow.

**Why this priority**: This is the core feature that simplifies the bot workflow by consolidating two steps into one, reducing complexity and potential failure points.

**Independent Test**: Can be fully tested by running `python tts.py "test text" --format ogg` and verifying that a valid OGG file is generated and the file path is returned on stdout.

**Acceptance Scenarios**:

1. **Given** the TTS skill is installed, **When** I run `python tts.py "hello" --format ogg`, **Then** an OGG audio file is generated in the output directory
2. **Given** I specify OGG format, **When** the conversion completes, **Then** the absolute path to the OGG file is printed to stdout
3. **Given** I specify OGG format with custom output path, **When** I run `python tts.py "hello" --format ogg -o myfile`, **Then** a file named `myfile.ogg` is created

---

### User Story 2 - Maintain MP3 as Default Format (Priority: P2)

As a bot developer, I want MP3 to remain the default output format when no format is specified, so that existing integrations continue to work without modification.

**Why this priority**: Backward compatibility is critical to avoid breaking existing bot workflows that depend on MP3 output.

**Independent Test**: Can be fully tested by running `python tts.py "test text"` without format flag and verifying that an MP3 file is generated (existing behavior preserved).

**Acceptance Scenarios**:

1. **Given** no format flag is specified, **When** I run `python tts.py "hello"`, **Then** an MP3 file is generated (default behavior)
2. **Given** I explicitly specify MP3 format, **When** I run `python tts.py "hello" --format mp3`, **Then** an MP3 file is generated
3. **Given** existing scripts use the tool without format flag, **When** they execute, **Then** they continue to receive MP3 files as before

---

### User Story 3 - Update Documentation for New Workflow (Priority: P3)

As a bot developer, I want updated SKILL.md documentation that reflects the simplified workflow with direct OGG generation, so that I understand how to use the new capability.

**Why this priority**: Documentation updates ensure developers can discover and use the new feature, but the feature itself works without documentation updates.

**Independent Test**: Can be fully tested by reviewing SKILL.md and verifying it shows the new `--format` option and updated workflow that no longer requires a separate mp3-to-ogg skill.

**Acceptance Scenarios**:

1. **Given** the feature is implemented, **When** I read SKILL.md, **Then** I see the `--format` option documented with examples
2. **Given** I read the Bot Integration Use Case section, **When** I review the workflow steps, **Then** I see the workflow shows direct OGG generation without the mp3-to-ogg conversion step
3. **Given** I need usage examples, **When** I read the Examples section, **Then** I see examples showing both MP3 and OGG output

### Edge Cases

- What happens when an invalid format is specified (e.g., `--format wav`)?
  - System should return error with message listing valid formats: mp3, ogg
  - Exit code should be 1 (input error)
- What happens when OGG conversion fails due to missing dependencies?
  - System should return clear error message indicating pydub or ffmpeg issue
  - Exit code should be 4 (processing error)
- What happens when user specifies `.mp3` extension with `--format ogg`?
  - System should respect the format flag and generate OGG file, ignoring extension mismatch
  - Or alternatively, auto-correct extension to match format
- What happens when very long text is converted to OGG?
  - Should work the same as MP3 (up to 1000 character limit)
  - OGG file size may differ from MP3 but should still be reasonable

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST accept a `--format` command-line argument with values `mp3` or `ogg`
- **FR-002**: System MUST default to MP3 format when no `--format` argument is provided (backward compatibility)
- **FR-003**: System MUST generate OGG format audio files when `--format ogg` is specified
- **FR-004**: System MUST generate MP3 format audio files when `--format mp3` is specified or when no format is specified
- **FR-005**: System MUST return the absolute file path of the generated audio file to stdout
- **FR-006**: System MUST auto-append the correct file extension (.ogg or .mp3) based on the selected format if not provided in output path
- **FR-007**: System MUST validate the format argument and reject invalid values with a clear error message
- **FR-008**: System MUST maintain all existing functionality (language selection, custom output paths, text validation) regardless of format
- **FR-009**: System MUST generate WhatsApp-compatible OGG files (Opus codec in OGG container)
- **FR-010**: System MUST handle format conversion errors gracefully with appropriate error messages and exit codes

### Key Entities

- **Audio Output**: Generated audio file in either MP3 or OGG format, with attributes: file path, format type, file size, duration
- **Format Configuration**: User-specified output format preference (mp3 or ogg), determines conversion pipeline and file extension

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Users can generate OGG audio files with a single command execution (no separate conversion step required)
- **SC-002**: OGG file generation completes within the same time range as MP3 generation (1-10 seconds depending on text length)
- **SC-003**: Generated OGG files are playable in WhatsApp on both Android and iOS devices
- **SC-004**: Existing MP3-based integrations continue to work without any code changes (100% backward compatibility)
- **SC-005**: Bot workflow complexity is reduced from 6 steps to 5 steps (eliminates separate mp3-to-ogg conversion step)
- **SC-006**: Invalid format specifications are caught and reported with clear error messages (100% of invalid inputs rejected with helpful feedback)
