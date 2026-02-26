# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Synthkit is a Python package for converting AI-generated Markdown (from Claude, Gemini, etc.) into production-ready documents. It provides a unified CLI (`synthkit doc/email/html/pdf`) and backward-compatible standalone commands (`md2doc`, `md2email`, `md2html`, `md2pdf`). Installable via `uvx synthkit` or `pip install synthkit`.

## Repository Structure

- **`src/synthkit/`**: Python package source
  - `cli.py` — Click CLI with subcommands and standalone entry points
  - `base.py` — Shared logic (format building, config discovery, batch processing, pandoc invocation)
  - `doc.py` — Markdown → Word (.docx) via pandoc
  - `email.py` — Markdown → clipboard (HTML/RTF, cross-platform via pyperclip)
  - `html.py` — Markdown → HTML via pandoc
  - `pdf.py` — Markdown → PDF via pandoc + weasyprint
- **`pyproject.toml`**: Package config (hatchling build, click+pypandoc_binary+pyperclip+weasyprint deps)
- **`style.css`**: Default stylesheet bundled with the package
- **`prompt-templates/`**: Prompt templates for AI interaction use cases
- **`guidelines/`**: Reference guidelines and standards

## Development

```bash
# Install in development mode
uv pip install -e .

# Run directly
uv run synthkit html example.md
uv run md2html example.md
```

## Architecture

- All converters share `base.py` logic: pandoc format string (`markdown+lists_without_preceding_blankline` ± `hard_line_breaks`), config file discovery under `~/.config/<toolname>/`, batch processing with success/fail counting.
- Mermaid diagram support is opt-in via `--mermaid` flag (requires `mermaid-filter` installed externally).
- `email.py` is cross-platform: uses `textutil`+`pbcopy` on macOS for RTF clipboard, falls back to `pyperclip` (HTML) on other platforms.
- `pdf.py` uses `--pdf-engine=weasyprint` (CSS-styled, no LaTeX needed). Config via `~/.config/md2pdf/style.css`.
- Entry points defined in `pyproject.toml`: `synthkit` (unified CLI group), plus `md2doc`/`md2email`/`md2html`/`md2pdf` (standalone).

## Testing

Uses pytest. Tests are in `tests/` with shared fixtures in `conftest.py`.

```bash
uv run --extra dev pytest        # run all tests
uv run --extra dev pytest -v     # verbose
uv run --extra dev pytest -k base  # run specific module
```

Tests use mocking for pandoc/clipboard calls. Integration tests in `test_cli.py::TestIntegration` run actual pandoc via the bundled binary.

## Key Dependencies

### Python (pip-installed automatically)
- **click** (CLI framework)
- **pypandoc_binary** (bundles pandoc binary)
- **pyperclip** (cross-platform clipboard)
- **weasyprint** (PDF engine)

### System (required for PDF only)
- **pango**, **cairo**, **gobject** — required by weasyprint
  - macOS: `brew install pango`
  - Ubuntu/Debian: `apt install libpango1.0-dev libcairo2-dev libgdk-pixbuf2.0-dev`

### External (optional)
- **mermaid-filter** (Mermaid diagram rendering, opt-in via `--mermaid` flag)
