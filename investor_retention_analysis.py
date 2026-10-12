
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_FILE = Path("data/raw/08_investor_transactions.csv")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load transaction data
df = pd.read_csv(DATA_FILE, parse_dates=["transaction_date"])

if df["transaction_date"].isna().any():
    raise ValueError("Missing or invalid transaction dates found.")

df["month"] = df["transaction_date"].dt.to_period("M")

# 1. Number of active months per investor
investor_activity = (
    df.groupby("investor_id")
    .agg(
        active_months=("month", "nunique"),
        first_active_month=("month", "min"),
        last_active_month=("month", "max"),
        transaction_count=("month", "size"),
    )
    .reset_index()
)

investor_activity["activity_segment"] = pd.cut(
    investor_activity["active_months"],
    bins=[0, 1, 5, float("inf")],
    labels=["1 month", "2-5 months", "6+ months"],
)

segment_summary = (
    investor_activity.groupby(
        "activity_segment", observed=False
    )
    .agg(investor_count=("investor_id", "nunique"))
    .reset_index()
)

segment_summary["investor_percentage"] = (
    segment_summary["investor_count"]
    / investor_activity["investor_id"].nunique()
    * 100
).round(2)

segment_summary.to_csv(
    REPORT_DIR / "investor_activity_segments.csv", index=False
)

print("\nINVESTOR ACTIVITY SEGMENTS")
print(segment_summary.to_string(index=False))

# 2. Monthly active investors
monthly_active = (
    df.groupby("month")["investor_id"]
    .nunique()
    .rename("active_investors")
    .reset_index()
)

monthly_active["month"] = monthly_active["month"].astype(str)
monthly_active.to_csv(
    REPORT_DIR / "monthly_active_investors.csv", index=False
)

print("\nMONTHLY ACTIVE INVESTORS")
print(monthly_active.to_string(index=False))

# 3. Month-to-month repeat activity
# Compare investors active in each month with those active in the next month.
monthly_sets = {
    month: set(group["investor_id"])
    for month, group in df.groupby("month")
}

months = sorted(monthly_sets)
repeat_rows = []

for current_month, next_month in zip(months, months[1:]):
    current_investors = monthly_sets[current_month]
    next_investors = monthly_sets[next_month]
    returned = current_investors & next_investors

    repeat_rows.append({
        "month": str(current_month),
        "next_month": str(next_month),
        "current_active_investors": len(current_investors),
        "next_month_active_investors": len(next_investors),
        "investors_active_in_both_months": len(returned),
        "repeat_activity_pct": round(
            len(returned) / len(current_investors) * 100, 2
        ) if current_investors else 0,
    })

repeat_summary = pd.DataFrame(repeat_rows)
repeat_summary.to_csv(
    REPORT_DIR / "month_to_month_repeat_activity.csv", index=False
)

print("\nMONTH-TO-MONTH REPEAT ACTIVITY")
print(repeat_summary.to_string(index=False))

# 4. Chart: monthly active investors
plt.figure(figsize=(12, 5))
plt.plot(
    monthly_active["month"],
    monthly_active["active_investors"],
    marker="o",
)
plt.title("Monthly Active Investors")
plt.xlabel("Month")
plt.ylabel("Unique Active Investors")
plt.xticks(rotation=60, ha="right")
plt.tight_layout()
plt.savefig(
    REPORT_DIR / "monthly_active_investors.png", dpi=150
)
plt.close()

# 5. Chart: repeat activity percentage
plt.figure(figsize=(12, 5))
plt.plot(
    repeat_summary["month"],
    repeat_summary["repeat_activity_pct"],
    marker="o",
)
plt.title("Month-to-Month Repeat Activity")
plt.xlabel("Starting Month")
plt.ylabel("Investors Also Active Next Month (%)")
plt.xticks(rotation=60, ha="right")
plt.tight_layout()
plt.savefig(
    REPORT_DIR / "month_to_month_repeat_activity.png", dpi=150
)
plt.close()

print("\nAnalysis completed. Reports and charts saved in reports/.")
