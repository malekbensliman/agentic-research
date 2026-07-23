#!/usr/bin/env python
"""Reduce a large 'When Words Sweat' Prosper source CSV to a small, shareable dataset.

The source files (240-355 MB) are unwieldy and carry ~140-170 columns of mixed,
mostly z-scored features. This script produces one ~10k-row, ~23-column file that
opens anywhere (Excel, pandas, the Claude Code desktop app) for the workshop
activity: predicting *funding success* from a loan request's language.

Design choices worth knowing:
  * We predict `granted` (funded vs expired), NOT default -- the shared files do
    not carry a usable default label.
  * We keep the *natural* ~12.3% funded rate (stratified sample) so the activity
    can teach why accuracy misleads under class imbalance.
  * We drop every post-funding field (rate, funded amount, yields, ...): using
    them would leak the target. See DATA_DICTIONARY.md.
  * `num_words` is re-derived from the raw text because the source `NumWords`
    column is standardized (mean 0, sd 1) and therefore unreadable.

Run:
    uv run --with pandas --with pyarrow python prepare_dataset.py \
        --source ../../prosper_archive_processed_with_compettion_2025_.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

# original source column -> friendly snake_case name in the shared file
COLUMN_MAP: dict[str, str] = {
    "Key": "key",
    "Date": "date",
    "Granted": "granted",
    "AmountRequested": "amount_requested",
    "CreditScoreRangeLower": "credit_score_lower",
    "CreditScoreRangeUpper": "credit_score_upper",
    "DebtToIncomeRatio": "debt_to_income",
    "IsBorrowerHomeowner": "is_homeowner",
    "Category": "category",
    "NumPriorListing": "prior_listings",
    "BorrowerState": "borrower_state",
    "Title": "title",
    "Description": "description",
    # psychological-dictionary theme scores (z-scored in the source; kept as-is).
    # NOTE the source misspelling 'Negative_emtion_liwc' is intentional here.
    "Concrete_liwc": "concrete",
    "Positive_emotion_liwc": "positive_emotion",
    "Negative_emtion_liwc": "negative_emotion",
    "Confidence & Commitment_liwc": "confidence_commitment",
    "Personal Struggles & Emotional Appeals_liwc": "personal_struggles",
    "Urgency & Momentum_liwc": "urgency_momentum",
}

# Final column order in the shared file (`funded` and `num_words` are derived).
FINAL_ORDER = [
    "key", "date", "granted", "funded",
    "amount_requested", "credit_score_lower", "credit_score_upper",
    "debt_to_income", "is_homeowner", "category",
    "prior_listings", "borrower_state",
    "title", "description", "num_words",
    "concrete", "positive_emotion", "negative_emotion",
    "confidence_commitment", "personal_struggles", "urgency_momentum",
]

# Columns dropped on purpose: LoanTermInMonths (constant 36 -> zero variance),
# TotalProsperLoans (~95% missing), BorrowerCity (privacy).
# Columns that remain STANDARDIZED in the source (z-scored, not raw units):
# amount_requested, debt_to_income, prior_listings. Documented in DATA_DICTIONARY.md.


def build(source: Path, n: int, seed: int) -> pd.DataFrame:
    df = pd.read_csv(source, usecols=list(COLUMN_MAP), low_memory=False)
    df = df.rename(columns=COLUMN_MAP)

    # Stratified sample that preserves the natural funded rate at exactly n rows.
    rate = df["granted"].mean()
    n_pos = round(n * rate)
    n_neg = n - n_pos
    pos = df[df["granted"] == 1].sample(n=n_pos, random_state=seed)
    neg = df[df["granted"] == 0].sample(n=n_neg, random_state=seed)
    out = (
        pd.concat([pos, neg])
        .sample(frac=1, random_state=seed)  # shuffle so classes interleave
        .reset_index(drop=True)
    )

    # Derived / cleaned columns.
    out["funded"] = out["granted"].map({1: "funded", 0: "expired"})
    out["num_words"] = out["description"].fillna("").str.split().str.len()
    out["date"] = out["date"].astype(str).str.slice(0, 10)  # YYYY-MM-DD only
    out["granted"] = out["granted"].astype(int)
    # is_homeowner is z-scored (two values) in the source; restore a clean 0/1.
    out["is_homeowner"] = (out["is_homeowner"] > 0).astype(int)

    return out[FINAL_ORDER]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", type=Path, required=True, help="large source CSV")
    ap.add_argument("--n", type=int, default=10_000, help="target row count")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out-dir", type=Path, default=Path(__file__).parent)
    args = ap.parse_args()

    out = build(args.source, args.n, args.seed)
    csv_path = args.out_dir / "prosper_loans.csv"
    pq_path = args.out_dir / "prosper_loans.parquet"
    out.to_csv(csv_path, index=False)
    out.to_parquet(pq_path, index=False)

    print(f"rows: {len(out)}")
    print(f"funded rate: {out['granted'].mean():.4f}")
    print(f"columns ({len(out.columns)}): {list(out.columns)}")
    print(f"wrote: {csv_path}  ({csv_path.stat().st_size/1e6:.1f} MB)")
    print(f"wrote: {pq_path}  ({pq_path.stat().st_size/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
