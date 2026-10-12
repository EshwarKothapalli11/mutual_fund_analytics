
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data/raw")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load data
transactions = pd.read_csv(DATA_DIR / "08_investor_transactions.csv")
funds = pd.read_csv(DATA_DIR / "01_fund_master.csv")

# Validate mapping
if funds["amfi_code"].duplicated().any():
    raise ValueError("Duplicate AMFI codes found in fund master.")

transactions["amount_inr"] = pd.to_numeric(
    transactions["amount_inr"], errors="raise"
)

df = transactions.merge(
    funds[["amfi_code", "fund_house"]],
    on="amfi_code",
    how="left",
    validate="many_to_one",
)

if df["fund_house"].isna().any():
    raise ValueError("Some transactions could not be mapped to a fund house.")

# Summarize transaction types by fund house
summary = (
    df.groupby(["fund_house", "transaction_type"])
    .agg(
        transaction_count=("amount_inr", "size"),
        total_amount_inr=("amount_inr", "sum"),
        average_amount_inr=("amount_inr", "mean"),
    )
    .reset_index()
)

summary["count_share_within_fund_house_pct"] = (
    summary["transaction_count"]
    / summary.groupby("fund_house")["transaction_count"].transform("sum")
    * 100
).round(2)

summary.to_csv(
    REPORT_DIR / "transaction_type_by_fund_house.csv",
    index=False,
)

print("\nTRANSACTION TYPE BY FUND HOUSE")
print(summary.round(2).to_string(index=False))

# Pivot tables for easier comparison
count_pivot = summary.pivot(
    index="fund_house",
    columns="transaction_type",
    values="transaction_count",
).fillna(0)

amount_pivot = summary.pivot(
    index="fund_house",
    columns="transaction_type",
    values="total_amount_inr",
).fillna(0)

count_pivot.to_csv(REPORT_DIR / "fund_house_transaction_type_counts.csv")
amount_pivot.to_csv(REPORT_DIR / "fund_house_transaction_type_amounts.csv")

# Chart: transaction counts by type and fund house
count_pivot.plot(kind="bar", figsize=(12, 6))
plt.title("Transaction Counts by Type and Fund House")
plt.xlabel("Fund House")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(REPORT_DIR / "transaction_type_counts_by_fund_house.png", dpi=150)
plt.close()

# Chart: transaction amounts by type and fund house
(amount_pivot / 10_000_000).plot(kind="bar", figsize=(12, 6))
plt.title("Transaction Amounts by Type and Fund House")
plt.xlabel("Fund House")
plt.ylabel("Total Transaction Amount (₹ crore)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(REPORT_DIR / "transaction_type_amounts_by_fund_house.png", dpi=150)
plt.close()

print("\nTOP FUND HOUSE FOR EACH TRANSACTION TYPE")
for transaction_type in summary["transaction_type"].unique():
    subset = summary[summary["transaction_type"] == transaction_type]
    top = subset.loc[subset["transaction_count"].idxmax()]
    print(
        f"{transaction_type}: {top['fund_house']} "
        f"({int(top['transaction_count'])} transactions)"
    )

print("\nAnalysis completed. Reports and charts saved in reports/.")
