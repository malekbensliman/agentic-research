# scripts/

Render tooling: markdown → CBS-branded `.pptx` via **Pandoc** (decision made — editable text boxes that polish cleanly in PowerPoint / Cowork).

## Build the deck
```bash
scripts/build.sh                 # -> build/MASTER.pptx
scripts/build.sh out/talk.pptx   # custom output path
```
`build.sh` preprocesses `slides/MASTER.md` and runs Pandoc with the CBS template as the reference doc (`--reference-doc=templates/cbs-template.pptx --slide-level=3`).

## Files
- `build.sh` — entry point (preprocess → pandoc).
- `prep_notes.py` — preprocessor: strips our YAML front-matter / HTML comments / `_~min_` duration notes / `**On slide:**` labels; cleans `### Slide — X` titles to `X`; turns `**Notes:**` blockquotes into Pandoc `::: notes` speaker-note divs.
- `slim_template.py` — one-off: turns a full CBS deck into a tiny reference template (drops content slides + unused media). Already applied → `templates/cbs-template.pptx` is ~92 KB.

## How the markdown maps to slides
- `#` Session and `##` Module → section-divider slides.
- `### Slide — Title` → a content slide: `On slide` bullets become the body, `Notes` go to the notes pane, `Visual:` marks where a diagram / screenshot goes.

## One-pager
- `onepager/` markdown → `.docx` / `.pdf` (also Pandoc) — TODO.
