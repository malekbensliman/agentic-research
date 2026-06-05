# Agentic Research

Workshop materials for **using agentic AI (primarily Claude Code) to do academic research** — a two-session, hands-on course for Columbia Business School faculty.

Framing: **"The Modern Researcher's Tech Stack."** The course is taught as self-contained ~15–20 minute modules (git, VS Code, the terminal, the ways to use Claude, MCP / skills / plugins…) that snap together into one workflow.

> Status: work in progress, currently maintained by Malek. Not yet shared publicly.

## Working across machines

This repo *is* the cross-machine workflow we teach:

```bash
git pull                              # start of a work session, on any machine
git add -A && git commit -m "..."     # save progress
git push                              # once a remote is set up
```

Opening this folder in Claude Code (or any agent) auto-loads project context from `CLAUDE.md` → `AGENTS.md`, so you never have to re-explain what this project is.

## Repo map

| Path | What lives here |
|------|-----------------|
| `slides/` | Slide content, one markdown file per module (`session-1/`, `session-2/`). Markdown is the source of truth; `.pptx` is a render target. |
| `onepager/` | One-page cheat sheet — definitions + most-useful commands. |
| `marketplace/` | The CBS Claude Code marketplace (plugins faculty can install). |
| `activities/` | Sample repos faculty point Claude Code at during exercises. |
| `scripts/` | Render tooling (markdown → `.pptx`, one-pager generation). |
| `docs/` | Design notes and decisions. |

## Conventions

- **Edit the markdown, not the rendered deck.** Decks are build outputs.
- See `AGENTS.md` for full project context and `docs/` for design decisions.
