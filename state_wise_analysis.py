
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_FILE = Path("data/raw/08_investor_transactions.csv")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load transaction data
df = pd.read_csv(DATA_FILE)

required_columns = {"state", "amount_inr", "transaction_type"}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

if df["state"].isna().any():
    raise ValueError("State column contains missing values.")

df["amount_inr"] = pd.to_numeric(df["amount_inr"], errors="raise")

# State-wise summary
state_summary = (
    df.groupby("state")
    .agg(
        transaction_count=("amount_inr", "size"),
        total_amount_inr=("amount_inr", "sum"),
        average_amount_inr=("amount_inr", "mean"),
        unique_investors=("investor_id", "nunique"),
    )
    .reset_index()
    .sort_values("transaction_count", ascending=False)
)

state_summary["transaction_percentage"] = (
    state_summary["transaction_count"] / len(df) * 100
).round(2)

state_summary.to_csv(
    REPORT_DIR / "state_wise_transaction_summary.csv", index=False
)

print("\nSTATE-WISE TRANSACTION SUMMARY")
print(state_summary.round(2).to_string(index=False))

# Top 10 states by transaction count
top_states = state_summary.head(10).sort_values("transaction_count")

plt.figure(figsize=(10, 6))
plt.barh(top_states["state"], top_states["transaction_count"])
plt.title("Top 10 States by Transaction Count")
plt.xlabel("Number of Transactions")
plt.ylabel("State")
plt.tight_layout()
plt.savefig(REPORT_DIR / "top_10_states_by_transactions.png", dpi=150)
plt.close()

# Top 10 states by transaction amount
top_amount_states = (
    state_summary.nlargest(10, "total_amount_inr")
    .sort_values("total_amount_inr")
)

plt.figure(figsize=(10, 6))
plt.barh(
    top_amount_states["state"],
    top_amount_states["total_amount_inr"] / 10_000_000,
)
plt.title("Top 10 States by Transaction Amount")
plt.xlabel("Total Transaction Amount (₹ crore)")
plt.ylabel("State")
plt.tight_layout()
plt.savefig(REPORT_DIR / "top_10_states_by_amount.png", dpi=150)
plt.close()

# Transaction type breakdown by state
state_type_summary = (
    df.groupby(["state", "transaction_type"])
    .agg(
        transaction_count=("amount_inr", "size"),
        total_amount_inr=("amount_inr", "sum"),
    )
    .reset_index()
)

state_type_summary.to_csv(
    REPORT_DIR / "state_transaction_type_summary.csv", index=False
)

print("\nTOP 5 STATES BY TRANSACTION AMOUNT")
print(
    state_summary.nlargest(5, "total_amount_inr")[
        ["state", "transaction_count", "total_amount_inr", "unique_investors"]
    ].round(2).to_string(index=False)
)

print("\nAnalysis completed. Reports and charts saved in the reports folder.")
