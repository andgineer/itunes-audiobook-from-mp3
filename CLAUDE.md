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
source ./activate.sh
```
This script creates a Python 3.12 virtual environment using `uv` and installs dependencies.

**IMPORTANT**: Always activate the virtual environment before running any commands. Use `source ./activate.sh` before each command.

## Common Commands

**Run tests**:
```bash
source ./activate.sh && pytest
source ./activate.sh && pytest tests/test_specific.py  # Run specific test file
```

**Linting and formatting**:
```bash
source ./activate.sh && pre-commit run --all-files  # Run all pre-commit hooks (ruff + mypy)
```

**IMPORTANT**: Always use `pre-commit run --all-files` for code quality checks. Never run ruff or mypy directly.

**Build and package**:
```bash
source ./activate.sh && python -m build  # Build wheel and source distribution
```

**Requirements management**:
```bash
source ./activate.sh && make reqs  # Update requirements and pre-commit hooks
```

**Version management**:
```bash
source ./activate.sh && make ver-bug     # Bump patch version
source ./activate.sh && make ver-feature # Bump minor version
source ./activate.sh && make ver-release # Bump major version
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
