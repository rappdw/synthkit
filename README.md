# Synthkit

[![PyPI](https://img.shields.io/pypi/v/synthkit.svg)](https://pypi.org/project/synthkit/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/rappdw/synthkit/actions/workflows/tests.yml/badge.svg)](https://github.com/rappdw/synthkit/actions/workflows/tests.yml)
[![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/rappdw/02d0a91962d09fd9473da34fccd76237/raw/synthkit-coverage.json)](https://github.com/rappdw/synthkit/actions/workflows/tests.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

A toolkit for amplifying what you can do with AI. Synthkit combines thinking tools (structured exploration, strategic debate) with production tools (document conversion, project scaffolding) into a single package — usable from the command line, from Claude Code, or both.

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

## Skills

Skills are Claude Code slash commands that give Claude specialized capabilities. Install the plugin and invoke them with `/synthkit:<skill-name>`.

### Thinking Tools

These skills help you think through problems before committing to solutions.

#### `/synthkit:explore-with-me` — Structured Exploration

Claude acts as an interviewer, not a generator. It draws out your domain knowledge through focused questions, structures your thinking, identifies gaps, and pressure-tests assumptions — only writing findings after validating them with you.

**When to use:** You have a decision to make, a problem to diagnose, a risk to assess, or a strategy to shape — and you know more about the situation than the AI does. The exploration typically resolves in a single conversation (5-15 rounds).

**Examples:** "Help me think through whether we should migrate to GraphQL." "I need to figure out why our deploy pipeline keeps breaking." "Let's explore the tradeoffs of hiring contractors vs. full-time."

**Output:** A markdown file with context, key findings, constraints, tensions, and recommendations.

#### `/synthkit:init-discovery` — Discovery Project Scaffolding

Sets up a multi-session exploration project. Claude interviews you about the initiative, then generates a customized `CLAUDE.md` (so future sessions have full context) plus a working file structure for sustained investigation.

**When to use:** The problem is too big for one conversation. You'll be coming back to it over days or weeks, possibly with evolving deliverables and multiple stakeholders. You need Claude to maintain context across sessions.

**Examples:** "Set up a discovery project for our Q3 platform migration." "I need to investigate our incident response process over the next few weeks." "Scaffold an exploration of our pricing strategy."

**Output:** `CLAUDE.md` + working files (`current-state.md`, `problem-analysis.md`, `requirements.md`, `options/`, `decision-log.md`).

#### `/synthkit:boardroom` — Strategic Debate

Think of this as a Monte Carlo simulation with intelligence. Traditional Monte Carlo varies the inputs and sees where outputs cluster. Boardroom varies the *mental models* — each advisor is a sample drawn from a different distribution of strategic thinking — and sees where conclusions cluster. When they don't cluster, you understand *why* they diverge. And unlike random sampling, Round 2 is adaptive: the samples communicate, update on each other's reasoning, and change their positions.

Concretely: spin up a board of AI advisors — real people whose strategic thinking you admire — and have them debate your decision in two rounds. Round 1: each advisor argues their position in parallel. Round 2: they read each other's arguments and fight — naming names, quoting each other, changing votes or doubling down. The vote tracker is your convergence metric. The interactive sliders let you run sensitivity analysis after the fact.

Inspired by [Allie K Miller's boardroom concept](https://x.com/alliekmiller/status/2021578555034149188).

**When to use:** You have a high-stakes strategic decision and want to stress-test it from multiple perspectives before committing. Pricing, launches, partnerships, organizational changes, market entry — anything where smart people would disagree.

**Examples:** `/synthkit:boardroom "Should I price this at $25,000 or $50,000?"` `/synthkit:boardroom "How should we launch the new developer tier?"` `/synthkit:boardroom "Should we build or buy our analytics platform?"`

**Output:** A folder with three files:
- `debate.md` — Full transcript with vote tracker, key tensions, and decision framework
- `debate.html` — Interactive dashboard with assumption sliders that recalculate projections
- `debate.pdf` — Print-optimized version for sharing with your team

#### `/synthkit:map-the-repo` — Codebase Documentation

Generate a browsable wiki from any codebase. The script scans your repo, extracts architecture, APIs, and module structure via AST analysis, then generates markdown docs and a self-contained HTML site with dark theme, Mermaid diagrams, full-text search, and syntax highlighting.

**When to use:** You need to document a codebase, onboard a new engineer, hand off a repo, or just understand a project's architecture. Works with Python (deep AST analysis), TypeScript, JavaScript, Go, Java, Rust, and more (regex-based extraction).

**Examples:** "Document this repo." "Generate a wiki for onboarding." "Map the architecture of this codebase." "I need to understand this project."

**Output:** A `wiki/` folder with:
- `docs/*.md` — Markdown documentation (index, architecture, data flows, API reference, glossary, per-module docs)
- `site/index.html` — Self-contained browsable site (open directly in browser, no build tools needed)

### Production Tools

These skills convert AI-generated content into deliverable formats.

#### `/synthkit:md2pdf` — Markdown to PDF

Convert markdown files to PDF using pandoc with weasyprint (CSS-based, no LaTeX needed).

**When to use:** You need a polished PDF from a markdown file — reports, proposals, documentation.

**Requires system libraries** (pango, cairo) — see [System Dependencies](#system-dependencies-for-pdf).

#### `/synthkit:md2docx` — Markdown to Word

Convert markdown files to Word (.docx) using pandoc.

**When to use:** You need to share a document with people who work in Word, or you need to use Word's review/comment features.

#### `/synthkit:md2html` — Markdown to HTML

Convert markdown files to standalone HTML using pandoc, with optional CSS styling.

**When to use:** You need a self-contained HTML file — for web publishing, email embedding, or portable viewing.

#### `/synthkit:md2email` — Markdown to Email

Convert a markdown file to formatted email content and copy it to the clipboard. Rich text (RTF) on macOS, HTML elsewhere.

**When to use:** You've drafted an email in markdown and want to paste it into your mail client with formatting intact.

## Document Conversion (CLI)

The conversion tools are also available as standalone CLI commands, independent of Claude Code.

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

## Reference Materials

### Prompt Templates

The `prompt-templates/` directory contains pointers to canonical templates maintained alongside their skills. If you're using Claude Code, the skills fill these in automatically.

| Template | Canonical source | Claude Code shortcut |
|----------|-----------------|----------------------|
| `structured-discovery.md` | `skills/init-discovery/references/` | `/synthkit:init-discovery` |

### Guidelines

The `guidelines/` directory contains reference standards and methods that can be provided as context to AI models.

| Guideline | Purpose |
|-----------|---------|
| `structured-elicitation.md` | The Structured Elicitation method (canonical source: `skills/explore-with-me/references/`) |
| `markdown-conventions.md` | Markdown formatting standards for AI-generated content |

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
│   ├── boardroom/         # Strategic debate with AI advisors
│   ├── explore-with-me/   # Structured exploration interviews
│   ├── init-discovery/    # Multi-session project scaffolding
│   ├── map-the-repo/      # Codebase documentation wiki generator
│   ├── md2pdf/            # PDF conversion skill
│   ├── md2docx/           # Word conversion skill
│   ├── md2html/           # HTML conversion skill
│   └── md2email/          # Email conversion skill
├── tests/                 # Test suite (pytest)
│   ├── conftest.py        # Shared fixtures
│   ├── test_base.py       # Base module tests
│   ├── test_cli.py        # CLI + integration tests
│   ├── test_doc.py        # Word converter tests
│   ├── test_email.py      # Email converter tests
│   ├── test_html.py       # HTML converter tests
│   └── test_pdf.py        # PDF converter tests
├── style.css              # Default stylesheet
├── prompt-templates/      # Pointers to canonical templates
└── guidelines/            # Pointers to canonical references
```

## Dependencies

| Package | Purpose | Bundled? |
|---------|---------|----------|
| [`click`](https://click.palletsprojects.com/) | CLI framework | pip |
| [`pypandoc_binary`](https://pypi.org/project/pypandoc-binary/) | Pandoc document converter | pip (includes binary) |
| [`pyperclip`](https://pypi.org/project/pyperclip/) | Cross-platform clipboard | pip |
| [`weasyprint`](https://weasyprint.org/) | PDF engine | pip (needs system libs) |
| [`mermaid-filter`](https://github.com/raghur/mermaid-filter) | Mermaid diagrams | Optional, external |
