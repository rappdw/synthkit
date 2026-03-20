---
name: md2html
user-invocable: true
argument-hint: [file.md ...]
allowed-tools: Bash(md2html *), Bash(synthkit html *), Read, Write
model: claude-sonnet-4-6
effort: low
description: >
  Convert Markdown files to HTML using pandoc. Use this skill when the user wants to create
  an HTML file from markdown, or says things like "make HTML", "convert to HTML",
  "export as HTML", or "/md2html".
---

# Markdown to HTML

Convert one or more Markdown files to standalone HTML using pandoc.

## Usage

Run the conversion using the `md2html` CLI command:

```bash
md2html $ARGUMENTS
```

Or via the unified CLI:

```bash
synthkit html $ARGUMENTS
```

### Options

| Flag | Description |
|------|-------------|
| `--hard-breaks` | Preserve line breaks from the source markdown |
| `--mermaid` | Enable Mermaid diagram rendering (requires `mermaid-filter` installed separately) |

### Examples

**Convert a single file:**
```bash
md2html report.md
```
Creates `report.html` in the current directory.

**Convert multiple files:**
```bash
md2html page1.md page2.md page3.md
```

**With Mermaid diagrams:**
```bash
md2html --mermaid design-doc.md
```

## Custom Styling

Place a CSS file at `~/.config/md2html/style.css` to customize the HTML appearance. When
present, this stylesheet is embedded into the output file (`--css` + `--self-contained`),
making the HTML fully portable with no external dependencies.

## Workflow

1. Identify the markdown file(s) the user wants to convert
2. Run `md2html` with appropriate flags
3. Report the output file path(s) to the user
