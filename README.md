# Synthkit

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/rappdw/synthkit/actions/workflows/tests.yml/badge.svg)](https://github.com/rappdw/synthkit/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/rappdw/synthkit/graph/badge.svg)](https://codecov.io/gh/rappdw/synthkit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

A toolkit for converting AI-generated Markdown (from Claude, Gemini, etc.) into production-ready documents: Word, HTML, PDF, and clipboard-ready email.

## Installation

```bash
# Run directly with uvx (no install needed)
uvx synthkit html document.md

# Or install globally
uv tool install synthkit

# Or install with pip
pip install synthkit
```

Pandoc is bundled automatically via [`pypandoc_binary`](https://pypi.org/project/pypandoc-binary/) — no separate install needed.

### System dependencies for PDF

PDF conversion uses [WeasyPrint](https://weasyprint.org/), which requires system libraries:

| Platform | Install command |
|----------|----------------|
| **macOS** | `brew install pango` |
| **Ubuntu/Debian** | `apt install libpango1.0-dev libcairo2-dev libgdk-pixbuf2.0-dev` |
| **Windows** | See [WeasyPrint docs](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows) |

`doc`, `html`, and `email` commands work without these.

## Usage

### Unified CLI

```bash
synthkit doc report.md           # → report.docx
synthkit html report.md          # → report.html
synthkit pdf report.md           # → report.pdf
synthkit email report.md         # → clipboard

# Batch processing
synthkit doc *.md
synthkit html *.md --hard-breaks

# Mermaid diagrams (requires mermaid-filter)
synthkit html report.md --mermaid
```

### Backward-compatible commands

```bash
md2doc report.md
md2html report.md
md2pdf report.md
md2email report.md
```

### Options

| Flag | Description |
|------|-------------|
| `--hard-breaks` | Preserve line breaks from source markdown |
| `--mermaid` | Enable Mermaid diagram rendering (requires [`mermaid-filter`](https://github.com/raghur/mermaid-filter)) |

## Configuration

Each converter looks for optional config files under `~/.config/<toolname>/`:

| Converter | Config Files |
|-----------|-------------|
| `doc` | `~/.config/md2doc/reference.docx` |
| `email` | `~/.config/md2email/style.css` |
| `html` | `~/.config/md2html/style.css` |
| `pdf` | `~/.config/md2pdf/style.css` |

## Testing

```bash
# Run tests
uv run --extra dev pytest

# With coverage
uv run --extra dev pytest --cov=synthkit --cov-report=term-missing
```

Tests run automatically on push/PR to `main` across Python 3.10-3.13 on Linux, macOS, and Windows.

## Repository Structure

```
├── .github/workflows/
│   ├── tests.yml          # CI: test on push/PR to main
│   └── publish.yml        # CD: publish to PyPI on release
├── pyproject.toml
├── src/synthkit/          # Python package
│   ├── cli.py             # Click CLI with subcommands
│   ├── base.py            # Shared conversion logic
│   ├── doc.py             # Word conversion
│   ├── email.py           # Email clipboard conversion
│   ├── html.py            # HTML conversion
│   └── pdf.py             # PDF conversion (via WeasyPrint)
├── tests/                 # Test suite (pytest)
│   ├── conftest.py        # Shared fixtures
│   ├── test_base.py       # Base module tests
│   ├── test_cli.py        # CLI + integration tests
│   ├── test_doc.py        # Word converter tests
│   ├── test_email.py      # Email converter tests
│   ├── test_html.py       # HTML converter tests
│   └── test_pdf.py        # PDF converter tests
├── style.css              # Default stylesheet
├── prompt-templates/      # AI interaction prompt templates
└── guidelines/            # Reference guidelines
```

## Dependencies

| Package | Purpose | Bundled? |
|---------|---------|----------|
| [`click`](https://click.palletsprojects.com/) | CLI framework | pip |
| [`pypandoc_binary`](https://pypi.org/project/pypandoc-binary/) | Pandoc document converter | pip (includes binary) |
| [`pyperclip`](https://pypi.org/project/pyperclip/) | Cross-platform clipboard | pip |
| [`weasyprint`](https://weasyprint.org/) | PDF engine | pip (needs system libs) |
| [`mermaid-filter`](https://github.com/raghur/mermaid-filter) | Mermaid diagrams | Optional, external |
