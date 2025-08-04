# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python CLI tool that fixes MP3 file tags to make them compatible with iTunes/iPhone audiobooks. It handles encoding issues (particularly Windows-1251 Cyrillic) and sets proper track ordering for audiobook playback.

**Main Package**: `audiobook_tags` in `src/audiobook_tags/`
- `main.py` - CLI argument parsing and entry point
- `tags.py` - Core MP3 tag processing logic using eyeD3 library

## Development Setup

**Environment activation** (required before any development work):
```bash
. ./activate.sh
```
This script creates a Python 3.12 virtual environment using `uv` and installs dependencies.

## Common Commands

**Run tests**:
```bash
pytest
pytest tests/test_specific.py  # Run specific test file
```

**Linting and formatting**:
```bash
pre-commit run --all-files  # Run all pre-commit hooks (ruff + mypy)
ruff check src/  # Manual ruff check
ruff format src/  # Manual ruff format
mypy src/  # Manual type checking
```

**Build and package**:
```bash
python -m build  # Build wheel and source distribution
```

**Requirements management**:
```bash
make reqs  # Update requirements and pre-commit hooks
```

**Version management**:
```bash
make ver-bug     # Bump patch version
make ver-feature # Bump minor version
make ver-release # Bump major version
```

## Architecture

**CLI Flow**: `main.py:main()` → `get_opts()` → `tags.py:process_files()`

**Core Processing**:
1. `get_files_list()` - Scans directory for MP3 files, sorts by name or tag if requested
2. `fix_file_tags()` - Per-file processing:
   - Sets genre/mediatype to "Audiobook"
   - Fixes encoding issues via `fix_encoding()`
   - Applies custom tag overrides from CLI
   - Sets track numbering and prefixes if requested
3. Saves all changes at once (or skips in dry-run mode)

**Key Dependencies**:
- `eyed3` - MP3 tag manipulation
- `pathlib` - File system operations
- Built-in `argparse` for CLI

**Testing**: Uses pytest with fixtures in `conftest.py`. Test files in `tests/` directory include actual MP3 sample in `tests/resources/`.

**Code Quality**:
- Ruff for linting/formatting (line length 100)
- MyPy for type checking
- Pre-commit hooks enforce quality standards
- Tests excluded from strict linting rules
