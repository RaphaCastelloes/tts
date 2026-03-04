# Quickstart: Language Selection for TTS

**Feature**: 004-lang-selection  
**Date**: 2026-03-04

## What This Feature Does

Adds command-line language selection to the TTS script, allowing users to choose between English and Brazilian Portuguese for speech output. Brazilian Portuguese remains the default for backward compatibility.

## Quick Examples

### Use Default Language (Brazilian Portuguese)

```bash
# No change needed - works exactly as before
python tts.py "Olá mundo"
# Output: /path/to/output/tts_20260304_153000_abc123.mp3 (in pt-br)
```

### Generate English Speech

```bash
python tts.py "Hello world" --lang en
# Output: /path/to/output/tts_20260304_153001_def456.mp3 (in English)
```

### Generate Brazilian Portuguese Speech (Explicit)

```bash
python tts.py "Olá mundo" --lang pt-br
# Output: /path/to/output/tts_20260304_153002_ghi789.mp3 (in pt-br)
```

### Combine with Custom Output Path

```bash
python tts.py "Hello world" --lang en -o greeting.mp3
# Output: /path/to/greeting.mp3 (in English)
```

## For Developers

### Files Modified

1. **tts.py**: Add `--lang` argument to argparse, pass to gTTS constructor
2. **tests/test_tts.py**: Add language selection tests
3. **tests/test_integration.py**: Add integration tests for language selection
4. **SKILL.md**: Update documentation with language examples

### Key Implementation Points

1. **Argument Parsing**:
   ```python
   parser.add_argument(
       '--lang',
       default='pt-br',
       choices=['en', 'pt-br'],
       help='Language for speech output (default: pt-br)'
   )
   ```

2. **Pass to gTTS**:
   ```python
   tts = gTTS(text=text, lang=args.lang, slow=False)
   ```

3. **Validation**: Automatic via argparse `choices` parameter

### Testing Checklist

- [ ] Test default behavior (no --lang) uses pt-br
- [ ] Test --lang en produces English audio
- [ ] Test --lang pt-br produces Portuguese audio
- [ ] Test invalid language code (e.g., --lang fr) exits with code 1
- [ ] Test help text shows --lang option
- [ ] Test backward compatibility (existing scripts work unchanged)

### Common Pitfalls

❌ **Don't**: Change the default from pt-br (breaks backward compatibility)  
✅ **Do**: Keep default='pt-br' in argparse

❌ **Don't**: Add custom validation for language codes  
✅ **Do**: Use argparse `choices` parameter for automatic validation

❌ **Don't**: Make --lang a required argument  
✅ **Do**: Keep it optional with default value

## For Users

### When to Use Each Language

**Use default (pt-br)** when:
- Your text is in Portuguese
- You're using existing scripts (no changes needed)
- You want Brazilian Portuguese pronunciation

**Use --lang en** when:
- Your text is in English
- You want English pronunciation
- You're generating audio for English-speaking users

**Use --lang pt-br** when:
- You want to be explicit about the language
- You're documenting your command for others
- You're scripting and want clarity

### Help Command

```bash
python tts.py --help
```

Shows all available options including language selection.

## Migration Guide

### Existing Scripts

**No changes required!** All existing scripts continue to work:

```bash
# Before feature (worked)
python tts.py "Olá mundo"

# After feature (still works, same behavior)
python tts.py "Olá mundo"
```

### Opting Into Language Selection

To use the new feature, simply add `--lang`:

```bash
# Old way (still works)
python tts.py "Hello world"  # Uses pt-br default

# New way (explicit English)
python tts.py "Hello world" --lang en  # Uses English
```

## Troubleshooting

### Error: "invalid choice: 'XX'"

**Cause**: Unsupported language code

**Solution**: Use only `en` or `pt-br`:
```bash
# Wrong
python tts.py "text" --lang fr

# Right
python tts.py "text" --lang en
```

### Error: "expected one argument"

**Cause**: --lang provided without value

**Solution**: Provide a language code:
```bash
# Wrong
python tts.py "text" --lang

# Right
python tts.py "text" --lang en
```

### Wrong Language in Audio

**Cause**: Case-sensitive language codes

**Solution**: Use lowercase:
```bash
# Wrong
python tts.py "text" --lang EN

# Right
python tts.py "text" --lang en
```

## Next Steps

1. Review the [specification](spec.md) for detailed requirements
2. Check [research.md](research.md) for implementation decisions
3. See [data-model.md](data-model.md) for data flow
4. Read [contracts/cli-interface.md](contracts/cli-interface.md) for the complete CLI contract
5. Run `/speckit.tasks` to generate implementation tasks
