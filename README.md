# Synthkit

[![PyPI](https://img.shields.io/pypi/v/synthkit.svg)](https://pypi.org/project/synthkit/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/rappdw/synthkit/actions/workflows/tests.yml/badge.svg)](https://github.com/rappdw/synthkit/actions/workflows/tests.yml)
[![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/rappdw/02d0a91962d09fd9473da34fccd76237/raw/synthkit-coverage.json)](https://github.com/rappdw/synthkit/actions/workflows/tests.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

Synthkit was born from building [Satori](https://www.proofpoint.com/us/platform/satori) — a platform that deploys AI agents to scale security operations. When AI generates content at volume, you need tooling to bridge the gap between raw output and what the organization actually needs. Synthkit is that bridge.

A "last-mile" toolkit for working with generative AI. Synthkit bridges the gap between raw LLM output and production-ready deliverables through:

- **Document conversion** — Transform AI-generated Markdown into Word, HTML, PDF, or clipboard-ready email
- **Structured exploration** — Guided discovery sessions that draw out your domain knowledge before generating anything
- **Prompt templates** — Curated templates for structured AI interactions (reports, emails, analysis)
- **Guidelines** — Reference standards and style guides to steer AI output quality

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

### Claude Code Plugin

Synthkit is also available as a [Claude Code](https://claude.ai/code) plugin, adding skills directly into your coding assistant:

```
/plugin install synthkit
```

This gives you slash commands inside Claude Code:

| Command | Description |
|---------|-------------|
| `/synthkit:explore-with-me` | Guided exploration — Claude interviews you to structure your thinking before writing anything |
| `/synthkit:md2pdf` | Convert markdown to PDF |
| `/synthkit:md2docx` | Convert markdown to Word |
| `/synthkit:md2html` | Convert markdown to HTML |
| `/synthkit:md2email` | Convert markdown to clipboard-ready email |

The **explore-with-me** skill is particularly useful for thinking through architecture decisions, incident postmortems, risk assessments, or any situation where you know more than the AI and premature generation would anchor on the wrong framing.

## Document Conversion

### System dependencies for PDF

PDF conversion uses [WeasyPrint](https://weasyprint.org/), which requires system libraries:

| Platform | Install command |
|----------|----------------|
| **macOS** | `brew install pango` |
| **Ubuntu/Debian** | `apt install libpango1.0-dev libcairo2-dev libgdk-pixbuf2.0-dev` |
| **Windows** | See [WeasyPrint docs](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows) |

`doc`, `html`, and `email` commands work without these.

### Usage

#### Unified CLI

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

#### Backward-compatible commands

```bash
md2doc report.md
md2html report.md
md2pdf report.md
md2email report.md
```

#### Options

| Flag | Description |
|------|-------------|
| `--hard-breaks` | Preserve line breaks from source markdown |
| `--mermaid` | Enable Mermaid diagram rendering (requires [`mermaid-filter`](https://github.com/raghur/mermaid-filter)) |

### Configuration

Each converter looks for optional config files under `~/.config/<toolname>/`:

| Converter | Config Files |
|-----------|-------------|
| `doc` | `~/.config/md2doc/reference.docx` |
| `email` | `~/.config/md2email/style.css` |
| `html` | `~/.config/md2html/style.css` |
| `pdf` | `~/.config/md2pdf/style.css` |

## Prompt Templates

The `prompt-templates/` directory contains curated prompt templates for structured AI interactions. These are optimized for Markdown-first responses to ensure compatibility with the document conversion tools.

Copy the contents of any template into your LLM of choice (Claude, Gemini, ChatGPT, etc.) to get consistently structured output ready for conversion.

## Guidelines

The `guidelines/` directory contains reference standards and style guides that can be provided as context to AI models to steer output quality and consistency.

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
├── .claude-plugin/        # Claude Code plugin metadata
│   └── plugin.json
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
├── skills/                # Claude Code plugin skills
│   ├── explore-with-me/   # Structured exploration interviews
│   ├── md2pdf/            # PDF conversion skill
│   ├── md2docx/           # Word conversion skill
│   ├── md2html/           # HTML conversion skill
│   └── md2email/          # Email conversion skill
├── hooks/                 # Claude Code plugin hooks
│   └── hooks.json         # SessionStart dependency check
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
