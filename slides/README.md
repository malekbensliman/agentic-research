# slides/

The whole workshop currently lives in one master deck for fast review:

**[`MASTER.md`](MASTER.md)** — both sessions, ~60 slides.
- Session 1 — Integrating AI tools into the research workflow (10 modules)
- Session 2 — AI for academic research (9 modules)

We'll split it into per-module files under `session-1/` and `session-2/` later.

- `assets/` — images referenced by slides (screenshots, diagrams).
- `_TEMPLATE.md` — the per-module format (for when we split).

**Markdown is the source of truth.** Decks (`.pptx`) render from `MASTER.md` via Pandoc + `../templates/cbs-template.pptx` (see `../scripts/` and `../templates/cbs-style.md`); rendered decks aren't committed — edit the markdown, then render.
