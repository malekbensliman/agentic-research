# When Words Sweat Activity — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `activities/when-words-sweat/` — a small shareable Prosper dataset plus setup-first prompts that let a CBS faculty member exercise the Claude Code desktop app end-to-end (EDA → simple model → richer-feature model → Qualtrics survey).

**Architecture:** A reproducible reducer script turns a 346 MB source CSV into a ~10k-row shareable CSV/parquet. Faculty-facing content (data dictionary, prompts, `.claude/` config, README) is generated to match the actual reduced columns. Author-facing solution notes record real model numbers so a faculty run can be checked.

**Tech Stack:** Python via `uv` inline deps (pandas, pyarrow, scikit-learn); markdown + JSON content.

## Global Constraints

- Target is **funding success** (`granted` 0/1); NO default modeling.
- Reduced dataset: **~10,000 rows**, stratified by `granted`, **natural ~12.3% funded rate preserved**.
- **Leakage columns MUST be absent** from the shared file: `BorrowerRate`, `LenderYield`, `EffectiveYield`, `EstimatedReturn`, `EstimatedLoss`, `AmountFunded`, `PercentFunded`, `MonthlyLoanPayment`, `Status`, any `Prosper*` repayment field.
- Drop `BorrowerCity` (privacy); keep `borrower_state`.
- Source file `prosper_archive_processed_with_compettion_2025_.csv` stays gitignored; reduced `prosper_loans.{csv,parquet}` ARE tracked.
- Environment is the **Claude Code desktop app** (Code tab; `/init`, `/output-style`, MCP Connectors). Prompts assume real Python execution.
- Commit messages end with `Claude-Session: https://claude.ai/code/session_01MAZudSVzLUZUEZRy1eXfGH`. Work stays on branch `activity-when-words-sweat`; only files created by this plan are staged.

---

### Task 1: Reducer script `prepare_dataset.py`

**Files:**
- Create: `activities/when-words-sweat/prepare_dataset.py`
- Output (generated, tracked): `activities/when-words-sweat/prosper_loans.csv`, `activities/when-words-sweat/prosper_loans.parquet`

**Interfaces:**
- Produces the reduced dataset with these exact snake_case columns:
  `key, date, granted, funded, amount_requested, credit_score_lower, credit_score_upper, debt_to_income, is_homeowner, category, loan_term_months, prior_listings, total_prosper_loans, borrower_state, title, description, num_words, concrete, positive_emotion, negative_emotion, confidence_commitment, personal_struggles, urgency_momentum`
- Column source map (original → friendly): `Key→key`, `Date→date`, `Granted→granted`, `AmountRequested→amount_requested`, `CreditScoreRangeLower→credit_score_lower`, `CreditScoreRangeUpper→credit_score_upper`, `DebtToIncomeRatio→debt_to_income`, `IsBorrowerHomeowner→is_homeowner`, `Category→category`, `LoanTermInMonths→loan_term_months`, `NumPriorListing→prior_listings`, `TotalProsperLoans→total_prosper_loans`, `BorrowerState→borrower_state`, `Title→title`, `Description→description`, `Concrete_liwc→concrete`, `Positive_emotion_liwc→positive_emotion`, `Negative_emtion_liwc→negative_emotion`, `Confidence & Commitment_liwc→confidence_commitment`, `Personal Struggles & Emotional Appeals_liwc→personal_struggles`, `Urgency & Momentum_liwc→urgency_momentum`. `funded` = `granted.map({1:"funded",0:"expired"})`. `num_words` = whitespace token count of raw `description` (re-derived, human-readable — the source `NumWords` is z-scored).

- [ ] **Step 1: Write the script** with argparse (`--source`, `--n`, `--seed`, `--out-dir`), reading only the mapped source columns via `usecols`, stratified sampling by `Granted` preserving rate, renaming, deriving `funded` and `num_words`, writing csv + parquet. Print a summary (rows, funded rate, columns).

- [ ] **Step 2: Run it**

Run: `cd activities/when-words-sweat && uv run --with pandas --with pyarrow python prepare_dataset.py --source ../../prosper_archive_processed_with_compettion_2025_.csv --n 10000 --seed 42`
Expected: prints `rows: 10000`, `funded rate: 0.12x`, and 23 columns.

- [ ] **Step 3: Verify output** (assertions in a one-off check)

