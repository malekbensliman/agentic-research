# AGENTS.md

Portable project context for any AI agent working in this repo. (`CLAUDE.md` imports this file, so Claude Code reads it too.)

## What this project is

Materials for a **two-session workshop teaching Columbia Business School (CBS) faculty to use agentic AI — primarily Claude Code — for academic research.** Co-created by Malek Ben Sliman and Jesse Schreger (Columbia GSB).

The organizing frame is **"The Modern Researcher's Tech Stack":** the course is a set of self-contained ~15–20 minute modules (git, VS Code, the terminal, the ways to use Claude, context management, MCP / skills / plugins / subagents, remote work) that combine into one workflow.

### Session 1 — Integrating AI tools into the research workflow
For faculty who have not yet integrated Claude Code. Install/config; the four ways to use Claude (Chat → Cowork → VS Code extension → terminal/CLI); Columbia access & pricing; privacy/data sharing; operating modes (plan, accept-edits, auto, skip-permissions); context window & `/compact`; essential slash commands; `CLAUDE.md` as memory; a chatbot-vs-Claude-Code demo (Treasury International Capital data); git basics. Ends with take-home assignments.

### Session 2 — AI for academic research
Hands-on; faculty run their own research live. Skills, MCP, plugins, subagents; output styles for academic writing; git worktrees; remote work (teleport, remote-control, `claude --remote`, the Research Grid via SSH + tmux/zellij/cmux); collaborative demos (e.g. WRDS CDS series vs. news events; Qualtrics MCP); LLMs for unstructured data (EDGAR → DuckDB/parquet, API calls); a personal-projects assignment.

## Deliverables

1. **Slides** — one markdown content doc per module, rendered to `.pptx`.
2. **One-pager** — a one-page cheat sheet (definitions + key commands).
3. **Marketplace** — a CBS Claude Code marketplace of useful plugins.
4. **Activities** — sample repos faculty point Claude Code at.

## Conventions for working in this repo

- **Markdown is the source of truth; `.pptx` / `.pdf` are render targets.** Edit the `.md`, then render — never hand-edit a generated deck.
- Keep each module's slide content in its own file under `slides/session-N/`.
- The one-pager is generated from / kept in sync with slide content, so definitions and commands never drift.
- Teaching stance: present setups that work for us, not a single prescribed "right" way; recommend Claude Code but support Codex users; go fast past Chat/Cowork and spend the time on the terminal + VS Code.

## Repo structure

See `README.md` for the folder map and `docs/` for design decisions.
