# Solution notes (for the instructor)

What a good faculty run should produce, so you can tell whether someone's setup is
working. Numbers are from the shipped `prosper_loans.csv` (seed 42, 25% test
split, numeric features scaled). **Treat them as ballpark** — exact values shift
with the split, scaling, and regularization a given run happens to use. The
*direction* and the *lift* are what's stable.

## EDA highlights (P1)

- Funded rate overall: **12.3%** (1,233 of 10,000).
- Funded listings have **higher credit** — mean `credit_score_lower` ≈ **662**
  (funded) vs **581** (expired).
- Funded listings are **longer** — median `num_words` ≈ **184** (funded) vs
  **146** (expired).
- Homeowners are funded more — **16.1%** vs **10.2%**.
- The theme flags barely separate the classes on their own (they're rare, ~1–22%
  prevalence). That's expected — the real language signal lives in the full
  vocabulary (P3), not six flags. A good teaching aside.

## The two models

| Model | Features | ROC-AUC | PR-AUC |
|---|---|---|---|
| Simple | structured financials only | **≈0.79–0.84** | ≈0.43–0.53 |
| Richer | + num_words, TF-IDF(500), themes | **≈0.85–0.88** | ≈0.51–0.59 |
| (text only) | TF-IDF of `description` alone | ≈0.73 | ≈0.33 |

**The headline:** adding language lifts ROC-AUC by **≈0.04–0.06**, and text *alone*
scores ~0.73 (well above 0.5). Language carries genuine funding signal.

Use PR-AUC alongside ROC-AUC because only ~12% are funded — accuracy is a trap
(predicting "never funded" scores 88% accuracy and is useless).

## The words (P3) — this is the payoff

- **Funded-leaning:** *prosper, balances, wedding, card, excellent, sold, term,
  includes, questions, 175, 24* — concrete, specific, financially literate.
- **Expired-leaning:** *need, chance, expenses, bad, working, catch, caused,
  payday, unable, 2006* — desperation and vagueness.

This reproduces the paper's thesis ("words that sweat") from a 3-second logistic
regression: how you ask predicts whether you get funded.

## Leakage check (P2)

A correct P2 run uses only pre-funding fields. If someone's AUC is ~0.99, they
(or Claude) pulled in a post-funding field — but those are already stripped from
the shared file, so this shouldn't happen. It's still worth naming the concept.

## What "working" looks like — setup smoke-test

- [ ] P0.1 Claude summarizes the folder → **file access works**
- [ ] P0.2 `/init` writes a `CLAUDE.md` → **memory works**
- [ ] P0.3 output style switches to Explanatory → **config works**
- [ ] P0.4 `/mcp` shows Qualtrics **connected** → **MCP works**
- [ ] P1 produces an `eda_report.html` that opens in a browser → **Python + plotting work**
- [ ] P2/P3 print AUCs in the ranges above → **modeling works**
- [ ] P4 drafts (or creates) a Qualtrics survey → **end-to-end works**

## Reproducing the reference numbers

The exact script used to generate these lives in the workshop scratchpad (not
shipped). Any faculty P2/P3 run following the prompts lands in the ranges above.
