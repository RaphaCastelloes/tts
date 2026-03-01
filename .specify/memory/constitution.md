<!--
Sync Impact Report:
- Version: 1.0.0 → 1.0.1 (PATCH: Platform constraint clarification)
- Modified principles: None
- Added sections: Platform & Runtime Constraints
- Removed sections: None
- Clarifications: Added Oracle Linux as target platform with specific requirements
- Templates requiring updates:
  ✅ constitution-template.md (source template)
  ✅ plan-template.md (Target Platform field now has concrete value)
  ✅ spec-template.md (No changes required)
  ✅ tasks-template.md (No changes required)
- Follow-up TODOs: None
- Amendment Notes:
  * Added Platform & Runtime Constraints section specifying Oracle Linux target
  * Clarified Python version and system-level dependency requirements
  * No principle changes - purely additive constraint documentation
-->

# TTS Skill Constitution

## Core Principles

### I. Skill-Centric Architecture
Every feature must be implemented as a self-contained skill with:
- A SKILL.md file documenting purpose, usage, inputs, outputs, and dependencies
- A single executable Python script (tts.py) that implements the core functionality
- Clear separation between skill logic and external integrations
- No hidden dependencies or undocumented requirements

**Rationale**: Skills must be portable, reusable, and independently testable. Documentation-first approach ensures clarity and maintainability.

### II. Text I/O Protocol
All skill interactions MUST follow a text-based input/output protocol:
- Accept input via command-line arguments or stdin
- Produce output to stdout (results) and stderr (errors/logs)
- Support both JSON and human-readable formats where applicable
- No GUI dependencies or interactive prompts in core functionality

**Rationale**: Text I/O ensures debuggability, composability with other tools, and automation-friendly interfaces.

### III. Minimal Dependencies
Dependencies must be:
- Explicitly declared in requirements.txt or similar dependency manifest
- Justified with clear rationale in SKILL.md
- Kept to minimum necessary for core functionality
- Versioned and pinned to avoid breaking changes

**Rationale**: Reduces maintenance burden, improves portability, and minimizes security surface area.

### IV. Error Handling & Observability
All code MUST implement:
- Explicit error handling with descriptive messages
- Structured logging to stderr for debugging
- Clear exit codes (0 for success, non-zero for failures)
- Input validation with helpful error messages

**Rationale**: Skills must fail gracefully and provide actionable feedback for troubleshooting.

### V. Test-First Development
Testing requirements:
- Unit tests written before implementation (TDD approach)
- Integration tests for external API/service interactions
- Test coverage for error conditions and edge cases
- Tests must be runnable independently without manual setup

**Rationale**: Ensures reliability, prevents regressions, and documents expected behavior.

## Documentation Standards

All skills MUST maintain:
- **SKILL.md**: Complete documentation including purpose, usage examples, inputs/outputs, dependencies, error codes, and troubleshooting
- **Inline comments**: For complex logic, algorithms, or non-obvious decisions
- **Version history**: Track changes and breaking modifications
- **Example usage**: Concrete examples in SKILL.md showing common use cases

Documentation must be updated atomically with code changes.

## Platform & Runtime Constraints

**Target Platform**: Oracle Linux

All code MUST be compatible with Oracle Linux environment:
- Python 3.8+ (use version available in Oracle Linux repositories)
- No platform-specific dependencies that conflict with Oracle Linux
- System-level dependencies must be installable via yum/dnf package manager
- File paths must use POSIX conventions (forward slashes)
- Line endings must be LF (Unix-style), not CRLF

**Runtime Requirements**:
- Skill must run without graphical environment (headless execution)
- No assumptions about specific Oracle Linux version unless explicitly documented
- System dependencies must be documented in SKILL.md with installation commands
- Environment variables must be documented if required

**Testing on Target Platform**:
- Integration tests should verify Oracle Linux compatibility where feasible
- Document any Oracle Linux-specific behaviors or limitations
- Provide Oracle Linux installation/setup instructions in SKILL.md

## Development Workflow

### Implementation Process
1. Define or update SKILL.md specification
2. Write tests for new functionality
3. Implement code to pass tests
4. Update documentation for any changes
5. Verify all tests pass before commit

### Code Review Requirements
- All changes must include updated tests
- SKILL.md must reflect current functionality
- No commented-out code or debug statements in production
- Follow PEP 8 style guidelines for Python code

### Quality Gates
- All tests must pass
- No unhandled exceptions in normal operation
- Dependencies must be declared and justified
- Documentation must be complete and accurate

## Governance

This constitution supersedes all other development practices and guidelines.

**Amendment Process**:
- Amendments require documented rationale and impact analysis
- Version must be incremented following semantic versioning
- All dependent templates and documentation must be updated
- Changes must be reviewed before adoption

**Compliance**:
- All code reviews must verify constitutional compliance
- Deviations require explicit justification and approval
- Complexity must be justified against simplicity principle
- Use `.specify/templates/` for development guidance templates

**Enforcement**:
- Constitution violations block merge/deployment
- Regular audits to ensure ongoing compliance
- Retroactive fixes required for discovered violations

**Version**: 1.0.1 | **Ratified**: 2026-02-28 | **Last Amended**: 2026-02-28
