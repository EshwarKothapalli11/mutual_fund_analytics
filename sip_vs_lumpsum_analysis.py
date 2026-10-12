
import pandas as pd
import matplotlib.pyplot as plt

# Load transaction data
df = pd.read_csv("data/raw/08_investor_transactions.csv")
df["transaction_date"] = pd.to_datetime(df["transaction_date"])

# Compare SIP and Lumpsum only
df = df[df["transaction_type"].isin(["SIP", "Lumpsum"])].copy()

# Summary by transaction type
summary = df.groupby("transaction_type").agg(
    transaction_count=("transaction_type", "size"),
    unique_investors=("investor_id", "nunique"),
    total_amount_inr=("amount_inr", "sum"),
    average_amount_inr=("amount_inr", "mean"),
    median_amount_inr=("amount_inr", "median")
).reset_index()

summary["average_amount_inr"] = summary["average_amount_inr"].round(2)
summary["median_amount_inr"] = summary["median_amount_inr"].round(2)

print("SIP VS LUMPSUM ANALYSIS")
print("----------------------")
print(summary.to_string(index=False))

# Average transactions per investor
frequency = df.groupby("transaction_type").agg(
    total_transactions=("transaction_type", "size"),
    unique_investors=("investor_id", "nunique")
).reset_index()

frequency["transactions_per_investor"] = (
    frequency["total_transactions"] / frequency["unique_investors"]
).round(2)

print("\nTRANSACTIONS PER INVESTOR")
print(frequency.to_string(index=False))

# Save aggregate reports
summary.to_csv("reports/sip_vs_lumpsum_summary.csv", index=False)
frequency.to_csv("reports/sip_vs_lumpsum_frequency.csv", index=False)

# Plot total transaction amounts
plt.figure(figsize=(8, 5))
plt.bar(summary["transaction_type"], summary["total_amount_inr"] / 1e7)
plt.title("Total Transaction Amount: SIP vs Lumpsum")
plt.xlabel("Transaction Type")
plt.ylabel("Total Amount (₹ crore)")
plt.tight_layout()
plt.savefig("reports/sip_vs_lumpsum_amount.png", dpi=150)
plt.close()

print("\nReports saved:")
print("- reports/sip_vs_lumpsum_summary.csv")
print("- reports/sip_vs_lumpsum_frequency.csv")
print("- reports/sip_vs_lumpsum_amount.png")
