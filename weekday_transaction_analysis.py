
import pandas as pd
import matplotlib.pyplot as plt

# Load transaction data
df = pd.read_csv("data/raw/08_investor_transactions.csv")
df["transaction_date"] = pd.to_datetime(df["transaction_date"])

# Extract weekday
df["weekday"] = df["transaction_date"].dt.day_name()

weekday_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

# Aggregate transactions by weekday
summary = (
    df.groupby("weekday")
    .agg(
        transaction_count=("transaction_type", "size"),
        total_amount_inr=("amount_inr", "sum"),
        average_amount_inr=("amount_inr", "mean")
    )
    .reindex(weekday_order)
    .reset_index()
)

summary["average_amount_inr"] = summary["average_amount_inr"].round(2)

print("WEEKDAY TRANSACTION ANALYSIS")
print("----------------------------")
print(summary.to_string(index=False))

# Save summary
summary.to_csv("reports/weekday_transaction_summary.csv", index=False)

# Plot transaction counts
plt.figure(figsize=(9, 5))
plt.bar(summary["weekday"], summary["transaction_count"])
plt.title("Transactions by Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("reports/weekday_transaction_count.png", dpi=150)
plt.close()

print("\nReports saved:")
print("- reports/weekday_transaction_summary.csv")
print("- reports/weekday_transaction_count.png")
