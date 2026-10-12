
import pandas as pd
import matplotlib.pyplot as plt

# Load transactions and fund master
transactions = pd.read_csv("data/raw/08_investor_transactions.csv")
funds = pd.read_csv("data/raw/01_fund_master.csv")

# Keep SIP transactions only
sip = transactions[
    transactions["transaction_type"].str.strip().str.upper() == "SIP"
].copy()

# Join scheme information to identify fund houses
merged = sip.merge(
    funds[["amfi_code", "fund_house"]],
    on="amfi_code",
    how="left"
)

# Aggregate SIP activity by fund house
summary = merged.groupby("fund_house").agg(
    sip_transaction_count=("transaction_type", "size"),
    unique_investors=("investor_id", "nunique"),
    total_sip_amount_inr=("amount_inr", "sum"),
    average_sip_amount_inr=("amount_inr", "mean")
).reset_index()

summary["average_sip_amount_inr"] = (
    summary["average_sip_amount_inr"].round(2)
)

summary = summary.sort_values(
    "total_sip_amount_inr", ascending=False
)

print("FUND HOUSE SIP ANALYSIS")
print("-----------------------")
print(summary.to_string(index=False))

# Save aggregate report
summary.to_csv("reports/fund_house_sip_summary.csv", index=False)

# Plot total SIP amount by fund house
plt.figure(figsize=(11, 6))
plt.barh(
    summary["fund_house"],
    summary["total_sip_amount_inr"] / 1e7
)
plt.title("Total SIP Transaction Amount by Fund House")
plt.xlabel("Total SIP Amount (₹ crore)")
plt.ylabel("Fund House")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("reports/fund_house_sip_amount.png", dpi=150)
plt.close()

print("\nReports saved:")
print("- reports/fund_house_sip_summary.csv")
print("- reports/fund_house_sip_amount.png")
