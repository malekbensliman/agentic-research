# The activity — copy-paste prompts, in order

Open **this folder** in the Claude Code desktop app (the **Code** tab → open the
`when-words-sweat` folder). Then paste these one at a time. Each block says what
you should see, so you can tell it worked.

> The point of Act 1 is to prove your setup works. The point of Act 2 is to get a
> real result. If Act 1 succeeds, the rest will too.

---

## Act 1 — Setup (this is the smoke-test)

### P0.1 — Let Claude read the project

```
Summarize this folder: what's the dataset, what does each column mean, and what question are we trying to answer? Read the README and DATA_DICTIONARY first.
```

**You should see:** a short summary — 10,000 Prosper loan listings, target is
`granted` (funded vs expired), the goal is predicting funding from the request's
language. If Claude can read the files, your file access works.

### P0.2 — Create project memory

```
/init
```

**You should see:** Claude writes a `CLAUDE.md` file describing this project. This
is the memory it will reuse every session — open it and skim it.

### P0.3 — Set how Claude explains things

```
/output-style explanatory
```

**You should see:** the style switch to **Explanatory** (this folder already ships
it, so you're confirming it). Try `/output-style` on its own to see the menu and
the other styles, e.g. **Learning**.

### P0.4 — Connect the Qualtrics MCP (for the last step)

Add the Qualtrics MCP through the desktop app's **Connectors** UI (or a project
`.mcp.json`). Then check it:

```
/mcp
```

**You should see:** the Qualtrics server listed as **connected**. If you don't have
Qualtrics set up yet, that's fine — you can still do P1–P3 and treat P4 as a draft.

---

## Act 2 — The analysis (get a real result)

### P1 — Explore the data → an HTML report

```
Do an exploratory analysis of prosper_loans.csv aimed at one question: what separates funded listings from expired ones? Cover the funding base rate, funded rate by credit score and by homeowner status, description length (num_words) vs funding, and how the language theme flags (concrete, confidence_commitment, personal_struggles, urgency_momentum) differ between funded and expired. Note in the report that amount_requested, debt_to_income, and prior_listings are standardized (z-scored), not raw units. Save everything as a single self-contained eda_report.html I can open in a browser, with charts and short written takeaways.
```

**You should see:** a new `eda_report.html`. Open it. Expect funded listings to
have **higher credit scores** and **longer descriptions**.

### P2 — A simple model: funding from the numbers only

```
Train a simple, interpretable model (logistic regression) that predicts `granted` from the structured financial columns only: amount_requested, credit_score_lower, credit_score_upper, debt_to_income, is_homeowner, category (as categorical), prior_listings. Scale the numeric features so it converges. Use a train/test split and report ROC-AUC and PR-AUC — not accuracy, because only ~12% are funded so accuracy is misleading. Then show the strongest coefficients.

Important: do NOT use any field that only exists after a loan is funded (rate, funded amount, yields, status) — that would be target leakage. Those are already excluded from this file; tell me which columns you used.
```

**You should see:** a baseline **ROC-AUC around 0.79–0.84** (exact value depends on
the split and whether features are scaled), and a short note on which features
matter — credit score dominates. This is "the numbers alone."

### P3 — A richer model: add the language

```
Now add the language of the request to the same kind of model and see if it helps. Build features from the text: num_words, a TF-IDF of `description` (max_features=500, English stop words, min_df=5), and the six theme flags. Combine them with the structured features from before, retrain, and compare ROC-AUC and PR-AUC against the structured-only model. Then show me the words most associated with getting funded and the words most associated with expiring.
```

**You should see:** the AUC **rise to about 0.85–0.88** — a real lift (≈+0.05) from
language alone. And the words tell the story: funded requests read concrete and
financially literate (*balances, card, term, excellent*); expired ones read
desperate and vague (*need, chance, payday, unable*). Words that sweat.

**Optional — build your own dictionary (the interesting bit).** You don't need a
big model to capture a theme; you can just count words:

```
Make a small "confidence" word list (e.g. will, plan, confident, guarantee, committed, repay) and a "desperation" word list (e.g. need, please, desperate, hope, chance, help). Score each description by how many words from each list it contains, add those two scores as features, and tell me whether they move funding in the direction we'd expect.
```

### P4 — From correlation to causation: a Qualtrics experiment

The models only show *association* — confident writers may also have better credit.
To test whether the *wording* causes funding, you need an experiment.

```
Design a between-subjects survey experiment to test whether confident (vs desperate) wording in a loan request makes people more willing to fund it. Write two versions of the same loan request that differ only in that tone, keeping the facts identical. Respondents see one version and rate willingness-to-fund from 0 to 100, plus a couple of covariates (perceived trustworthiness, perceived risk). If the Qualtrics MCP is connected, create the survey; otherwise, output the full survey spec (questions, flow, randomization) so I can create it later.
```

**You should see:** two matched loan descriptions (same facts, different tone), a
0–100 funding question, random assignment — and, if Qualtrics is connected, a new
survey in your account. This is how you'd turn a text finding into a causal claim.
