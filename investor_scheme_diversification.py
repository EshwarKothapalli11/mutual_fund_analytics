
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_FILE = Path("data/raw/08_investor_transactions.csv")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE)

required = {"investor_id", "amfi_code", "amount_inr", "transaction_type"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {missing}")

df["amount_inr"] = pd.to_numeric(df["amount_inr"], errors="raise")

# 1. Calculate unique schemes and activity per investor
investor_summary = (
    df.groupby("investor_id")
    .agg(
        unique_schemes=("amfi_code", "nunique"),
        transaction_count=("amfi_code", "size"),
        total_transaction_amount_inr=("amount_inr", "sum"),
    )
    .reset_index()
)

# Assign descriptive scheme-count segments
investor_summary["scheme_segment"] = pd.cut(
    investor_summary["unique_schemes"],
    bins=[0, 1, 3, 6, 9, float("inf")],
    labels=[
        "1 scheme",
        "2-3 schemes",
        "4-6 schemes",
        "7-9 schemes",
        "10+ schemes",
    ],
)

# 2. Aggregate segment summary only
segment_summary = (
    investor_summary.groupby("scheme_segment", observed=False)
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
    REPORT_DIR / "investor_scheme_segments.csv", index=False
)

print("\nINVESTOR SCHEME SEGMENTS")
print(segment_summary.round(2).to_string(index=False))

# 3. Distribution by number of unique schemes
distribution = (
    investor_summary["unique_schemes"]
    .value_counts()
    .sort_index()
    .rename_axis("unique_schemes")
    .reset_index(name="investor_count")
)

distribution["investor_percentage"] = (
    distribution["investor_count"]
    / investor_summary["investor_id"].nunique()
    * 100
).round(2)

distribution.to_csv(
    REPORT_DIR / "investor_scheme_count_distribution.csv", index=False
)

print("\nINVESTORS BY NUMBER OF UNIQUE SCHEMES")
print(distribution.to_string(index=False))

# 4. Chart: investor distribution
plt.figure(figsize=(10, 5))
plt.bar(
    distribution["unique_schemes"],
    distribution["investor_count"],
)
plt.title("Investor Distribution by Number of Unique Schemes")
plt.xlabel("Unique Schemes in Transaction Records")
plt.ylabel("Number of Investors")
plt.xticks(distribution["unique_schemes"])
plt.tight_layout()
plt.savefig(
    REPORT_DIR / "investor_scheme_count_distribution.png", dpi=150
)
plt.close()

# 5. Chart: scheme segments
plt.figure(figsize=(10, 5))
plt.bar(
    segment_summary["scheme_segment"].astype(str),
    segment_summary["investor_count"],
)
plt.title("Investors by Scheme-Count Segment")
plt.xlabel("Unique Scheme Segment")
plt.ylabel("Number of Investors")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig(
    REPORT_DIR / "investor_scheme_segments.png", dpi=150
)
plt.close()

print("\nAnalysis completed. Aggregate reports and charts saved in reports/.")
