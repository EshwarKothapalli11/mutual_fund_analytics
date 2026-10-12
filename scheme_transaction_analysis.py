
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data/raw")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load datasets
transactions = pd.read_csv(DATA_DIR / "08_investor_transactions.csv")
funds = pd.read_csv(DATA_DIR / "01_fund_master.csv")

# Validate required columns
transaction_columns = {
    "amfi_code", "investor_id", "transaction_type", "amount_inr"
}
fund_columns = {"amfi_code", "scheme_name", "fund_house", "category", "sub_category"}

if not transaction_columns.issubset(transactions.columns):
    raise ValueError("Required transaction columns are missing.")

if not fund_columns.issubset(funds.columns):
    raise ValueError("Required fund master columns are missing.")

# Check for duplicate scheme codes before merging
if funds["amfi_code"].duplicated().any():
    raise ValueError("Duplicate AMFI codes found in fund master.")

transactions["amount_inr"] = pd.to_numeric(
    transactions["amount_inr"], errors="raise"
)

# Merge transaction data with scheme information
df = transactions.merge(
    funds[
        ["amfi_code", "scheme_name", "fund_house", "category", "sub_category"]
    ],
    on="amfi_code",
    how="left",
    validate="many_to_one",
    indicator=True,
)

if (df["_merge"] != "both").any():
    raise ValueError("Some transactions could not be mapped to a scheme.")

df = df.drop(columns="_merge")

# 1. Scheme-level summary
scheme_summary = (
    df.groupby(
        ["amfi_code", "scheme_name", "fund_house", "category", "sub_category"],
        as_index=False,
    )
    .agg(
        transaction_count=("amount_inr", "size"),
        total_amount_inr=("amount_inr", "sum"),
        average_amount_inr=("amount_inr", "mean"),
        unique_investors=("investor_id", "nunique"),
    )
    .sort_values("transaction_count", ascending=False)
)

scheme_summary["transaction_percentage"] = (
    scheme_summary["transaction_count"] / len(df) * 100
).round(2)

scheme_summary.to_csv(
    REPORT_DIR / "scheme_transaction_summary.csv", index=False
)

print("\nTOP 10 SCHEMES BY TRANSACTION COUNT")
print(
    scheme_summary.head(10)[
        ["scheme_name", "transaction_count", "total_amount_inr",
         "unique_investors", "transaction_percentage"]
    ].round(2).to_string(index=False)
)

# 2. Top 10 schemes by total transaction amount
top_amount = scheme_summary.nlargest(10, "total_amount_inr")

print("\nTOP 10 SCHEMES BY TOTAL TRANSACTION AMOUNT")
print(
    top_amount[
        ["scheme_name", "transaction_count", "total_amount_inr",
         "unique_investors"]
    ].round(2).to_string(index=False)
)

top_amount.to_csv(
    REPORT_DIR / "top_10_schemes_by_amount.csv", index=False
)

# 3. Chart: transaction counts
top_count = scheme_summary.head(10).sort_values("transaction_count")

plt.figure(figsize=(12, 7))
plt.barh(top_count["scheme_name"], top_count["transaction_count"])
plt.title("Top 10 Schemes by Transaction Count")
plt.xlabel("Number of Transactions")
plt.ylabel("Scheme")
plt.tight_layout()
plt.savefig(
    REPORT_DIR / "top_10_schemes_by_transaction_count.png", dpi=150
)
plt.close()

# 4. Chart: transaction amounts
chart_data = top_amount.sort_values("total_amount_inr")

plt.figure(figsize=(12, 7))
plt.barh(
    chart_data["scheme_name"],
    chart_data["total_amount_inr"] / 10_000_000,
)
plt.title("Top 10 Schemes by Transaction Amount")
plt.xlabel("Total Transaction Amount (₹ crore)")
plt.ylabel("Scheme")
plt.tight_layout()
plt.savefig(
    REPORT_DIR / "top_10_schemes_by_transaction_amount.png", dpi=150
)
plt.close()

# 5. Transaction type breakdown by scheme
type_summary = (
    df.groupby(["scheme_name", "transaction_type"])
    .agg(
        transaction_count=("amount_inr", "size"),
        total_amount_inr=("amount_inr", "sum"),
    )
    .reset_index()
)

type_summary.to_csv(
    REPORT_DIR / "scheme_transaction_type_summary.csv", index=False
)

print("\nSCHEME-LEVEL ANALYSIS COMPLETED")
print(f"Transactions analyzed: {len(df):,}")
print(f"Unique schemes analyzed: {df['amfi_code'].nunique()}")
print("Reports and charts saved in the reports folder.")
