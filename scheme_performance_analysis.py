
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load the dataset
df = pd.read_csv("data/raw/07_scheme_performance.csv")

output_dir = Path("reports")
output_dir.mkdir(parents=True, exist_ok=True)

# 1. Top schemes by 3-year returns
top_returns = df.sort_values("return_3yr_pct", ascending=False)

print("TOP 10 SCHEMES BY 3-YEAR RETURNS")
print(top_returns[
    ["scheme_name", "category", "return_3yr_pct", "benchmark_3yr_pct"]
].head(10).to_string(index=False))

# 2. Compare returns against the benchmark
df["benchmark_outperformance_pct"] = (
    df["return_3yr_pct"] - df["benchmark_3yr_pct"]
)

print("\nTOP 10 SCHEMES BY BENCHMARK OUTPERFORMANCE")
print(df.sort_values("benchmark_outperformance_pct", ascending=False)[
    ["scheme_name", "return_3yr_pct",
     "benchmark_3yr_pct", "benchmark_outperformance_pct"]
].head(10).to_string(index=False))

# 3. Top schemes by Sharpe ratio
print("\nTOP 10 SCHEMES BY SHARPE RATIO")
print(df.sort_values("sharpe_ratio", ascending=False)[
    ["scheme_name", "sharpe_ratio", "std_dev_ann_pct", "risk_grade"]
].head(10).to_string(index=False))

# Save detailed results
report_path = output_dir / "scheme_performance_analysis.csv"
df.to_csv(report_path, index=False)

# 4. Plot 3-year returns for the top 10 schemes
top10 = top_returns.head(10).sort_values("return_3yr_pct")

plt.figure(figsize=(12, 7))
plt.barh(top10["scheme_name"], top10["return_3yr_pct"])
plt.title("Top 10 Mutual Fund Schemes by 3-Year Returns")
plt.xlabel("3-Year Return (%)")
plt.ylabel("Scheme")
plt.tight_layout()

chart_path = output_dir / "top_10_scheme_returns.png"
plt.savefig(chart_path, dpi=150)
plt.close()

# 5. Plot return versus risk
plt.figure(figsize=(9, 6))
plt.scatter(df["std_dev_ann_pct"], df["return_3yr_pct"])
plt.title("3-Year Returns vs Annualized Standard Deviation")
plt.xlabel("Annualized Standard Deviation (%)")
plt.ylabel("3-Year Return (%)")
plt.grid(True, alpha=0.3)
plt.tight_layout()

risk_chart_path = output_dir / "scheme_returns_vs_risk.png"
plt.savefig(risk_chart_path, dpi=150)
plt.close()

print("\nAnalysis saved to:", report_path)
print("Returns chart saved to:", chart_path)
print("Risk chart saved to:", risk_chart_path)
