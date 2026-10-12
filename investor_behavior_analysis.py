
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_FILE = Path("data/raw/08_investor_transactions.csv")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE)
df["amount_inr"] = pd.to_numeric(df["amount_inr"], errors="raise")

# 1. Investor-level behavior summary
investor_summary = (
    df.groupby("investor_id")
    .agg(
        transaction_count=("amount_inr", "size"),
        total_transaction_amount_inr=("amount_inr", "sum"),
        average_transaction_amount_inr=("amount_inr", "mean"),
        unique_schemes=("amfi_code", "nunique"),
        transaction_types_used=("transaction_type", "nunique"),
        first_transaction_date=("transaction_date", "min"),
        last_transaction_date=("transaction_date", "max"),
    )
    .reset_index()
)

investor_summary["behavior_segment"] = investor_summary[
    "transaction_types_used"
].map({
    1: "Single transaction type",
    2: "Two transaction types",
    3: "All three transaction types",
}).fillna("Other")

investor_summary.to_csv(
    REPORT_DIR / "investor_behavior_summary.csv", index=False
)

print("\nINVESTOR BEHAVIOR SUMMARY")
print(
    investor_summary[
        [
            "transaction_count",
            "total_transaction_amount_inr",
            "average_transaction_amount_inr",
            "unique_schemes",
        ]
    ].describe().round(2).to_string()
)

# 2. Investor segment summary
segment_summary = (
    investor_summary.groupby("behavior_segment")
    .agg(
        investor_count=("investor_id", "nunique"),
        average_transactions=("transaction_count", "mean"),
        average_total_transaction_amount_inr=(
            "total_transaction_amount_inr", "mean"
        ),
    )
    .reset_index()
)

segment_summary["investor_percentage"] = (
    segment_summary["investor_count"]
    / investor_summary["investor_id"].nunique()
    * 100
).round(2)

segment_summary.to_csv(
    REPORT_DIR / "investor_behavior_segments.csv", index=False
)

print("\nINVESTOR BEHAVIOR SEGMENTS")
print(segment_summary.round(2).to_string(index=False))

# 3. Transaction frequency distribution
frequency = (
    investor_summary["transaction_count"]
    .value_counts()
    .sort_index()
    .rename_axis("transaction_count")
    .reset_index(name="investor_count")
)

frequency.to_csv(
    REPORT_DIR / "investor_transaction_frequency.csv", index=False
)

plt.figure(figsize=(10, 5))
plt.bar(frequency["transaction_count"], frequency["investor_count"])
plt.title("Investor Distribution by Transaction Frequency")
plt.xlabel("Number of Transactions")
plt.ylabel("Number of Investors")
plt.xticks(frequency["transaction_count"])
plt.tight_layout()
plt.savefig(
    REPORT_DIR / "investor_transaction_frequency.png", dpi=150
)
plt.close()

# 4. Investor behavior segments chart
plt.figure(figsize=(9, 5))
plt.bar(
    segment_summary["behavior_segment"],
    segment_summary["investor_count"],
)
plt.title("Investors by Transaction-Type Variety")
plt.xlabel("Transaction Types Used")
plt.ylabel("Number of Investors")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig(
    REPORT_DIR / "investor_behavior_segments.png", dpi=150
)
plt.close()

print("\nAnalysis completed. Reports and charts saved in reports/.")
