# Data dictionary — `prosper_loans.csv` / `.parquet`

10,000 Prosper.com loan **listings** (2007–2008), one row per listing. The task
is to predict **funding success** — did enough lenders fund the request before it
expired? — from the listing's financials and, above all, its **language**.

- Rows: 10,000 (a stratified sample; the natural **12.3%** funded rate is preserved)
- One row = one loan listing
- Target: `granted` (`funded` is its human-readable label)

## Columns

| Column | Type | Units | Meaning |
|---|---|---|---|
| `key` | text | — | Listing identifier (opaque). |
| `date` | text | `YYYY-MM-DD` | Listing creation date (2007-04 to 2008-10). |
| **`granted`** | int | 0 / 1 | **Target.** 1 = the listing was funded; 0 = it expired unfunded. |
| `funded` | text | `funded`/`expired` | Human-readable label of `granted`. |
| `amount_requested` | float | **standardized** | Loan amount requested. Z-scored in the source (mean 0, sd 1) — *not* dollars. Higher = larger-than-average ask. |
| `credit_score_lower` | float | **raw** | Lower bound of the borrower's credit-score band (≈520–860). |
| `credit_score_upper` | float | **raw** | Upper bound of the credit-score band. |
| `debt_to_income` | float | **standardized** | Debt-to-income ratio, z-scored. Higher = more leveraged than average. |
| `is_homeowner` | int | 0 / 1 | 1 = borrower owns a home. |
| `category` | int | 0–7 | Prosper loan-purpose category **code**. Treat as categorical; exact label map is not shipped with the processed data. |
| `prior_listings` | float | **standardized** | Count of the borrower's prior listings, z-scored. |
| `borrower_state` | text | — | US state abbreviation (e.g. `CA`, `TX`). |
| `title` | text | — | Short listing title. |
| **`description`** | text | — | The free-text loan request — the object of study. |
| `num_words` | int | **raw** | Word count of `description` (re-derived here; the source `NumWords` was z-scored). |
| `concrete` | int | 0 / 1 | 1 = description flagged for **concrete** (vs abstract) language. |
| `positive_emotion` | int | 0 / 1 | 1 = description flagged for positive emotional language. |
| `negative_emotion` | int | 0 / 1 | 1 = description flagged for negative emotional language. |
| `confidence_commitment` | int | 0 / 1 | 1 = confident, committed tone (estimated dictionary theme). |
| `personal_struggles` | int | 0 / 1 | 1 = personal hardship / emotional appeal (estimated theme). |
| `urgency_momentum` | int | 0 / 1 | 1 = urgency / momentum language (estimated theme). |

### A note on "standardized" columns
Several numeric features (`amount_requested`, `debt_to_income`, `prior_listings`)
were **z-scored** by the paper's authors, so they are unitless (centered at 0) and
you **cannot** read them as dollars or percentages. The genuinely interpretable
numeric fields are `credit_score_lower/upper` and `num_words`. The six `theme`
columns are **binary flags** (0/1), not intensities.

## Deliberately omitted — these would leak the target
A listing's *outcome* fields only exist **after** it is funded, so including them
would let a model "predict" funding by peeking at the answer. They are **not** in
this file on purpose (a teaching point in the activity):

`BorrowerRate`, `LenderYield`, `EffectiveYield`, `EstimatedReturn`,
`EstimatedLoss`, `AmountFunded`, `PercentFunded`, `MonthlyLoanPayment`, `Status`,
and all `Prosper*` repayment fields.

We also dropped `LoanTermInMonths` (constant, 36), `TotalProsperLoans` (~95%
missing), and `BorrowerCity` (privacy).

## Provenance & credit
Data behind **Netzer, Lemaire & Herzenstein, "When Words Sweat: Identifying
Signals for Loan Default in the Text of Loan Applications," _Journal of Marketing
Research_ (2019).** Underlying records are public Prosper.com listings (2007–2008).
Shared by **Alain Lemaire** for teaching; reduced to this 10k sample for the CBS
"Agentic Research" workshop. Please keep the credit line if you reuse it.

> Note: the paper studies loan **default**; these listing files do not carry a
> usable default label, so this activity studies **funding success** instead —
> a cleaner, and arguably more marketing-native (persuasion), question.
