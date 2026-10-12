
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load the dataset
file_path = Path("data/raw/03_aum_by_fund_house.csv")
df = pd.read_csv(file_path)

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Inspect reporting dates
print("AUM Analysis")
print("------------")
print("Total records:", len(df))
print("Reporting dates:", df["date"].nunique())
print("Date range:", df["date"].min().date(), "to", df["date"].max().date())

# Use the latest reporting date
latest_date = df["date"].max()
latest_df = df[df["date"] == latest_date].copy()

# Rank fund houses by AUM
latest_df = latest_df.sort_values("aum_crore", ascending=False)

print("\nLatest reporting date:", latest_date.date())
print("\nTop 10 fund houses by AUM:")
print(
    latest_df[["fund_house", "aum_lakh_crore", "aum_crore", "num_schemes"]]
    .head(10)
    .to_string(index=False)
)

# Create output directory
output_dir = Path("reports")
output_dir.mkdir(parents=True, exist_ok=True)

# Save ranking
ranking_path = output_dir / "fund_house_aum_ranking.csv"
latest_df.to_csv(ranking_path, index=False)

# Plot the top 10 fund houses
top10 = latest_df.head(10).sort_values("aum_lakh_crore")

plt.figure(figsize=(11, 6))
plt.barh(top10["fund_house"], top10["aum_lakh_crore"])
plt.title(f"Top 10 Fund Houses by AUM ({latest_date.date()})")
plt.xlabel("AUM (₹ lakh crore)")
plt.ylabel("Fund House")
plt.tight_layout()

chart_path = output_dir / "fund_house_aum_top10.png"
plt.savefig(chart_path, dpi=150)
plt.close()

print("\nRanking saved to:", ranking_path)
print("Chart saved to:", chart_path)