Run:
```bash
uv run --with pandas python - <<'PY'
import pandas as pd
d=pd.read_csv("activities/when-words-sweat/prosper_loans.csv")
assert len(d)==10000, len(d)
assert abs(d.granted.mean()-0.1233)<0.02, d.granted.mean()
need=set("key date granted funded amount_requested credit_score_lower credit_score_upper debt_to_income is_homeowner category loan_term_months prior_listings total_prosper_loans borrower_state title description num_words concrete positive_emotion negative_emotion confidence_commitment personal_struggles urgency_momentum".split())
assert set(d.columns)==need, set(d.columns)^need
leak={"BorrowerRate","LenderYield","AmountFunded","PercentFunded","EstimatedReturn","Status","borrower_rate","amount_funded"}
assert not (leak & set(d.columns)), leak & set(d.columns)
assert d.description.notna().all()
print("OK: rows, rate, columns, no-leakage, text all verified")
PY
```
Expected: `OK: rows, rate, columns, no-leakage, text all verified`

- [ ] **Step 4: Commit**

```bash
git add activities/when-words-sweat/prepare_dataset.py activities/when-words-sweat/prosper_loans.csv activities/when-words-sweat/prosper_loans.parquet
git commit -m "Add When Words Sweat dataset reducer + reduced 10k dataset" -m "Claude-Session: https://claude.ai/code/session_01MAZudSVzLUZUEZRy1eXfGH"
```

---

### Task 2: `DATA_DICTIONARY.md`

**Files:**
- Create: `activities/when-words-sweat/DATA_DICTIONARY.md`

**Interfaces:**
- Consumes: the 23 columns produced by Task 1.

- [ ] **Step 1: Write the dictionary** — a table (column | type | meaning), a "target" note on `granted`/`funded`, a "text & theme features" note (themes are z-scored psychological-dictionary scores; higher = more of that quality), a **"Deliberately omitted — would leak the target"** section listing the excluded post-funding fields and *why*, and a provenance/credit block (Netzer, Lemaire & Herzenstein, *When Words Sweat*, JMR 2019; shared by Alain Lemaire for teaching; public Prosper listings, 2007–2008).

- [ ] **Step 2: Verify coverage**

Run:
```bash
uv run --with pandas python - <<'PY'
import pandas as pd,re
cols=set(pd.read_csv("activities/when-words-sweat/prosper_loans.csv",nrows=1).columns)
txt=open("activities/when-words-sweat/DATA_DICTIONARY.md").read()
missing=[c for c in cols if c not in txt]
assert not missing, f"columns missing from dictionary: {missing}"
print("OK: every column documented")
PY
```
Expected: `OK: every column documented`

- [ ] **Step 3: Commit**
```bash
git add activities/when-words-sweat/DATA_DICTIONARY.md
git commit -m "Add data dictionary for When Words Sweat dataset" -m "Claude-Session: https://claude.ai/code/session_01MAZudSVzLUZUEZRy1eXfGH"
```

---

### Task 3: `.claude/` config + folder `README.md`

**Files:**
- Create: `activities/when-words-sweat/.claude/settings.json`
- Create: `activities/when-words-sweat/README.md`

