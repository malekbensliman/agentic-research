# Design — "When Words Sweat" hands-on activity

**Date:** 2026-07-23
**Author:** Malek Ben Sliman (with Claude Code)
**Location in repo:** `activities/when-words-sweat/`
**Status:** design approved in brainstorming; pending user review before planning.

## One-line summary

A self-contained marketing activity for CBS faculty: a small, shareable
Prosper.com loan-listing dataset plus a sequence of copy-paste prompts that
walk a faculty member from a fresh **Claude Code desktop app** setup through
EDA, a simple model, a richer-feature model, and a Qualtrics survey — all
answering one tangible question: **does the language of a loan request change
whether strangers fund it?**

## Motivation and framing

- Source: the data behind Netzer, Lemaire & Herzenstein, *"When Words Sweat:
  Identifying Signals for Loan Default in the Text of Loan Applications"*
  (JMR 2019). Shared by Alain Lemaire for teaching.
- The paper's headline outcome is **default**, but the shared files do **not**
  contain a usable default label (of 19,630 funded loans, only ~2,256 have any
  repayment field and only ~13 show a late payment — these are 2007–2008
  *listings* captured before loans resolved). Confirmed empirically across all
  three files (`Status ∈ {Expired, Completed}` only).
- We therefore re-anchor on **funding success** (`Granted`: funded vs expired).
  This is cleaner (159,158 rows, ~12.3% funded, text present for every row) and
  a purer **marketing** question — persuasion and copywriting, not credit risk.

## Audience and environment (load-bearing)

- Faculty use the **Claude Code desktop app** (released 2026-04-14; the app
  with the **Code tab**, `/init`, output styles, project `.claude/settings.json`,
  MCP via Connectors UI, and real Python execution).
- This is **not** the Claude Desktop *chat* app. Confirmed with the user.
- The activity doubles as a **setup smoke-test**: if a faculty member's app can
  open the folder, run `/init`, execute Python, and reach the Qualtrics MCP,
  the prompts simply work end-to-end.

## Deliverables (what ships in `activities/when-words-sweat/`)

### Faculty-facing
1. `prosper_loans.csv` and `prosper_loans.parquet` — the shared dataset.
2. `DATA_DICTIONARY.md` — column → plain-English meaning, provenance, and a
   "deliberately omitted (would leak)" section.
3. `PROMPTS.md` — the exercise as ordered, copy-paste prompts (Acts 1 & 2).
4. `.claude/settings.json` — inherited project config (Explanatory output style,
   sensible permissions, CBS marketplace reference) so the folder "looks like
   this repo" the moment it is opened.

### Author-facing (for Malek, to verify a faculty run)
5. `prepare_dataset.py` — reproducible reducer from a big local source file to
   the shared dataset (kept in-folder; big sources stay gitignored).
6. `SOLUTION_NOTES.md` — expected EDA highlights and ballpark model numbers.
7. `README.md` — what the activity is, how to run it, and the credit note.

## Dataset spec

- **Source:** `prosper_archive_processed_with_compettion_2025_.csv` (base file;
  159,158 rows, 138 cols — it carries both core LIWC dims and the bespoke
  "estimated" theme columns like `Confidence & Commitment_liwc`).
  `prepare_dataset.py` takes a `--source` flag to swap in the LIWC-confound file.
- **Sample:** stratified by `Granted` to lock the natural rate; **~10,000 rows**
  (≈1,230 funded). Natural imbalance is kept on purpose — it sets up the
  "accuracy lies, use ROC-AUC / PR-AUC" lesson.
- **Columns (~23, renamed to friendly snake_case):**
  - ids/meta: `key`, `date`
  - target: `granted` (0/1), `funded` (label: "funded"/"expired")
  - structured, pre-funding (no leakage): `amount_requested`,
    `credit_score_lower`, `credit_score_upper`, `debt_to_income`,
    `is_homeowner`, `category`, `loan_term_months`, `prior_listings`,
    `total_prosper_loans`, `borrower_state`
  - text: `title`, `description` (raw), `num_words` (re-derived, human-readable)
  - themes (z-scored, curated ~6): `concrete`, `positive_emotion`,
    `negative_emotion`, `confidence_commitment`, `personal_struggles`,
    `urgency_momentum`
