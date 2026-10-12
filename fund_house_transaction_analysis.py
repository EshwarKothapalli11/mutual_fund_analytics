
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data/raw")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load data
transactions = pd.read_csv(DATA_DIR / "08_investor_transactions.csv")
funds = pd.read_csv(DATA_DIR / "01_fund_master.csv")

# Validate required columns
if "amfi_code" not in transactions.columns or "amount_inr" not in transactions.columns:
    raise ValueError("Required transaction columns are missing.")

if "investor_id" not in transactions.columns:
    raise ValueError("investor_id column is missing.")

if funds["amfi_code"].duplicated().any():
    raise ValueError("Duplicate AMFI codes found in fund master.")

transactions["amount_inr"] = pd.to_numeric(
    transactions["amount_inr"], errors="raise"
)

# Map each transaction to its fund house
df = transactions.merge(
    funds[["amfi_code", "fund_house"]],
    on="amfi_code",
    how="left",
    validate="many_to_one",
)

if df["fund_house"].isna().any():
    raise ValueError("Some transactions could not be mapped to a fund house.")

# 1. Overall fund house summary
summary = (
    df.groupby("fund_house")
    .agg(
        transaction_count=("amount_inr", "size"),
        total_amount_inr=("amount_inr", "sum"),
        average_amount_inr=("amount_inr", "mean"),
        unique_investors=("investor_id", "nunique"),
        schemes=("amfi_code", "nunique"),
    )
    .reset_index()
    .sort_values("transaction_count", ascending=False)
)

summary["transaction_percentage"] = (
    summary["transaction_count"] / len(df) * 100
).round(2)

summary.to_csv(
    REPORT_DIR / "fund_house_transaction_summary.csv",
    index=False,
)

print("\nFUND HOUSE TRANSACTION SUMMARY")
print(summary.round(2).to_string(index=False))

# 2. Transaction type by fund house
type_summary = (
    df.groupby(["fund_house", "transaction_type"])
    .agg(
        transaction_count=("amount_inr", "size"),
        total_amount_inr=("amount_inr", "sum"),
    )
    .reset_index()
)

type_summary.to_csv(
    REPORT_DIR / "fund_house_transaction_type_summary.csv",
    index=False,
)

# 3. Chart: transaction counts
count_data = summary.sort_values("transaction_count")

plt.figure(figsize=(10, 6))
plt.barh(count_data["fund_house"], count_data["transaction_count"])
plt.title("Transactions by Fund House")
plt.xlabel("Number of Transactions")
plt.ylabel("Fund House")
plt.tight_layout()
plt.savefig(
    REPORT_DIR / "fund_house_transaction_counts.png",
    dpi=150,
)
plt.close()

# 4. Chart: total transaction amount
amount_data = summary.sort_values("total_amount_inr")

plt.figure(figsize=(10, 6))
plt.barh(
    amount_data["fund_house"],
    amount_data["total_amount_inr"] / 10_000_000,
)
plt.title("Total Transaction Amount by Fund House")
plt.xlabel("Total Transaction Amount (₹ crore)")
plt.ylabel("Fund House")
plt.tight_layout()
plt.savefig(
    REPORT_DIR / "fund_house_transaction_amounts.png",
    dpi=150,
)
plt.close()

# 5. Transaction type count comparison
type_pivot = type_summary.pivot(
    index="fund_house",
    columns="transaction_type",
    values="transaction_count",
).fillna(0)

type_pivot.to_csv(
    REPORT_DIR / "fund_house_transaction_type_pivot.csv"
)

print("\nTOP 3 FUND HOUSES BY TOTAL TRANSACTION AMOUNT")
print(
    summary.nlargest(3, "total_amount_inr")[
        ["fund_house", "transaction_count", "total_amount_inr",
         "unique_investors", "schemes"]
    ].round(2).to_string(index=False)
)

print("\nAnalysis completed. Reports and charts saved in reports/.")
