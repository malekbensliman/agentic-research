# Repo skeleton design — 2026-06-05

First sub-project of the `agentic-research` workshop repo: lay down the full directory scaffold so every deliverable has a home.

## Decision: full scaffold

Chosen over a lean skeleton: create all folders up front (`slides`, `onepager`, `marketplace`, `activities`, `scripts`, `docs`, `.claude`) so structure is settled and nothing surprises us later. Render tooling and the marketplace manifest start as stubs.

## Structure

See `../README.md` for the folder map and `../AGENTS.md` for project context.

## Decisions

- **D1 — `AGENTS.md` is the real context file.** Adopted. `CLAUDE.md` is a one-line `@AGENTS.md` shim so context is portable across agents (Claude Code reads `CLAUDE.md`; Cursor / Codex read `AGENTS.md`).
- **D2 — Explanatory output style + an elaborate `settings.json`.** The repo commits an **Explanatory** output style in `.claude/settings.json`, and that file is intentionally **more elaborate than a typical personal repo**. Rationale (Malek, 2026-06-05): assume most faculty do NOT have a personal dotfiles setup, so the repo should be batteries-included and give a good out-of-box experience. Malek overrides locally via `settings.local.json` for his own building sessions.
- **D3 — Marketplace location.** Lives as a subdirectory for now — a marketplace does not need its own repository (a local path or subdir is valid; a separate repo is only needed if faculty add it remotely by `owner/repo`). Split it out if/when that day comes.
- **D4 — Render tool.** Deferred to the slides sub-project. Candidates: Pandoc (editable pptx), Quarto (academic-friendly), Marp / Slidev (HTML decks).
- **D5 — Rendered decks.** Gitignored. Markdown is the source of truth; final `.pptx` live in Google Drive for cross-machine polish.

## The elaborate `settings.json` (in progress)

Because faculty lack Malek's dotfiles, `.claude/settings.json` aims to be a good default environment. Candidates (pending verification of exact keys against current docs + Malek's sign-off):

- `outputStyle: "Explanatory"` — teaching mode by default.
- Pre-register the CBS marketplace so it's available when the folder is opened.
- A curated, conservative permission allow-list for clearly-safe commands, to reduce prompt fatigue without hiding the permission model the course teaches.

## Deferred / future

- A possible `dotfiles/` folder (minimal auto-install for git / tmux / VS Code) — added if Malek decides to include setup automation.