- [ ] **Step 1: Write `.claude/settings.json`** — set `outputStyle: "explanatory"`, permission allows for `uv run`/python reads, and (if the repo marketplace name is known) reference the CBS marketplace. Do NOT ship a `CLAUDE.md` (P0's `/init` creates it live).

- [ ] **Step 2: Write `README.md`** — what the activity is, the funding-success question, the 4-step arc, "open this folder in the Claude Code desktop app → follow PROMPTS.md", and the credit note.

- [ ] **Step 3: Verify JSON valid**

Run: `python3 -c "import json;print('outputStyle',json.load(open('activities/when-words-sweat/.claude/settings.json'))['outputStyle'])"`
Expected: `outputStyle explanatory`

- [ ] **Step 4: Commit**
```bash
git add activities/when-words-sweat/.claude/settings.json activities/when-words-sweat/README.md
git commit -m "Add inherited .claude config and README for the activity" -m "Claude-Session: https://claude.ai/code/session_01MAZudSVzLUZUEZRy1eXfGH"
```

---

### Task 4: `PROMPTS.md`

**Files:**
- Create: `activities/when-words-sweat/PROMPTS.md`

- [ ] **Step 1: Write the prompts** in two acts.
  - **Act 1 — Setup (smoke-test):** open folder in the Code tab; `/init`; `/output-style explanatory` (framed as view/confirm/switch); connect the Qualtrics MCP via Connectors, then `/mcp` to confirm connected.
  - **Act 2 — Analysis:** P1 EDA → self-contained `eda_report.html`; P2 logistic regression on structured features only, report ROC-AUC + PR-AUC + top coefficients, with the leakage warning; P3 add language (num_words, TF-IDF max_features=500, theme scores), same learner, show AUC lift + top language features, plus optional "build your own confidence dictionary" sub-prompt; P4 design a between-subjects Qualtrics experiment varying one theme (willingness-to-fund 0–100) and create it via MCP, degrading to a drafted spec if MCP absent.
  - Each prompt is a fenced copy-paste block with a one-line "what you should see."

- [ ] **Step 2: Verify** the file references the real dataset filename and all four analysis prompts exist.

Run: `grep -c 'prosper_loans' activities/when-words-sweat/PROMPTS.md && grep -Eo 'P[1-4]' activities/when-words-sweat/PROMPTS.md | sort -u`
Expected: nonzero count and `P1 P2 P3 P4`.

- [ ] **Step 3: Commit**
```bash
git add activities/when-words-sweat/PROMPTS.md
git commit -m "Add setup-first prompt sequence for the activity" -m "Claude-Session: https://claude.ai/code/session_01MAZudSVzLUZUEZRy1eXfGH"
```

---

### Task 5: `SOLUTION_NOTES.md` with real model numbers

**Files:**
- Create: `activities/when-words-sweat/SOLUTION_NOTES.md`
- Scratch: `scratchpad/reference_run.py` (NOT committed)

**Interfaces:**
- Consumes: `prosper_loans.csv` from Task 1.

- [ ] **Step 1: Write a reference run** in scratchpad that trains both models on the reduced data (Model 1: logistic on structured; Model 2: + language via TF-IDF(500) + themes) with a train/test split and prints ROC-AUC + PR-AUC for each, plus the strongest positive/negative language coefficients and a few EDA numbers (funded rate; funded-rate by homeowner; mean theme score by funded/expired).

- [ ] **Step 2: Run it** and capture the numbers.

Run: `uv run --with pandas --with scikit-learn python scratchpad/reference_run.py`
Expected: prints two AUC pairs and coefficient/EDA lines.

- [ ] **Step 3: Write `SOLUTION_NOTES.md`** — the EDA highlights and the real AUCs (so Model 2 > Model 1 lift is documented), a note that numbers are ballpark (seed-dependent), and the "what "working" looks like" checklist for verifying a faculty run.

- [ ] **Step 4: Commit**
```bash
git add activities/when-words-sweat/SOLUTION_NOTES.md
git commit -m "Add solution notes with reference model results" -m "Claude-Session: https://claude.ai/code/session_01MAZudSVzLUZUEZRy1eXfGH"
```

---

### Task 6: Update `activities/README.md` index + open PR + merge

**Files:**
- Modify: `activities/README.md` (add a pointer to the new activity)

- [ ] **Step 1: Add a short section** to `activities/README.md` linking `when-words-sweat/` as a Session-2 marketing example.

- [ ] **Step 2: Commit**
```bash
git add activities/README.md
git commit -m "Link When Words Sweat activity from activities index" -m "Claude-Session: https://claude.ai/code/session_01MAZudSVzLUZUEZRy1eXfGH"
```

- [ ] **Step 3: Push and open PR**

Run: `git push -u origin activity-when-words-sweat` then `gh pr create` with a body summarizing the activity (ends with the session URL line).

- [ ] **Step 4: Merge** the PR once created.

---

## Self-Review

- **Spec coverage:** dataset (T1), dictionary + leakage doc (T2), `.claude` config + README (T3), setup-first prompts incl. Qualtrics (T4), reducer script + solution notes (T1/T5), activities index (T6). Provenance covered in T2/T3. All spec deliverables map to a task. ✓
- **Placeholder scan:** verification commands are concrete; content tasks specify exact sections. ✓
- **Type consistency:** the 23-column list is identical in Global Constraints, T1 interfaces, and the T1/T2 verify commands. ✓
