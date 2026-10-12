
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load the original dataset
input_file = Path("data/raw/08_investor_transactions.csv")
df = pd.read_csv(input_file)

# Prepare dates
df["transaction_date"] = pd.to_datetime(df["transaction_date"])

output_dir = Path("reports")
output_dir.mkdir(parents=True, exist_ok=True)

print("INVESTOR TRANSACTION ANALYSIS")
print("-----------------------------")
print("Total transactions:", len(df))
print("Unique investors:", df["investor_id"].nunique())
print("Date range:",
      df["transaction_date"].min().date(),
      "to",
      df["transaction_date"].max().date())

# 1. Transaction type summary
type_summary = (
    df.groupby("transaction_type")
    .agg(
        transaction_count=("amount_inr", "size"),
        total_amount_inr=("amount_inr", "sum"),
        average_amount_inr=("amount_inr", "mean"),
        median_amount_inr=("amount_inr", "median")
    )
    .reset_index()
    .sort_values("total_amount_inr", ascending=False)
)

print("\nTRANSACTION TYPE SUMMARY")
print(type_summary.round(2).to_string(index=False))

type_summary.to_csv(
    output_dir / "transaction_type_summary.csv",
    index=False
)

# 2. Monthly transaction activity
df["month"] = df["transaction_date"].dt.to_period("M").astype(str)

monthly = (
    df.groupby("month")
    .agg(
        transaction_count=("amount_inr", "size"),
        total_amount_inr=("amount_inr", "sum")
    )
    .reset_index()
)

monthly.to_csv(
    output_dir / "monthly_transaction_summary.csv",
    index=False
)

# Plot monthly transaction count
plt.figure(figsize=(12, 6))
plt.plot(
    monthly["month"],
    monthly["transaction_count"],
    marker="o",
    markersize=3
)
plt.title("Monthly Investor Transaction Count")
plt.xlabel("Month")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=60)
plt.grid(True, alpha=0.3)
plt.tight_layout()

chart_path = output_dir / "monthly_transaction_count.png"
plt.savefig(chart_path, dpi=150)
plt.close()

# 3. Transaction type count chart
type_counts = df["transaction_type"].value_counts()

plt.figure(figsize=(9, 5))
plt.bar(type_counts.index, type_counts.values)
plt.title("Transactions by Type")
plt.xlabel("Transaction Type")
plt.ylabel("Number of Transactions")
plt.tight_layout()

type_chart_path = output_dir / "transactions_by_type.png"
plt.savefig(type_chart_path, dpi=150)
plt.close()

print("\nReports saved:")
print("- reports/transaction_type_summary.csv")
print("- reports/monthly_transaction_summary.csv")
print("- reports/monthly_transaction_count.png")
print("- reports/transactions_by_type.png")
