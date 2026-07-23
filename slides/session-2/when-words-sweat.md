---
module: When Words Sweat — language and loan funding
session: 2
order: 5
duration_min: 20
template: ../../templates/cbs-template.pptx
learning_goals:
  - Understand the dataset and the funding-prediction task
  - See how free text becomes features that measurably improve a model
  - Connect a correlational finding to a causal Qualtrics experiment
---

<!-- Companion to the hands-on activity in activities/when-words-sweat/.
     Slots alongside Session 2, Module 5 (Collaborative demo) / Module 7 (LLMs
     for unstructured data). Markdown is the source of truth; render to .pptx. -->

# Slide 1 — When Words Sweat
<!-- layout: Section Header -->

**On slide:**
- Does *how* you write a loan request change whether strangers fund it?
- A tangible marketing question, run end-to-end in Claude Code.

**Visual:** section header; faint background of a handwritten loan request.

**Notes:**
> The hands-on for this session. Everyone runs the same small dataset and a few
> prompts; by the end they've built two models and designed a survey — and proved
> their Claude Code setup works.

# Slide 2 — The data and the question
<!-- layout: Title and Content -->

**On slide:**
- Prosper.com peer-to-peer loans, 2007–2008: a borrower writes a request; strangers fund it or not.
- 10,000 real listings; **~12% funded**.
- Predict `granted` (funded vs expired) from the request — especially its **language**.
- From Netzer, Lemaire & Herzenstein, *"When Words Sweat"* (JMR 2019).

**Visual:** one real loan `description` with the funded/expired outcome tag.

**Notes:**
> The paper's headline is loan *default*; these listing files don't carry a usable
> default label, so we study *funding* — cleaner, and a purer persuasion question.
> Data shared by Alain Lemaire for teaching.

# Slide 3 — What's in each row
<!-- layout: Two Content -->

**On slide:**
- **The text:** `description` (the request), `title`, `num_words`.
- **The numbers:** credit-score band, amount, debt-to-income, homeowner, category.
- **Language themes:** concrete, positive/negative emotion, confidence, struggle, urgency.
- Caveat: some numeric fields are **z-scored** (not dollars); credit score and word count are raw.

**Visual:** two-column table — "Structured" vs "From the text".

**Notes:**
> Point out the leakage trap we removed: rate, funded amount, and yields only
> exist *after* funding — using them would be cheating. Good teaching moment.

# Slide 4 — The activity, in four moves
<!-- layout: Title and Content -->

**On slide:**
- **Setup** — open the folder, `/init`, output style, connect the Qualtrics MCP.
- **Explore** — Claude builds a browsable `eda_report.html`.
- **Two models** — funding from the numbers alone, then + the language.
- **Survey** — turn the finding into a Qualtrics experiment.

**Visual:** ../assets/ four-step arrow strip (setup → EDA → models → survey).

**Notes:**
> Act 1 is the smoke-test: if setup works, the analysis works. The "simple vs
> complex" jump is about *features*, not a heavier model — same fast learner,
> richer inputs.

# Slide 5 — The result you'll reproduce
<!-- layout: Comparison -->

**On slide:**
- **Numbers only:** ROC-AUC ≈ **0.79–0.84**.
- **+ Language:** ROC-AUC ≈ **0.85–0.88** — a real lift.
- Funded words: *balances, card, term, excellent, sold*.
- Expired words: *need, chance, payday, unable, bad*.

**Visual:** two-bar AUC chart + a "funded vs expired words" split list.

**Notes:**
> Language alone scores ~0.73 — well above chance. The word lists recover the
> paper's thesis: concrete, financially-literate asks get funded; desperate, vague
> ones expire. "Words that sweat," from a three-second logistic regression.

# Slide 6 — From correlation to causation
<!-- layout: Title and Content -->

**On slide:**
- The models show *association* — confident writers may also have better credit.
- To test the *wording* itself: an experiment.
- Two matched requests, same facts, different tone → measure willingness-to-fund.
- Claude drafts and creates it via the **Qualtrics MCP**.

**Visual:** A/B loan-description mock with a 0–100 "how likely to fund?" slider.

**Notes:**
> This closes the loop and motivates Session 2's Qualtrics MCP demo — not pulling
> survey data, but *creating* the instrument from a finding you just produced.
