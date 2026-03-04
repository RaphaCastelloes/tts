# Feature Specification: OGG-Only Audio Output

**Feature Branch**: `003-ogg-only-output`  
**Created**: March 3, 2026  
**Status**: Draft  
**Input**: User description: "let the output format only in ogg"

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

### User Story 1 - Generate OGG Audio Files (Priority: P1)

As a WhatsApp bot developer, I need the TTS script to generate audio files in OGG/Opus format so that the audio files are optimized for WhatsApp voice messaging with smaller file sizes and better compression.

**Why this priority**: This is the core functionality change. OGG/Opus is the standard audio codec for WhatsApp voice messages and provides better compression than MP3, resulting in smaller file sizes and faster transmission.

**Independent Test**: Run the script with any text input and verify the output file is in OGG container format with Opus codec. File should play correctly in WhatsApp on both Android and iOS devices.

**Acceptance Scenarios**:

1. **Given** the TTS script is installed, **When** I run `python tts.py "hello world"`, **Then** an OGG file is created in the output directory
2. **Given** I have an OGG output file, **When** I inspect the file format, **Then** it shows OGG container with Opus codec
3. **Given** I have a generated OGG file, **When** I send it via WhatsApp, **Then** it plays correctly as a voice message

---

### User Story 2 - Maintain Custom Output Path Support (Priority: P2)

As a bot developer, I need to specify custom output paths for OGG files so that I can organize audio files according to my bot's file structure requirements.

**Why this priority**: The recent addition of custom output path support is valuable functionality that should be preserved when switching to OGG format.

**Independent Test**: Use the `-o` flag to specify a custom output path and verify the OGG file is created at the specified location with .ogg extension.

**Acceptance Scenarios**:

1. **Given** I use the `-o` flag, **When** I run `python tts.py "hello" -o custom.ogg`, **Then** the file is created at the specified path with OGG format
2. **Given** I specify a path without extension, **When** I run `python tts.py "hello" -o myfile`, **Then** the system automatically adds .ogg extension
3. **Given** I specify a path with .mp3 extension, **When** the script runs, **Then** it replaces the extension with .ogg

---

### User Story 3 - Backward Compatible File Naming (Priority: P3)

As a system administrator, I need the generated OGG files to follow the existing naming convention so that my existing scripts and automation continue to work with the new format.

**Why this priority**: Maintains compatibility with existing integrations while only changing the file extension and format.

**Independent Test**: Generate multiple files and verify they follow the pattern `tts_YYYYMMDD_HHMMSS_<hash>.ogg` with unique timestamps and hashes.

**Acceptance Scenarios**:

1. **Given** I generate an audio file, **When** I check the filename, **Then** it follows the pattern `tts_YYYYMMDD_HHMMSS_<hash>.ogg`
2. **Given** I generate multiple files, **When** I inspect the filenames, **Then** each has a unique timestamp and hash
3. **Given** existing automation expects timestamp-based filenames, **When** I integrate the new OGG files, **Then** the automation continues to work with only extension changes

### Edge Cases

- What happens when the user specifies a custom output path with a .mp3 extension? (System should replace with .ogg)
- How does the system handle existing MP3 files in the output directory? (They remain untouched, new files are OGG)
- What happens if audio conversion dependencies (pydub, ffmpeg) are not installed? (Clear error message with installation instructions)
- How does the system behave if the gTTS service is unavailable? (Existing network error handling applies)
- What happens with very long text that generates large audio files? (OGG compression handles this more efficiently than MP3)

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST generate audio files in OGG container format with Opus codec
- **FR-002**: System MUST convert gTTS MP3 output to OGG/Opus format automatically
- **FR-003**: System MUST set audio sample rate to 16kHz (WhatsApp standard)
- **FR-004**: System MUST output mono channel audio (single channel)
- **FR-005**: System MUST maintain existing file naming pattern with .ogg extension
- **FR-006**: System MUST support custom output paths with automatic .ogg extension handling
- **FR-007**: System MUST provide clear error messages if conversion dependencies are missing
- **FR-008**: System MUST validate generated OGG files are WhatsApp-compatible
- **FR-009**: System MUST maintain backward compatibility with all existing command-line arguments
- **FR-010**: System MUST update all documentation to reflect OGG output format

### Key Entities

- **AudioFile**: Generated OGG audio file with attributes: file path, file name, format (OGG/Opus), sample rate (16kHz), channels (mono), file size, duration
- **ConversionJob**: Represents the process of converting gTTS MP3 output to OGG/Opus format, with states: generating TTS, encoding audio, saving file, complete, failed

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: All generated audio files are in OGG/Opus format (100% compliance)
- **SC-002**: Generated OGG files are 30-50% smaller than equivalent MP3 files
- **SC-003**: Audio generation completes in under 10 seconds for typical messages (up to 500 characters)
- **SC-004**: Generated OGG files play successfully in WhatsApp on both Android and iOS devices (100% compatibility)
- **SC-005**: All existing command-line functionality remains operational after format change
- **SC-006**: File naming convention remains consistent, only extension changes from .mp3 to .ogg
