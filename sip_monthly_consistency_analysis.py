
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned SIP data
df = pd.read_csv("data/processed/04_monthly_sip_inflows_cleaned.csv")
df["month"] = pd.to_datetime(df["month"])
df = df.sort_values("month").reset_index(drop=True)

# Calculate month-over-month change
df["mom_change_crore"] = df["sip_inflow_crore"].diff()
df["mom_growth_pct"] = df["sip_inflow_crore"].pct_change() * 100

# Display key findings
valid = df.dropna(subset=["mom_growth_pct"])

largest_increase = valid.loc[valid["mom_change_crore"].idxmax()]
largest_decrease = valid.loc[valid["mom_change_crore"].idxmin()]

print("MONTHLY SIP CONSISTENCY ANALYSIS")
print("--------------------------------")
print(f"Months analyzed: {len(df)}")
print(f"Average monthly SIP inflow: ₹{df['sip_inflow_crore'].mean():.2f} crore")
print(f"Highest SIP inflow: ₹{df['sip_inflow_crore'].max():.2f} crore")
print(f"Lowest SIP inflow: ₹{df['sip_inflow_crore'].min():.2f} crore")

print("\nLARGEST MONTH-OVER-MONTH INCREASE")
print(f"Month: {largest_increase['month'].strftime('%Y-%m')}")
print(f"Change: ₹{largest_increase['mom_change_crore']:.2f} crore")
print(f"Growth: {largest_increase['mom_growth_pct']:.2f}%")

print("\nLARGEST MONTH-OVER-MONTH DECREASE")
print(f"Month: {largest_decrease['month'].strftime('%Y-%m')}")
print(f"Change: ₹{largest_decrease['mom_change_crore']:.2f} crore")
print(f"Growth: {largest_decrease['mom_growth_pct']:.2f}%")

# Save monthly analysis
df.to_csv("reports/sip_monthly_consistency.csv", index=False)

# Plot monthly inflow trend
plt.figure(figsize=(11, 5))
plt.plot(df["month"], df["sip_inflow_crore"], marker="o")
plt.title("Monthly SIP Inflow Trend")
plt.xlabel("Month")
plt.ylabel("SIP Inflow (₹ crore)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reports/sip_monthly_consistency.png", dpi=150)
plt.close()

# Plot month-over-month growth
plt.figure(figsize=(11, 5))
plt.bar(df["month"].dt.strftime("%Y-%m"), df["mom_growth_pct"])
plt.title("Monthly SIP Inflow Growth")
plt.xlabel("Month")
plt.ylabel("MoM Growth (%)")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("reports/sip_monthly_growth.png", dpi=150)
plt.close()

print("\nReports saved:")
print("- reports/sip_monthly_consistency.csv")
print("- reports/sip_monthly_consistency.png")
print("- reports/sip_monthly_growth.png")
