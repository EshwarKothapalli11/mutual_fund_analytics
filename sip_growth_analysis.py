
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load the cleaned SIP dataset
file_path = Path("data/processed/04_monthly_sip_inflows_cleaned.csv")
df = pd.read_csv(file_path)

df["month"] = pd.to_datetime(df["month"], format="%Y-%m")
df = df.sort_values("month")

# Create the output directory
output_dir = Path("reports")
output_dir.mkdir(parents=True, exist_ok=True)

# Create two charts with separate y-axes
fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.plot(
    df["month"],
    df["sip_inflow_crore"],
    marker="o",
    markersize=3,
    label="Monthly SIP inflow (₹ crore)"
)
ax1.set_xlabel("Month")
ax1.set_ylabel("SIP inflow (₹ crore)")
ax1.tick_params(axis="x", rotation=45)
ax1.grid(True, alpha=0.3)

ax2 = ax1.twinx()
ax2.plot(
    df["month"],
    df["yoy_growth_pct"],
    linestyle="--",
    label="YoY growth (%)"
)
ax2.set_ylabel("YoY growth (%)")

# Combine both legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.title("Monthly SIP Inflows and Year-over-Year Growth")
fig.tight_layout()

chart_path = output_dir / "sip_inflows_vs_yoy_growth.png"
fig.savefig(chart_path, dpi=150)
plt.close(fig)

print("Months analyzed:", len(df))
print("Missing YoY growth values:", df["yoy_growth_pct"].isna().sum())
print("Chart saved to:", chart_path)
