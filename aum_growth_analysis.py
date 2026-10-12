
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load data
df = pd.read_csv("data/raw/03_aum_by_fund_house.csv")
df["date"] = pd.to_datetime(df["date"])

# Select earliest and latest reporting dates
earliest_date = df["date"].min()
latest_date = df["date"].max()

earliest = df[df["date"] == earliest_date][
    ["fund_house", "aum_lakh_crore"]
].rename(columns={"aum_lakh_crore": "starting_aum"})

latest = df[df["date"] == latest_date][
    ["fund_house", "aum_lakh_crore"]
].rename(columns={"aum_lakh_crore": "latest_aum"})

# Match fund houses across both dates
growth = earliest.merge(latest, on="fund_house", how="inner")

# Calculate absolute and percentage growth
growth["aum_change"] = growth["latest_aum"] - growth["starting_aum"]
growth["growth_pct"] = (
    growth["aum_change"] / growth["starting_aum"] * 100
)

growth = growth.sort_values("growth_pct", ascending=False)

print("AUM Growth Analysis")
print("-------------------")
print("Starting date:", earliest_date.date())
print("Ending date:", latest_date.date())
print("Fund houses matched:", len(growth))
print("\nGrowth ranking:")
print(growth.round(2).to_string(index=False))

# Save results
output_dir = Path("reports")
output_dir.mkdir(parents=True, exist_ok=True)

report_path = output_dir / "fund_house_aum_growth.csv"
growth.to_csv(report_path, index=False)

# Plot percentage growth
plot_data = growth.sort_values("growth_pct")

plt.figure(figsize=(11, 6))
plt.barh(plot_data["fund_house"], plot_data["growth_pct"])
plt.title("Fund-House AUM Growth: Earliest to Latest Reporting Date")
plt.xlabel("AUM Growth (%)")
plt.ylabel("Fund House")
plt.tight_layout()

chart_path = output_dir / "fund_house_aum_growth.png"
plt.savefig(chart_path, dpi=150)
plt.close()

print("\nReport saved to:", report_path)
print("Chart saved to:", chart_path)
