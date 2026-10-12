
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# File paths
DATA_FILE = Path("data/raw/08_investor_transactions.csv")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load data
df = pd.read_csv(DATA_FILE)

# Validate required columns
required_columns = {"payment_mode", "kyc_status", "amount_inr"}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

# Convert transaction amount to numeric
df["amount_inr"] = pd.to_numeric(df["amount_inr"], errors="raise")

# 1. Payment mode analysis
payment_summary = (
    df.groupby("payment_mode")
    .agg(
        transaction_count=("amount_inr", "size"),
        total_amount_inr=("amount_inr", "sum"),
        average_amount_inr=("amount_inr", "mean"),
        median_amount_inr=("amount_inr", "median"),
    )
    .reset_index()
)

payment_summary["transaction_percentage"] = (
    payment_summary["transaction_count"] / len(df) * 100
).round(2)

payment_summary.to_csv(
    REPORT_DIR / "payment_mode_summary.csv", index=False
)

print("\nPAYMENT MODE ANALYSIS")
print(payment_summary.round(2).to_string(index=False))

# 2. KYC status analysis
kyc_summary = (
    df.groupby("kyc_status")
    .agg(
        transaction_count=("amount_inr", "size"),
        total_amount_inr=("amount_inr", "sum"),
        average_amount_inr=("amount_inr", "mean"),
    )
    .reset_index()
)

kyc_summary["transaction_percentage"] = (
    kyc_summary["transaction_count"] / len(df) * 100
).round(2)

kyc_summary.to_csv(
    REPORT_DIR / "kyc_status_summary.csv", index=False
)

print("\nKYC STATUS ANALYSIS")
print(kyc_summary.round(2).to_string(index=False))

# 3. Payment mode chart
plt.figure(figsize=(9, 5))
plt.bar(
    payment_summary["payment_mode"],
    payment_summary["transaction_count"]
)
plt.title("Transaction Count by Payment Mode")
plt.xlabel("Payment Mode")
plt.ylabel("Number of Transactions")
plt.tight_layout()
plt.savefig(REPORT_DIR / "transactions_by_payment_mode.png", dpi=150)
plt.close()

# 4. KYC status chart
plt.figure(figsize=(7, 5))
plt.bar(
    kyc_summary["kyc_status"],
    kyc_summary["transaction_count"]
)
plt.title("Transaction Count by KYC Status")
plt.xlabel("KYC Status")
plt.ylabel("Number of Transactions")
plt.tight_layout()
plt.savefig(REPORT_DIR / "transactions_by_kyc_status.png", dpi=150)
plt.close()

# 5. Cross-analysis: payment mode vs KYC status
cross_summary = pd.crosstab(
    df["payment_mode"],
    df["kyc_status"],
    margins=False
)

cross_summary.to_csv(REPORT_DIR / "payment_mode_by_kyc_status.csv")

print("\nPAYMENT MODE vs KYC STATUS")
print(cross_summary.to_string())

print("\nAnalysis completed. Reports and charts saved in the reports folder.")
