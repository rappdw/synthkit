---
name: md2email
user-invocable: true
argument-hint: [file.md]
allowed-tools: Bash(md2email *), Bash(synthkit email *), Read, Write
model: claude-sonnet-4-6
effort: low
description: >
  Convert a Markdown file to clipboard-ready email. Use this skill when the user wants to
  turn markdown into an email they can paste, or says things like "make this an email",
  "copy as email", "prepare for email", or "/md2email".
---

# Markdown to Email

Convert a single Markdown file to formatted email content and copy it to the clipboard. On
macOS, the content is converted to RTF for rich-text pasting. On other platforms, HTML is
copied via pyperclip.

## Usage

Run the conversion using the `md2email` CLI command:

```bash
md2email $ARGUMENTS
```

Or via the unified CLI:

```bash
synthkit email $ARGUMENTS
```

**Note:** Unlike the other converters, `md2email` takes a single file (not multiple).

### Options

| Flag | Description |
|------|-------------|
| `--hard-breaks` | Preserve line breaks from the source markdown |
| `--mermaid` | Enable Mermaid diagram rendering (requires `mermaid-filter` installed separately) |

### Examples

**Convert and copy to clipboard:**
```bash
md2email update.md
```
The formatted content is now on your clipboard — paste into your email client.

**With hard line breaks:**
```bash
md2email --hard-breaks meeting-notes.md
```

**Smart file finding** — the `.md` extension is optional:
```bash
md2email update
```
This finds and converts `update.md`.

## Custom Styling

Place a CSS file at `~/.config/md2email/style.css` to customize the email formatting.

## Platform Behavior

- **macOS:** Converts HTML → RTF via `textutil`, then copies to clipboard with `pbcopy`. This
  produces the best results when pasting into mail clients (Mail.app, Outlook, Gmail).
- **Other platforms:** Copies HTML to clipboard via `pyperclip`. Most modern email clients
  handle HTML paste well.

## Workflow

1. Identify the markdown file the user wants to email
2. Run `md2email` with appropriate flags
3. Tell the user the content is on their clipboard, ready to paste
