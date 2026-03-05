# Research: Reorganize Scripts and Unify Documentation

**Feature**: 007-reorganize-scripts  
**Date**: 2026-03-05  
**Status**: Complete

## Overview

This document captures research and decisions for reorganizing the TTS skill project structure and unifying documentation. Since this is a pure refactoring task with no functional changes, research focuses on best practices for Python project structure and documentation organization.

## Technical Decisions

### Decision 1: Scripts Directory Location

**Question**: Where should executable scripts be located in a Python CLI project?

**Options Considered**:
1. Keep scripts at project root (current state)
2. Move to `/scripts` directory
3. Move to `/bin` directory
4. Move to `/src` directory

**Decision**: Use `/scripts` directory

**Rationale**:
- Standard convention for Python CLI tools and skills
- Clear separation between executable scripts and library code
- Easy to locate all executables in one place
- Consistent with common Python project layouts (cookiecutter templates, etc.)
- `/bin` is typically for compiled binaries in Unix systems
- `/src` is for library/package code, not standalone scripts

**References**:
- Python Packaging User Guide recommends separating scripts
- Common pattern in skills/tools repositories

---

### Decision 2: Documentation Strategy

**Question**: How should documentation be organized - multiple files or single source?

**Options Considered**:
1. Keep README.md and SKILL.md separate (current state)
2. Merge all content into SKILL.md, simplify README.md
3. Merge all content into README.md, remove SKILL.md
4. Keep both files with identical content

**Decision**: Merge content into SKILL.md, simplify README.md to overview + link

**Rationale**:
- SKILL.md is the constitution-mandated comprehensive documentation file
- README.md should be brief entry point (GitHub/repo landing page convention)
- Single source of truth prevents documentation drift
- Users get complete information in one place (SKILL.md)
- README.md serves as quick overview and pointer to full docs

**Implementation**:
- Merge Quick Start, Features, and Project Structure from README.md into SKILL.md
- Reduce README.md to < 50 lines with overview and link to SKILL.md
- Maintain all existing SKILL.md sections (Usage, Dependencies, Error Codes, etc.)

---

### Decision 3: Git History Preservation

**Question**: How to move files while preserving git history?

**Options Considered**:
1. Copy files and delete old locations (loses history)
2. Use `git mv` command (preserves history)
3. Move manually and commit separately (partial history)

**Decision**: Use `git mv` for all file moves

**Rationale**:
- `git mv` explicitly preserves file history and is tracked by git
- Allows `git log --follow` to track file across moves
- Important for traceability and understanding code evolution
- Requirement FR-008 mandates history preservation

**Commands**:
```bash
git mv tts.py scripts/tts.py
git mv mp3-to-ogg/scripts/convert_mp3_to_ogg.py scripts/convert_mp3_to_ogg.py
```

---

### Decision 4: Test File Updates

**Question**: How to handle test imports after script relocation?

**Options Considered**:
1. Update imports to reference new paths
2. Use relative imports
3. Add symlinks to old locations
4. Modify PYTHONPATH

**Decision**: Update imports to reference new script locations directly

**Rationale**:
- Cleanest approach - tests reference actual file locations
- No symlinks or PYTHONPATH manipulation needed
- Tests remain simple and explicit
- Follows "explicit is better than implicit" Python principle

**Changes Required**:
- Update `sys.path.insert()` statements in test files
- Change from `os.path.dirname(os.path.dirname(__file__))` to account for new structure
- Example: `sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts'))`

---

### Decision 5: Obsolete Code Removal

**Question**: What to do with `/mp3-to-ogg` folder now that OGG conversion is integrated?

**Options Considered**:
1. Keep folder for reference
2. Archive to separate branch
3. Delete completely
4. Move to `/deprecated` directory

**Decision**: Delete completely via `git rm -r`

**Rationale**:
- Functionality fully replaced by `--format ogg` in tts.py (feature 006)
- Keeping obsolete code creates confusion
- Git history preserves the code if needed
- Clean repository reduces maintenance burden
- Follows "remove obsolete code" principle

**Migration Note**:
- Users needing OGG conversion should use: `python scripts/tts.py --format ogg`
- Old script path documented in migration notes

---

## Implementation Notes

### File Movement Order

1. Create `/scripts` directory
2. Move `tts.py` to `scripts/tts.py` (git mv)
3. Move `convert_mp3_to_ogg.py` to `scripts/convert_mp3_to_ogg.py` (git mv)
4. Update test imports
5. Update SKILL.md with merged content
6. Simplify README.md
7. Remove `/mp3-to-ogg` folder (git rm -r)
8. Update all documentation paths
9. Verify tests pass

### Documentation Merge Strategy

**From README.md → SKILL.md**:
- Quick Start section → Insert after Purpose section
- Features list → Insert in new Features section
- Project Structure → Update existing structure diagram

**README.md New Content**:
- Brief 2-3 sentence description
- Link to SKILL.md for complete documentation
- Quick installation command
- Basic usage example (one-liner)

### Testing Strategy

**Validation Steps**:
1. Run `pytest tests/` to verify all tests pass
2. Test script execution: `python scripts/tts.py "test"`
3. Verify OGG conversion: `python scripts/tts.py "test" --format ogg`
4. Check documentation completeness in SKILL.md
5. Verify no broken links in documentation

**Success Criteria**:
- All tests pass (100% compatibility)
- Scripts executable from new locations
- Documentation complete and accurate
- No obsolete code remains

---

## Risks and Mitigations

### Risk 1: Broken External References
**Risk**: Users or scripts may have hardcoded paths to `tts.py` at root
**Mitigation**: Add migration notes to README.md showing old vs new paths

### Risk 2: Test Import Failures
**Risk**: Test imports may break if path updates are incomplete
**Mitigation**: Comprehensive testing after each import change

### Risk 3: Documentation Gaps
**Risk**: Merging docs could lose important information
**Mitigation**: Careful review of both README.md and SKILL.md before merge, ensure all sections preserved

---

## Alternatives Rejected

### Alternative 1: Keep Current Structure
**Rejected because**: Doesn't follow Python project conventions, scripts scattered across repository

### Alternative 2: Use `/bin` Directory
**Rejected because**: `/bin` typically for compiled binaries in Unix, not Python scripts

### Alternative 3: Keep Separate Documentation Files
**Rejected because**: Creates documentation fragmentation, users must check multiple files

### Alternative 4: Archive mp3-to-ogg Instead of Deleting
**Rejected because**: Git history provides archiving, no need for separate archived code in active repo

---

## References

- Python Packaging User Guide: https://packaging.python.org/
- Cookiecutter Python Project Templates
- TTS Skill Constitution (Gate 1: Skill-Centric Architecture, Documentation Standards)
- Common Python CLI project structures (Click, Typer, etc.)

---

## Summary

All technical decisions finalized:
- ✅ Scripts location: `/scripts` directory
- ✅ Documentation strategy: Unified SKILL.md
- ✅ File movement: `git mv` for history preservation
- ✅ Test updates: Direct import path updates
- ✅ Obsolete code: Complete removal of `/mp3-to-ogg`

No unresolved questions remain. Ready for Phase 1 design.
