# Spec — PowerPoint harvester (`draft.pptx` → slide DSL)

- **Date:** 2026-06-09
- **Status:** approved design, pending spec review
- **Authors:** Malek (direction) + Claude (drafting)

## Goal

Let a faculty member draft slides in PowerPoint (their natural surface, often
content lifted from another class) and pull that content into this workshop's
canonical markdown deck (`slides/MASTER.md`), where `build.sh` re-skins it into
CBS branding.

**Why:** Malek has slides from another class to fold into the master. Editing
the rendered `build/MASTER.pptx` doesn't work — it's git-ignored and overwritten
on every render. The repo's invariant is "markdown is the source of truth; pptx
is a render target" (`AGENTS.md`).

**How to apply:** the PowerPoint is an *input you harvest from*, never a second
source of truth. A tool extracts its content to DSL markdown for review; a human
merges the wanted slides into `MASTER.md`. This preserves the single-source
invariant and keeps the one-pager + git diffs clean.

## Locked decisions

1. **Harvest-inbox model** (not bidirectional sync, not pptx-as-truth). The
   inbox `.pptx` is disposable; markdown stays canonical.
2. **Stdlib only** — read the `.pptx` as a zip via `zipfile` + `xml.etree`, the
   same pattern as `scripts/slim_template.py`. No `python-pptx`, so faculty need
   no `pip install`.
3. **Image convention = Option A** — harvested images are referenced with the
   existing `**Visual:**` convention, and `prep_notes.py` is taught to render
   `**Visual:**` lines. One unified image pipeline for hand-authored and
   harvested images alike.

## Component 1 — `scripts/harvest_pptx.py`

**Contract:** `scripts/harvest_pptx.py path/to/draft.pptx` reads the deck and
prints DSL markdown to **stdout**. It **never writes to `MASTER.md`**. It writes
extracted image binaries to `slides/assets/`.

**Slide ordering:** resolve order via `ppt/presentation.xml` `<p:sldIdLst>` →
`ppt/_rels/presentation.xml.rels`, **not** by `slideN.xml` filename (filenames
are not guaranteed to be in presentation order).

**Per slide, extract:**
- **Title** — the shape whose placeholder is `type="title"` or `type="ctrTitle"`.
  Fallback to `(untitled {N})` if absent. Emit `### Slide — {title}`.
- **Body bullets** — text from body/non-title shapes. Each `<a:p>` paragraph is
  one bullet; its `lvl` attribute (0-based) sets indent depth → nested `-`.
  Emit under `**On slide:**`.
- **Speaker notes** — text from `ppt/notesSlides/notesSlideM.xml` body
  placeholder (skip the slide-number placeholder). Emit as
  `**Notes:**` + `>` blockquote.

**Images:**
- Extract media referenced by each slide's `slideN.xml.rels` (`r:embed` → rId →
  `ppt/media/...`). Write to `slides/assets/{stem}-slide{NN}-img{M}.{ext}` where
  `{stem}` is the input filename stem (e.g. `draft`). Positional names — never
  title-derived — so odd characters / duplicate titles can't break filenames.
- **Dedup by source media:** one `ppt/media/imageX` reused on many slides (e.g.
  a logo) is written **once**; every reference points at that single file.
- Emit a `**Visual:** assets/{name} — imported from slide {N}` line per image.

**Non-text content not silently dropped:** tables / charts / SmartArt that we
don't extract become a visible
`**Visual:** (imported from slide {N}: table — needs manual handling)` line, so
the gap is on the page rather than lost.

**Error handling:** if the path is missing or not a Zip/pptx, print a clear
message to stderr and exit non-zero. Do not create partial output files.

## Component 2 — `prep_notes.py` enhancement (`**Visual:**` rendering)

Teach the existing preprocessor one rule so `**Visual:**` lines stop rendering
as literal text and become real slide content. Parse
`**Visual:** [`]<target>[`] — <description>`:

- **Target is an asset path that exists** (contains `/` or an image extension,
  and the file is present relative to `slides/`) → emit Pandoc image syntax
  `![<description>](<target>)`. Pandoc embeds it into the `.pptx`.
- **Target is a parenthetical stage direction** (e.g. `(live demo)`,
  `(hands-on)`) → move the text into the speaker-notes pane, not the slide body
  (it's a presenter cue, not audience content).
- **Target is an asset path that does NOT exist yet** (e.g. the 4 not-yet-drawn
  bespoke SVGs) → leave a short visible placeholder line so it reads as a TODO
  and the build never breaks on a missing file.

**Consequence to expect:** after this change, the 6 existing `**Visual:**` lines
in `MASTER.md` render differently — the 2 demo cues move to notes, the 4 SVG
specs show as placeholders until their assets exist. This is the intended
cleanup (today they render as stray body text).

## Out of scope (explicitly)

- **Drawing the 4 bespoke SVG diagrams** (`agent-in-repo`, `four-modes-spectrum`,
  `llm-plus-terminal`, `vscode-cockpit`) — that's artwork, still parked.
- **Auto-merging into `MASTER.md`** — merge stays human-driven (the safety
  boundary that protects existing DSL metadata: `Visual` specs, `_~min_` timing,
  comments).
- **`python-pptx`** — rejected to keep the toolchain dependency-free.

## End-to-end workflow

1. Edit / assemble slides in `slides/draft.pptx` (PowerPoint). Auto-git-ignored
   by the existing `*.pptx` rule.
2. `scripts/harvest_pptx.py slides/draft.pptx > /tmp/harvest.md` — emits DSL,
   writes images to `slides/assets/`.
3. Review `/tmp/harvest.md` together; splice wanted slides into `MASTER.md` under
   the right `##` Module.
4. `scripts/build.sh` → CBS-branded `build/MASTER.pptx` with images embedded.

## Verification

- A small fixture `.pptx` (title + nested bullets + notes + one image + one
  duplicated logo) harvests to the expected DSL; the logo lands in `assets/`
  exactly once; slide order matches presentation order.
- `prep_notes.py`: a `**Visual:**` line with an existing asset → `![…](…)`; a
  `(live demo)` line → notes; a missing-asset line → placeholder, build succeeds.
- `scripts/build.sh` renders without error and the embedded image appears on the
  slide.

## Risks

- **Messy source decks** (grouped shapes, text in tables, multi-column layouts)
  extract imperfectly. Mitigation: flag non-text as `**Visual:**` rather than
  guess; review step catches the rest.
- **Bullet nesting** beyond what `lvl` captures may flatten. Acceptable for v1.
