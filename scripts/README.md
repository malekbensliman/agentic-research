# scripts/

Render tooling: markdown → CBS-branded `.pptx` via **Pandoc** (decision made — editable text boxes that polish cleanly in PowerPoint / Cowork).

## Build the deck
```bash
scripts/build.sh                 # -> build/MASTER.pptx
scripts/build.sh out/talk.pptx   # custom output path
```
`build.sh` preprocesses `slides/MASTER.md` and runs Pandoc with the CBS template as the reference doc (`--reference-doc=templates/cbs-template.pptx --slide-level=3`).

## Live preview (CBS-themed, in your browser)
```bash
scripts/preview.sh        # one-shot  -> build/MASTER.html (opens once)
scripts/watch.sh          # real-time -> re-render on save + live-reload the browser
```
Same markdown + preprocessing as the pptx build, rendered to a CBS-skinned reveal.js deck. Edit markdown → re-run → refresh. (Needs internet — reveal.js loads from a CDN.) The CBS look is a CSS twin of the `.pptx` master; for exact PowerPoint fidelity use `build.sh`.

## Files
- `build.sh` — entry point for the `.pptx` (preprocess → pandoc).
- `preview.sh` — one-shot reveal.js HTML preview (CBS CSS skin).
- `watch.sh` — **real-time** preview: re-renders on save + live-reloads the browser (needs node/npx for browser-sync).
- `cbs-theme.html` — the inline CSS skin for the preview.
- `prep_notes.py` — preprocessor: strips our YAML front-matter / HTML comments / `_~min_` duration notes / `**On slide:**` labels; cleans `### Slide — X` titles to `X`; turns `**Notes:**` blockquotes into Pandoc `::: notes` speaker-note divs.
- `slim_template.py` — one-off: turns a full CBS deck into a tiny reference template (drops content slides + unused media). Already applied → `templates/cbs-template.pptx` is ~92 KB.

## How the markdown maps to slides
- `#` Session and `##` Module → section-divider slides.
- `### Slide — Title` → a content slide: `On slide` bullets become the body, `Notes` go to the notes pane, `Visual:` marks where a diagram / screenshot goes.

## One-pager
- `onepager/` markdown → `.docx` / `.pdf` (also Pandoc) — TODO.
