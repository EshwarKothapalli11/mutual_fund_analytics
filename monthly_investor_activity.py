
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_FILE = Path("data/raw/08_investor_transactions.csv")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load and validate data
df = pd.read_csv(DATA_FILE, parse_dates=["transaction_date"])

required = {
    "transaction_date",
    "transaction_type",
    "amount_inr",
    "investor_id",
}
missing = required - set(df.columns)

if missing:
    raise ValueError(f"Missing required columns: {missing}")

if df["transaction_date"].isna().any():
    raise ValueError("Missing or invalid transaction dates found.")

df["amount_inr"] = pd.to_numeric(df["amount_inr"], errors="raise")
df["month"] = df["transaction_date"].dt.to_period("M").astype(str)

# 1. Overall monthly activity
monthly = (
    df.groupby("month")
    .agg(
        transaction_count=("amount_inr", "size"),
        total_amount_inr=("amount_inr", "sum"),
        average_amount_inr=("amount_inr", "mean"),
        unique_investors=("investor_id", "nunique"),
    )
    .reset_index()
)

monthly["transaction_percentage"] = (
    monthly["transaction_count"] / len(df) * 100
).round(2)

monthly.to_csv(
    REPORT_DIR / "monthly_investor_activity_summary.csv",
    index=False,
)

print("\nMONTHLY INVESTOR ACTIVITY")
print(monthly.round(2).to_string(index=False))

# 2. Monthly activity by transaction type
monthly_type = (
    df.groupby(["month", "transaction_type"])
    .agg(
        transaction_count=("amount_inr", "size"),
        total_amount_inr=("amount_inr", "sum"),
    )
    .reset_index()
)

monthly_type.to_csv(
    REPORT_DIR / "monthly_activity_by_transaction_type.csv",
    index=False,
)

# 3. Monthly transaction count chart
plt.figure(figsize=(12, 5))
plt.plot(
    monthly["month"],
    monthly["transaction_count"],
    marker="o",
)
plt.title("Monthly Transaction Count")
plt.xlabel("Month")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=60, ha="right")
plt.tight_layout()
plt.savefig(
    REPORT_DIR / "monthly_transaction_trend.png",
    dpi=150,
)
plt.close()

# 4. Monthly transaction amount chart
plt.figure(figsize=(12, 5))
plt.plot(
    monthly["month"],
    monthly["total_amount_inr"] / 10_000_000,
    marker="o",
)
plt.title("Monthly Transaction Amount")
plt.xlabel("Month")
plt.ylabel("Transaction Amount (₹ crore)")
plt.xticks(rotation=60, ha="right")
plt.tight_layout()
plt.savefig(
    REPORT_DIR / "monthly_transaction_amount_trend.png",
    dpi=150,
)
plt.close()

# 5. SIP, lumpsum, and redemption count trends
count_pivot = monthly_type.pivot(
    index="month",
    columns="transaction_type",
    values="transaction_count",
).fillna(0)

count_pivot.plot(figsize=(12, 5), marker="o")
plt.title("Monthly Transactions by Transaction Type")
plt.xlabel("Month")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=60, ha="right")
plt.tight_layout()
plt.savefig(
    REPORT_DIR / "monthly_transaction_type_trend.png",
    dpi=150,
)
plt.close()

# 6. Identify peak and lowest months
peak_count = monthly.loc[monthly["transaction_count"].idxmax()]
lowest_count = monthly.loc[monthly["transaction_count"].idxmin()]
peak_amount = monthly.loc[monthly["total_amount_inr"].idxmax()]

print("\nKEY FINDINGS")
print(
    f"Highest transaction count: {peak_count['month']} "
    f"({int(peak_count['transaction_count'])} transactions)"
)
print(
    f"Lowest transaction count: {lowest_count['month']} "
    f"({int(lowest_count['transaction_count'])} transactions)"
)
print(
    f"Highest transaction amount: {peak_amount['month']} "
    f"(₹{peak_amount['total_amount_inr'] / 10_000_000:.2f} crore)"
)

print("\nAnalysis completed. Reports and charts saved in reports/.")
