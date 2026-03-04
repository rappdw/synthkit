# Weekly Status Report

Generate a weekly status report in Markdown format. The output will be converted to Word/PDF via SynthKit, so follow these conventions:

## Structure

Use this exact heading structure:

```
# Weekly Status Report — [Team Name] — [Date Range]

## Executive Summary
[2-3 sentence overview of the week]

## Completed This Week
- [Item with brief description]
- [Item with brief description]

## In Progress
| Initiative | Status | Owner | Target Date |
|------------|--------|-------|-------------|
| ...        | ...    | ...   | ...         |

## Blockers & Risks
- **[Blocker name]** — [Description and mitigation]

## Next Week
- [Planned item]
- [Planned item]

## Metrics
| Metric | This Week | Last Week | Trend |
|--------|-----------|-----------|-------|
| ...    | ...       | ...       | ...   |
```

## Formatting Rules

- Use `#` for the title, `##` for sections — no deeper nesting
- Tables for anything with multiple columns (status tracking, metrics)
- Bulleted lists for sequential items (completed, planned)
- Bold for emphasis on blocker names and key terms
- No horizontal rules between sections (headings provide structure)
- No code blocks unless reporting on technical work

## Tips

- Keep the executive summary to 2-3 sentences — it's what leadership reads
- Status tables should fit on one page when converted to Word
- Use concrete language: "Shipped feature X" not "Made progress on feature X"

## Conversion

```bash
synthkit doc weekly-report.md    # → weekly-report.docx
synthkit pdf weekly-report.md    # → weekly-report.pdf
synthkit email weekly-report.md  # → clipboard (paste into email)
```