- **Deliberately omitted — would leak the target** (documented in the
  dictionary): `BorrowerRate`, `LenderYield`, `EffectiveYield`,
  `EstimatedReturn`, `EstimatedLoss`, `AmountFunded`, `PercentFunded`,
  `MonthlyLoanPayment`, `Status`, and all `Prosper*` repayment fields — these
  only exist *after* a loan is funded.
- **Privacy:** drop `BorrowerCity`; keep `borrower_state` (US state, not PII).
- **Size target:** CSV ≈8–12 MB, parquet ≈3 MB. Commit both; gitignore the
  240–355 MB source files.

## PROMPTS.md structure

### Act 1 — Setup (proves the install works)
- **P0a** open the `when-words-sweat/` folder in the Code tab.
- **P0b** `/init` → creates `CLAUDE.md` (faculty watch it read the folder).
- **P0c** `/output-style explanatory` → customize outputs (mirrors this repo).
- **P0d** connect the **Qualtrics MCP** (Connectors UI or `.mcp.json`), then
  `/mcp` to confirm it shows **connected**.

`.claude/settings.json` ships with `outputStyle: explanatory` so the folder
already "looks like this one"; P0c is framed as *view/confirm/switch* so the
command is still taught rather than a no-op. `CLAUDE.md` is **not** shipped —
`/init` creating it live is the teaching moment.

### Act 2 — Analysis (proves it can work)
- **P1 — EDA → `eda_report.html`:** funding base rate; funded vs
  credit-score / amount / DTI; description length vs funded; 3–4 themes vs
  funded. Output is a **standalone self-contained HTML report**.
- **P2 — simple model:** logistic regression on **structured pre-funding
  features only**. Report ROC-AUC + PR-AUC (not accuracy) and top coefficients.
  Prompt teaches **leakage** explicitly (why rate/funded-amount are excluded).
- **P3 — richer features:** add language — `num_words`, TF-IDF on `description`
  (capped, e.g. `max_features=500`), and the theme scores — to the **same
  learner family**. Show the **AUC lift** over P2 and the top language features.
  Optional advanced sub-prompt: *build your own theme dictionary* (keyword-count
  a small "confidence" lexicon over `description`, add as a feature) — the
  "featurization is the interesting part" payoff, compute-light.
- **P4 — Qualtrics experiment:** the models are correlational; design a
  between-subjects experiment that varies **one theme** (e.g., high vs low
  confidence, or concrete vs vague loan description) and measures
  willingness-to-fund (0–100) plus a couple of covariates. Create it in
  Qualtrics via the MCP; if the MCP is not connected, Claude drafts the survey
  spec instead.

## Modeling notes

- Everything is laptop-fast: 10k rows, logistic + gradient boosting +
  TF-IDF(500) train in seconds. No embeddings, no long jobs.
- The "simple → complex" contrast is a **featurization ladder**, not a heavier
  model: same learner, richer features (structured → + lexical → + themes).
- Scripts use `uv` inline dependencies (pandas, pyarrow, scikit-learn,
  matplotlib) per the repo's tooling conventions.

## Non-goals (YAGNI)

- No default prediction (data does not support it).
- No embeddings / transformer featurization as a required path.
- No hand-authored notebook shipped to faculty — faculty *generate* their
  analysis via the prompts; that is the point.
- No live Qualtrics credentials assumed in the build; P4 degrades gracefully to
  a drafted survey spec.

## Open items to resolve during planning

- Confirm the repo `.gitignore` already excludes `prosper_archive_*`.
- Decide exact CBS-marketplace reference (if any) for the shipped
  `.claude/settings.json`.
- Compute real ballpark AUCs for `SOLUTION_NOTES.md` during the build.
