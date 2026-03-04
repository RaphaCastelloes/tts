# Research: Language Selection for TTS

**Feature**: 004-lang-selection  
**Date**: 2026-03-04  
**Status**: Complete

## Overview

Research findings for adding command-line language selection to the TTS script with pt-br as default and support for en via --lang argument.

## Research Areas

### 1. gTTS Language Support

**Question**: What language codes does gTTS support and how are they specified?

**Findings**:
- gTTS uses ISO 639-1 language codes (2-letter codes)
- Brazilian Portuguese: `'pt-br'` (with regional variant)
- English: `'en'` (defaults to US English)
- Language is passed via `lang` parameter to gTTS constructor
- Invalid language codes raise `ValueError` with message about unsupported language

**Decision**: Use exact codes `'pt-br'` and `'en'` as specified in requirements

**Rationale**: 
- These codes are already supported by gTTS 2.5.0
- No additional dependencies or configuration needed
- Clear distinction between Brazilian Portuguese and other Portuguese variants

**Alternatives Considered**:
- Using `'pt'` for Portuguese: Rejected because it defaults to European Portuguese, not Brazilian
- Supporting all gTTS languages: Rejected to keep scope minimal and focused on user requirements

### 2. Argument Parsing Pattern

**Question**: What's the best practice for adding optional language argument with default value?

**Findings**:
- argparse already in use in tts.py for text and --output arguments
- `add_argument()` with `default` parameter provides clean default value handling
- `choices` parameter can restrict valid inputs and auto-generate error messages
- Help text automatically generated for --help output

**Decision**: Use argparse with default='pt-br' and choices=['en', 'pt-br']

**Rationale**:
- Consistent with existing argument parsing pattern
- Built-in validation via choices parameter
- Automatic help text generation
- No additional dependencies

**Implementation Pattern**:
```python
parser.add_argument(
    '--lang',
    default='pt-br',
    choices=['en', 'pt-br'],
    help='Language for speech output (default: pt-br)'
)
```

**Alternatives Considered**:
- Environment variable: Rejected because CLI argument is more explicit and discoverable
- Config file: Rejected as over-engineering for 2 language options
- Manual validation: Rejected because argparse choices provides better UX

### 3. Backward Compatibility Strategy

**Question**: How to ensure existing scripts continue working without modification?

**Findings**:
- Default parameter values in argparse are only used when argument not provided
- Existing invocations like `python tts.py "text"` will use default='pt-br'
- No breaking changes to existing argument structure
- Help text will show new optional argument

**Decision**: Use default='pt-br' parameter, making --lang completely optional

**Rationale**:
- Zero impact on existing usage patterns
- Existing scripts get pt-br behavior automatically
- Users can opt-in to language selection when needed

**Alternatives Considered**:
- Requiring --lang always: Rejected as breaking change
- Auto-detecting language from text: Rejected as unreliable and out of scope

### 4. Error Handling for Invalid Languages

**Question**: How should invalid language codes be handled?

**Findings**:
- argparse `choices` parameter automatically validates input
- Invalid choice triggers SystemExit with clear error message
- Error message format: "invalid choice: 'xx' (choose from 'en', 'pt-br')"
- Caught by existing try/except SystemExit block in main()

**Decision**: Rely on argparse choices validation, no custom error handling needed

**Rationale**:
- Automatic validation with clear error messages
- Consistent with existing error handling pattern
- Exit code 1 (EXIT_INPUT_ERROR) already appropriate

**Alternatives Considered**:
- Custom validation function: Rejected as redundant with argparse choices
- Allowing any language and catching gTTS errors: Rejected as poor UX (fails late)

### 5. Testing Strategy

**Question**: What test cases are needed to validate language selection?

**Findings**:
- Need to test default behavior (no --lang argument)
- Need to test explicit language selection (--lang en, --lang pt-br)
- Need to test invalid language code handling
- Can mock gTTS to avoid network calls in unit tests
- Integration tests should verify actual audio generation

**Decision**: Add unit tests for argument parsing, integration tests for audio generation

**Test Cases Required**:
1. **Default language**: Invoke without --lang, verify pt-br used
2. **Explicit pt-br**: Invoke with --lang pt-br, verify pt-br used
3. **Explicit en**: Invoke with --lang en, verify en used
4. **Invalid language**: Invoke with --lang xx, verify error message and exit code 1
5. **Help text**: Verify --lang appears in help output with correct description

**Rationale**:
- Covers all acceptance scenarios from spec
- Tests both happy path and error cases
- Validates backward compatibility

### 6. Documentation Updates

**Question**: What documentation needs to be updated?

**Findings**:
- SKILL.md has Usage section showing command examples
- SKILL.md has Inputs table documenting parameters
- SKILL.md has Examples section showing various invocations
- Help text auto-generated from argparse

**Decision**: Update SKILL.md Usage, Inputs, and Examples sections

**Updates Required**:
1. Add --lang to command-line options section
2. Add --lang to inputs table with constraints
3. Add examples showing --lang en and --lang pt-br usage
4. Update description to mention default pt-br language
5. Add error message example for invalid language code

**Rationale**:
- Maintains documentation completeness per Constitution Principle I
- Helps users discover and use new feature
- Documents default behavior explicitly

## Summary

All research complete with no blockers identified. The implementation is straightforward:

1. Add `--lang` argument to argparse with `default='pt-br'` and `choices=['en', 'pt-br']`
2. Pass language argument to gTTS constructor
3. Update tests to cover language selection scenarios
4. Update SKILL.md documentation

No new dependencies, no breaking changes, full backward compatibility maintained.
