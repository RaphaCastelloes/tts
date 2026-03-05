# Quickstart: Reorganize Scripts and Unify Documentation

**Feature**: 007-reorganize-scripts  
**Date**: 2026-03-05  
**Target**: Developers working with TTS skill

## Overview

This guide helps you understand and implement the project structure reorganization and documentation unification for the TTS skill.

## Prerequisites

- Existing TTS skill repository on branch `006-ogg-output-option` or later
- Git installed and configured
- All tests currently passing
- Familiarity with git mv command

## Quick Setup (5 minutes)

### Step 1: Create Scripts Directory

```bash
# From repository root
mkdir scripts
```

### Step 2: Move Executable Scripts

```bash
# Move tts.py to scripts/ (preserves git history)
git mv tts.py scripts/tts.py

# Move convert_mp3_to_ogg.py to scripts/
git mv mp3-to-ogg/scripts/convert_mp3_to_ogg.py scripts/convert_mp3_to_ogg.py
```

### Step 3: Update Test Imports

Update test files to reference new script locations:

**File**: `tests/test_tts.py`
```python
# Change this line:
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# To this:
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))
```

Repeat for `tests/test_audio_format.py` and `tests/test_integration.py`.

### Step 4: Merge Documentation

**Merge README.md content into SKILL.md**:
1. Copy "Quick Start" section from README.md to SKILL.md (after Purpose section)
2. Copy "Features" list to SKILL.md (new Features section)
3. Update "Project Structure" diagram in SKILL.md to show new layout

**Simplify README.md** to:
```markdown
# WhatsApp TTS Script

Convert text to speech and generate WhatsApp-compatible audio files in MP3 or OGG format.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate MP3
python scripts/tts.py "hello world" --lang en

# Generate OGG for WhatsApp
python scripts/tts.py "hello world" --format ogg --lang en
```

## Documentation

See [SKILL.md](SKILL.md) for complete documentation.

## Version

**Version**: 1.1.0  
**Status**: Production Ready
```

### Step 5: Update All Documentation Paths

Update all references from `tts.py` to `scripts/tts.py` in:
- SKILL.md examples
- SKILL.md usage sections
- Any remaining documentation files

### Step 6: Remove Obsolete Code

```bash
# Remove mp3-to-ogg folder completely
git rm -r mp3-to-ogg/
```

### Step 7: Verify Everything Works

```bash
# Run tests
pytest tests/ -v

# Test MP3 generation
python scripts/tts.py "test" --lang en

# Test OGG generation
python scripts/tts.py "test" --format ogg --lang en
```

### Step 8: Commit Changes

```bash
git add -A
git commit -m "Reorganize scripts into /scripts directory and unify documentation

- Move tts.py to scripts/tts.py
- Move convert_mp3_to_ogg.py to scripts/
- Merge README.md quick start into SKILL.md
- Simplify README.md to brief overview
- Remove obsolete mp3-to-ogg/ folder
- Update all documentation paths
- Update test imports

All tests passing. No functional changes."
```

## Testing Checklist

After implementation, verify:

- [ ] `/scripts` directory exists and contains both Python files
- [ ] `tts.py` no longer exists at repository root
- [ ] `mp3-to-ogg/` directory is completely removed
- [ ] All tests pass: `pytest tests/ -v`
- [ ] Script execution works: `python scripts/tts.py "test"`
- [ ] OGG conversion works: `python scripts/tts.py "test" --format ogg`
- [ ] SKILL.md contains Quick Start section
- [ ] SKILL.md contains Features section
- [ ] SKILL.md has updated project structure diagram
- [ ] README.md is under 50 lines
- [ ] README.md links to SKILL.md
- [ ] All documentation examples reference `scripts/tts.py`
- [ ] Git history preserved (verify with `git log --follow scripts/tts.py`)

## Common Issues

### Issue 1: Test Import Errors

**Symptom**: Tests fail with `ModuleNotFoundError`

**Solution**: Ensure test files have correct path in `sys.path.insert()`:
```python
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))
```

### Issue 2: Script Not Found

**Symptom**: `python scripts/tts.py` fails with "No such file or directory"

**Solution**: Verify you used `git mv` not regular `mv`, and file exists in scripts/ directory:
```bash
ls -la scripts/
```

### Issue 3: Git History Lost

**Symptom**: `git log --follow scripts/tts.py` shows no history

**Solution**: Use `git mv` instead of copying/deleting:
```bash
git mv tts.py scripts/tts.py
```

## Migration Notes for Users

If you have existing scripts or integrations using the old paths:

### Before (Old Path)
```bash
python tts.py "hello" --format ogg
```

### After (New Path)
```bash
python scripts/tts.py "hello" --format ogg
```

**Quick Fix**: Create a symlink for backward compatibility (temporary):
```bash
ln -s scripts/tts.py tts.py
```

## Next Steps

After completing this reorganization:
1. Test all functionality thoroughly
2. Update any external documentation or deployment scripts
3. Notify users of the path change
4. Consider updating CI/CD pipelines if they reference old paths

## Reference

- **Specification**: `specs/007-reorganize-scripts/spec.md`
- **Implementation Plan**: `specs/007-reorganize-scripts/plan.md`
- **Research**: `specs/007-reorganize-scripts/research.md`
- **Feature Branch**: `007-reorganize-scripts`

## Time Estimate

- Implementation: 15-20 minutes
- Testing: 10 minutes
- Documentation updates: 15 minutes
- **Total**: ~45 minutes

## Success Criteria

✅ All executable scripts in `/scripts` directory  
✅ SKILL.md is single comprehensive documentation source  
✅ README.md simplified to < 50 lines  
✅ All tests pass (100% compatibility)  
✅ No obsolete code in repository  
✅ Git history preserved for all moved files  
✅ All documentation references correct paths
