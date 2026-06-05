# CBS slide template — design system

Source: extracted from a CBS course deck (B6601 / B7609) that Malek provided as the **visual template basis only** — we use its slide master / theme / layouts, **not** its content. The template lives at `cbs-template.pptx` (this folder); the original deck was deleted per Malek's instruction.

`templates/cbs-template.pptx` is the **Pandoc reference doc**: its layout names match Pandoc's standard pptx layouts, so `pandoc --reference-doc=templates/cbs-template.pptx slide.md -o deck.pptx` renders our markdown into CBS branding (Pandoc uses the master + layouts, ignores content).

## Fonts
- **Century Gothic** — titles and body (confirmed against the master view).
- (theme1.xml nominally lists Corbel, and the body XML lists Arial as a fallback level — but the deck uses Century Gothic throughout; match that.)

## Palette (theme colors)
| Role | Hex |
|------|-----|
| Primary blue (dk2 / accent1) | `#0081CC` |
| Bright blue (accent3) | `#00AFEF` |
| Light blue (accent2) | `#AAC1E2` |
| Navy (folHlink) | `#023160` |
| Greys | `#404040` · `#808080` · `#9E9A92` · `#F2F2F2` |
| Base | `#000000` on `#FFFFFF` |

## Format
- 16:9 widescreen.

## Layouts available
Use these names in each slide's layout-hint comment so Pandoc maps content correctly:

`Title Slide` · `Title and Content` · `Section Header` · `Two Content` · `Comparison` · `Title Only` · `Content with Caption` · `Picture with Caption` · `Blank`
(deck extras: `4_Blank`, `Section Divider Layout`, `1_Title and Content`, `DEFAULT`)

## Notes
- `cbs-template.pptx` is currently the full deck repurposed as the reference doc (~91 MB, kept local & git-ignored). Slim it (strip content slides + unused media) when convenient — needs `python-pptx` or a quick PowerPoint "save with content deleted".
