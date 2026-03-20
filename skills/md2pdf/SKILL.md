---
name: md2pdf
user-invocable: true
argument-hint: [file.md ...]
allowed-tools: Bash(md2pdf *), Bash(synthkit pdf *), Read, Write
model: claude-sonnet-4-6
effort: low
description: >
  Convert Markdown files to PDF using weasyprint as the PDF engine. Use this skill when the
  user wants to create a PDF from a markdown file, or says things like "make a PDF",
  "convert to PDF", "export as PDF", or "/md2pdf".
---

# Markdown to PDF

Convert one or more Markdown files to PDF using pandoc with weasyprint as the CSS-based PDF
engine. No LaTeX installation needed — weasyprint handles PDF rendering via HTML/CSS.

## Usage

Run the conversion using the `md2pdf` CLI command:

```bash
md2pdf $ARGUMENTS
```

Or via the unified CLI:

```bash
synthkit pdf $ARGUMENTS
```

### Options

| Flag | Description |
|------|-------------|
| `--hard-breaks` | Preserve line breaks from the source markdown (newlines become `<br>`) |
| `--mermaid` | Enable Mermaid diagram rendering (requires `mermaid-filter` installed separately) |

### Examples

**Convert a single file:**
```bash
md2pdf report.md
```
Creates `report.pdf` in the current directory.

**Convert multiple files:**
```bash
md2pdf chapter1.md chapter2.md chapter3.md
```

**With hard line breaks preserved:**
```bash
md2pdf --hard-breaks notes.md
```

**With Mermaid diagrams:**
```bash
md2pdf --mermaid design-doc.md
```

## Custom Styling

Place a CSS file at `~/.config/md2pdf/style.css` to customize the PDF appearance. This
stylesheet is automatically applied to all conversions when present.

## System Dependencies

Weasyprint requires system libraries (pango, cairo, gobject):
- **macOS:** `brew install pango`
- **Ubuntu/Debian:** `sudo apt install libpango1.0-dev libcairo2-dev libgdk-pixbuf2.0-dev`

The command will show a helpful error message if these are missing.

## Workflow

1. Identify the markdown file(s) the user wants to convert
2. Run `md2pdf` with appropriate flags
3. Report the output file path(s) to the user
