# Contracts: Reorganize Scripts and Unify Documentation

**Feature**: 007-reorganize-scripts  
**Date**: 2026-03-05

## Overview

This feature is a pure refactoring task focused on file reorganization and documentation consolidation. **No interface contracts are modified** as part of this work.

## Interface Contracts

**N/A** - No external interfaces are changed.

The TTS skill's command-line interface remains identical:
- Same command syntax: `python scripts/tts.py "text" [options]`
- Same arguments: `--lang`, `--format`, `-o/--output`
- Same output format: absolute file path to stdout
- Same exit codes: 0 (success), 1 (input error), 2 (network), 3 (filesystem), 4 (processing)
- Same error messages

**Only the script path changes** from `tts.py` to `scripts/tts.py` - the interface itself is unchanged.

## Migration Contract

For users upgrading to this reorganized structure:

### Old Usage (Before 007)
```bash
python tts.py "hello world" --format ogg --lang en
```

### New Usage (After 007)
```bash
python scripts/tts.py "hello world" --format ogg --lang en
```

**Migration Notes**:
- All functionality remains identical
- Only the path to the executable changes
- Backward compatibility: Users can create a symlink if needed
- Documentation provides clear migration path

## Testing Contract

**Validation Requirements**:
1. All existing tests must pass after reorganization (100% compatibility)
2. Scripts must be executable from new locations
3. Output format remains identical
4. Error handling unchanged

**Test Updates Required**:
- Import statements in test files updated to reference new script locations
- No changes to test assertions or expected behaviors
- No new tests required (functionality unchanged)

## Summary

**No functional interface changes** - only file location reorganization. The skill's API, behavior, and contracts remain completely unchanged.
