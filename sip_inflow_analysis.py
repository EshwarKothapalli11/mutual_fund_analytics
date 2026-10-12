
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load the SIP dataset
file_path = Path("data/processed/04_monthly_sip_inflows_cleaned.csv")
df = pd.read_csv(file_path)

# Convert month to a date
df["month"] = pd.to_datetime(df["month"], format="%Y-%m")

# Sort by month
df = df.sort_values("month")

# Display basic statistics
print("SIP Inflow Analysis")
print("-------------------")
print("Number of months:", len(df))
print("Average monthly SIP inflow (crore):",
      round(df["sip_inflow_crore"].mean(), 2))
print("Minimum monthly SIP inflow (crore):",
      round(df["sip_inflow_crore"].min(), 2))
print("Maximum monthly SIP inflow (crore):",
      round(df["sip_inflow_crore"].max(), 2))

# Create output directory
output_dir = Path("reports")
output_dir.mkdir(parents=True, exist_ok=True)

# Plot monthly SIP inflows
plt.figure(figsize=(12, 6))
plt.plot(
    df["month"],
    df["sip_inflow_crore"],
    marker="o",
    linewidth=1.5
)

plt.title("Monthly SIP Inflows Over Time")
plt.xlabel("Month")
plt.ylabel("SIP Inflow (₹ crore)")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save chart
chart_path = output_dir / "monthly_sip_inflows.png"
plt.savefig(chart_path, dpi=150)
plt.close()

print("\nChart saved to:", chart_path)