# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Synthkit is a Bash toolkit for converting AI-generated Markdown (from Claude, Gemini, etc.) into production-ready documents. Four scripts handle the "last-mile" transformation: `md2doc` (Word), `md2email` (clipboard-ready email), `md2html` (HTML), `md2pdf` (PDF).

## Repository Structure

- **Root**: Conversion scripts (`md2doc`, `md2email`, `md2html`, `md2pdf`)
- **`prompt-templates/`**: Prompt templates for various AI interaction use cases
- **`guidelines/`**: Reference guidelines and standards

## Scripts

All scripts are standalone Bash files in the repo root. They share these conventions:
- `set -u` for strict undefined-variable checking (use `${arr[@]+"${arr[@]}"}` pattern for optional arrays)
- Pandoc base format: `markdown+lists_without_preceding_blankline` with optional `+hard_line_breaks`
- `--hard-breaks` flag available on all scripts
- Mermaid diagram support via `--filter mermaid-filter`
- Batch processing with SUCCESS_COUNT/FAIL_COUNT tracking (except `md2email` which is single-file)
- Per-tool config files under `$HOME/.config/<toolname>/`

| Script | Output | Key Dependencies | Config Path |
|--------|--------|-----------------|-------------|
| `md2doc` | .docx | pandoc, mermaid-filter | `~/.config/md2doc/reference.docx` |
| `md2email` | clipboard (RTF) | pandoc, textutil, pbcopy (macOS only) | `~/.config/md2email/style.css` |
| `md2html` | .html | pandoc | `~/.config/md2html/style.css` |
| `md2pdf` | .pdf | pandoc, xelatex, eisvogel template | `~/.config/md2pdf/fix-unicode.lua`, `unicode-support.tex` |

## Testing

No test framework. Test manually:
```bash
./md2doc example.md
./md2html *.md
./md2pdf example.md
echo "test" > /tmp/test.md && ./md2email /tmp/test.md
```

Use `bash -x ./md2doc example.md` to debug with trace output.

## Key Dependencies

- **Pandoc** (all scripts)
- **xelatex** + **eisvogel** template (md2pdf)
- **mermaid-filter** (diagram rendering, all scripts)
- **textutil** + **pbcopy** (md2email, macOS-only)
