# scripts/

Render tooling for turning the markdown sources into distributables:

- `slides/` markdown → `.pptx`
- `onepager/` markdown → `.docx` / `.pdf`

**Render tool not yet chosen.** Candidates under consideration:

- **Pandoc** — markdown → editable `.pptx` (real text boxes; good for polishing in PowerPoint / Cowork).
- **Quarto** — academic-friendly (R / Python / Stata-adjacent), markdown-native, renders via Pandoc.
- **Marp / Slidev** — great HTML decks for live presenting, but not editable `.pptx`.

Decision deferred to the slides sub-project.
