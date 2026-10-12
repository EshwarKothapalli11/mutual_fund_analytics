
import pandas as pd
import matplotlib.pyplot as plt

# Load transaction data
df = pd.read_csv("data/raw/08_investor_transactions.csv")

# Keep SIP transactions only
sip = df[
    df["transaction_type"].str.strip().str.upper() == "SIP"
].copy()

# Aggregate by age group
summary = sip.groupby("age_group").agg(
    sip_transaction_count=("transaction_type", "size"),
    unique_investors=("investor_id", "nunique"),
    total_sip_amount_inr=("amount_inr", "sum"),
    average_sip_amount_inr=("amount_inr", "mean")
).reset_index()

summary["average_sip_amount_inr"] = (
    summary["average_sip_amount_inr"].round(2)
)

summary = summary.sort_values("total_sip_amount_inr", ascending=False)

print("SIP ANALYSIS BY AGE GROUP")
print("-------------------------")
print(summary.to_string(index=False))

# Save aggregate report
summary.to_csv("reports/sip_age_group_summary.csv", index=False)

# Plot transaction counts
plt.figure(figsize=(9, 5))
plt.bar(
    summary["age_group"].astype(str),
    summary["sip_transaction_count"]
)
plt.title("SIP Transactions by Investor Age Group")
plt.xlabel("Age Group")
plt.ylabel("Number of SIP Transactions")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("reports/sip_age_group_transactions.png", dpi=150)
plt.close()

print("\nReports saved:")
print("- reports/sip_age_group_summary.csv")
print("- reports/sip_age_group_transactions.png")
