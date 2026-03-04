# Markdown Conventions for SynthKit

These conventions ensure AI-generated Markdown converts cleanly through SynthKit's pipeline (pandoc → Word, HTML, PDF, or clipboard email).

## Headings

- Use ATX-style headings (`#`, `##`, `###`) — not underline-style
- Start the document with a single `#` heading (becomes the document title)
- Use `##` for major sections, `###` for subsections
- Avoid going deeper than `###` — deep nesting converts poorly to Word

## Lists

- Bulleted lists don't require a blank line before them (SynthKit handles this via `+lists_without_preceding_blankline`)
- Use `-` for bullets (not `*` or `+`) for consistency
- Nested lists: indent with 4 spaces
- Numbered lists: use `1.` for all items (let the renderer handle numbering)

## Tables

- Use pipe tables with a header row and separator
- Align columns with colons in the separator row if needed: `|:---|:---:|---:|`
- Keep tables simple — complex merged cells don't survive format conversion
- For wide tables, keep column count to 5 or fewer for Word output

```markdown
| Column A | Column B | Column C |
|----------|----------|----------|
| data     | data     | data     |
```

## Emphasis

- Use `**bold**` for strong emphasis
- Use `*italic*` for mild emphasis
- Avoid `***bold italic***` — rendering varies across formats

## Code

- Inline code: single backticks `` `like this` ``
- Code blocks: triple backticks with language identifier
- Code blocks convert to monospace in Word and styled `<pre>` in HTML

## Links and Images

- Use standard Markdown links: `[text](url)`
- Images: `![alt text](path)` — use relative paths for local images
- Images should be in a common format (PNG, JPG) for cross-format compatibility

## What to Avoid

- HTML tags — pandoc handles them inconsistently across output formats
- Footnotes — support varies by output format
- Raw LaTeX — only works for PDF output
- Tab characters for indentation — use spaces
- Trailing whitespace for line breaks — use `--hard-breaks` flag instead
