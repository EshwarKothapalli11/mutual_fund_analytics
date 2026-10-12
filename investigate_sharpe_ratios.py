
import pandas as pd
from pathlib import Path

# Load the original dataset without modifying it
input_file = Path("data/raw/07_scheme_performance.csv")
df = pd.read_csv(input_file)

# Identify liquid-fund records
liquid = df[df["category"] == "Liquid"].copy()

# Compare Sharpe ratio with 3-year return
liquid["difference"] = (
    liquid["sharpe_ratio"] - liquid["return_3yr_pct"]
).round(4)

# Flag exact matches for investigation, not automatic correction
liquid["potential_anomaly"] = liquid["difference"].abs() < 0.0001

print("Sharpe Ratio Data-Quality Investigation")
print("---------------------------------------")
print("Liquid schemes inspected:", len(liquid))
print("Exact Sharpe/return matches:",
      int(liquid["potential_anomaly"].sum()))

print("\nFindings:")
print(liquid[
    ["scheme_name", "return_3yr_pct", "sharpe_ratio",
     "std_dev_ann_pct", "difference", "potential_anomaly"]
].to_string(index=False))

# Save investigation report separately
output_dir = Path("reports")
output_dir.mkdir(parents=True, exist_ok=True)

report_file = output_dir / "sharpe_ratio_investigation.csv"
liquid.to_csv(report_file, index=False)

print("\nInvestigation report saved to:", report_file)
print("Original dataset was not modified.")
