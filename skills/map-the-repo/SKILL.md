---
name: map-the-repo
user-invocable: true
description: >
  Generate comprehensive documentation and a browsable wiki for any codebase. Use this skill
  whenever the user wants to document a repo, generate a wiki, understand architecture, produce
  onboarding docs, map dependencies, or says things like "document this repo", "explain this
  codebase", "map the repo", "generate a wiki", "architecture docs", "I need to understand
  this project", or "onboard me". Also useful when handing off a repo to a new engineer or
  agent. This is the documentation companion to /explore-with-me — explore first to understand,
  then map to document.
---

# Map the Repo

Generate a browsable wiki from a codebase. The script produces structural scaffolding; your
job is to enrich it with genuine architectural insight.

## Workflow

### 1. Orient

Before running the script, build context:

- Check for existing discovery output (init-discovery CLAUDE.md, explore-with-me findings)
  and use it to inform your understanding
- Read `README.md`, `pyproject.toml` / `package.json` / `go.mod` / `Cargo.toml` to identify
  the language, framework, and project type
- Scan the top-level directory structure to understand the layout

### 2. Run the Script

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/map-the-repo/scripts/map.py --repo-path . --output-path ./wiki
```

The script generates:
- `wiki/docs/*.md` — Markdown documentation (index, architecture, data flows, API reference,
  glossary, per-module docs)
- `wiki/site/index.html` — Self-contained browsable site (dark theme, search, Mermaid diagrams)

### 3. Enrich

This is the critical step. The script produces structure — file listings, function signatures,
import graphs. You provide understanding.

Read every generated file in `wiki/docs/` and rewrite weak sections:

- **`architecture.md`** — The Mermaid diagram should immediately convey system shape. Add
  prose explaining *why* the system is structured this way, not just *what* the structure is.
  Note key design decisions and their tradeoffs.

- **`data-flows.md`** — Add sequence diagrams for the 2-3 most important flows through the
  system. Explain what triggers each flow and what the end state is.

- **Module docs** (`modules/*.md`) — Each should read like a senior engineer wrote it after
  a day in the code. Explain the module's role in the system, its key abstractions, and any
  non-obvious behavior. Don't just list functions — explain what problems they solve.

- **`glossary.md`** — Add domain-specific terms that a new engineer would need to understand.
  Define them in the context of this specific codebase, not generic definitions.

- **`api-reference.md`** — Verify signatures are correct. Add usage examples for the most
  important public APIs.

After enriching the markdown files, regenerate the HTML site to pick up your changes:

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/map-the-repo/scripts/map.py --repo-path . --output-path ./wiki --rebuild-site
```

### 4. Present

Tell the user:
- Where to open the site (`wiki/site/index.html`)
- What was found (number of modules, public APIs, key architectural patterns)
- Any areas where the documentation is thin and could use human input
