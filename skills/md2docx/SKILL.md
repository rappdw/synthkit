---
name: md2docx
user-invocable: true
argument-hint: [file.md ...]
allowed-tools: Bash(md2doc *), Bash(synthkit doc *), Read, Write
model: claude-sonnet-4-6
effort: low
description: >
  Convert Markdown files to Word (.docx) format using pandoc. Use this skill when the user
  wants to create a Word document from markdown, or says things like "make a docx",
  "convert to Word", "export as Word", or "/md2docx".
---

# Markdown to Word (.docx)

Convert one or more Markdown files to Word documents using pandoc.

## Usage

Run the conversion using the `md2doc` CLI command:

```bash
md2doc $ARGUMENTS
```

Or via the unified CLI:

```bash
synthkit doc $ARGUMENTS
```

### Options

| Flag | Description |
|------|-------------|
| `--hard-breaks` | Preserve line breaks from the source markdown |
| `--mermaid` | Enable Mermaid diagram rendering (requires `mermaid-filter` installed separately) |

### Examples

**Convert a single file:**
```bash
md2doc report.md
```
Creates `report.docx` in the current directory.

**Convert multiple files:**
```bash
md2doc chapter1.md chapter2.md chapter3.md
```

**With hard line breaks preserved:**
```bash
md2doc --hard-breaks notes.md
```

## Custom Reference Document

Place a Word template at `~/.config/md2doc/reference.docx` to customize the output styling.
This reference document controls fonts, spacing, heading styles, and other formatting. Pandoc
applies these styles automatically when the file is present.

## Workflow

1. Identify the markdown file(s) the user wants to convert
2. Run `md2doc` with appropriate flags
3. Report the output file path(s) to the user
