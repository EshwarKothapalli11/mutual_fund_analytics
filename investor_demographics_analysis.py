
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load transaction data
df = pd.read_csv("data/raw/08_investor_transactions.csv")

output_dir = Path("reports")
output_dir.mkdir(parents=True, exist_ok=True)

# Aggregate by age group
age_summary = (
    df.groupby("age_group")
    .agg(
        transaction_count=("amount_inr", "size"),
        total_amount_inr=("amount_inr", "sum"),
        average_amount_inr=("amount_inr", "mean")
    )
    .reset_index()
    .sort_values("total_amount_inr", ascending=False)
)

print("TRANSACTION ACTIVITY BY AGE GROUP")
print(age_summary.round(2).to_string(index=False))

age_summary.to_csv(
    output_dir / "transactions_by_age_group.csv",
    index=False
)

# Aggregate by city tier
city_summary = (
    df.groupby("city_tier")
    .agg(
        transaction_count=("amount_inr", "size"),
        total_amount_inr=("amount_inr", "sum"),
        average_amount_inr=("amount_inr", "mean")
    )
    .reset_index()
    .sort_values("total_amount_inr", ascending=False)
)

print("\nTRANSACTION ACTIVITY BY CITY TIER")
print(city_summary.round(2).to_string(index=False))

city_summary.to_csv(
    output_dir / "transactions_by_city_tier.csv",
    index=False
)

# Plot transaction counts by age group
plt.figure(figsize=(9, 5))
plt.bar(age_summary["age_group"], age_summary["transaction_count"])
plt.title("Transactions by Investor Age Group")
plt.xlabel("Age Group")
plt.ylabel("Number of Transactions")
plt.tight_layout()

age_chart = output_dir / "transactions_by_age_group.png"
plt.savefig(age_chart, dpi=150)
plt.close()

# Plot transaction counts by city tier
plt.figure(figsize=(8, 5))
plt.bar(city_summary["city_tier"], city_summary["transaction_count"])
plt.title("Transactions by City Tier")
plt.xlabel("City Tier")
plt.ylabel("Number of Transactions")
plt.tight_layout()

city_chart = output_dir / "transactions_by_city_tier.png"
plt.savefig(city_chart, dpi=150)
plt.close()

print("\nReports and charts saved in:", output_dir)
