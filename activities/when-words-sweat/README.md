# When Words Sweat — does language get your loan funded?

A hands-on marketing activity for the **Agentic Research** workshop. You point the
**Claude Code desktop app** at this folder and drive it through a real analysis —
which also confirms your whole setup works: file access, Python, and an MCP server.

## The question

On Prosper.com (a peer-to-peer lending site), a borrower writes a free-text loan
request and strangers decide whether to fund it. **Does *how* you write the
request — not just your credit — change whether you get funded?** That is a pure
marketing question: persuasion, framing, word choice.

You get 10,000 real 2007–2008 listings (`prosper_loans.csv`). ~12% were funded.
See `DATA_DICTIONARY.md` for the columns; the star is `description` (the request
text) and the target is `granted` (funded vs expired).

## What you'll do (≈20 min)

Open this folder in the Claude Code desktop app (**Code** tab), then work through
`PROMPTS.md` in order:

1. **Setup** — `/init`, pick an output style, connect the Qualtrics MCP. If these
   work, your environment is good.
2. **EDA** — Claude builds a browsable `eda_report.html`.
3. **Simple model** — predict funding from financials alone (and learn why we must
   *exclude* post-funding fields — target leakage).
4. **Richer model** — add the language of the request; watch the accuracy lift and
   see *which words* fund a loan.
5. **Survey** — the models are correlational; have Claude design and create a
   Qualtrics experiment to test whether the language *causes* funding.

## Files

| File | For |
|---|---|
| `prosper_loans.csv` / `.parquet` | the dataset (open in Excel, pandas, or Claude) |
| `DATA_DICTIONARY.md` | what every column means (+ what we omitted and why) |
| `PROMPTS.md` | the copy-paste exercise, in order |
| `.claude/settings.json` | inherited config (Explanatory output style + sensible permissions) |
| `prepare_dataset.py` | how the big source file was reduced to this one (reference) |
| `SOLUTION_NOTES.md` | what a good run looks like (for the instructor) |

## Credit

Data behind Netzer, Lemaire & Herzenstein, *"When Words Sweat"* (JMR 2019); public
Prosper listings, shared by **Alain Lemaire** for teaching. Keep the credit line if
you reuse it.
