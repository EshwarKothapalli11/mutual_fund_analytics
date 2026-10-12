
from pathlib import Path
import pandas as pd

# Define project paths
PROJECT_DIR = Path(__file__).resolve().parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load fund master dataset
DATA_FILE = RAW_DIR / "01_fund_master.csv"
df = pd.read_csv(DATA_FILE)

# Display exploration results
print("TOTAL FUNDS:", len(df))
print("UNIQUE FUND HOUSES:", df["fund_house"].nunique())

print("\nFUND HOUSES:")
print(df["fund_house"].value_counts().to_string())

print("\nCATEGORIES:")
print(df["category"].value_counts().to_string())

print("\nSUB-CATEGORIES:")
print(df["sub_category"].value_counts().to_string())

print("\nRISK GRADES:")
print(df["risk_category"].value_counts().to_string())

print("\nPLAN TYPES:")
print(df["plan"].value_counts().to_string())

print("\nSCHEME CODE RANGE:")
print("Minimum:", df["amfi_code"].min())
print("Maximum:", df["amfi_code"].max())

# Save exploration results
report_path = REPORT_DIR / "fund_master_exploration.txt"

with open(report_path, "w", encoding="utf-8") as report:
    report.write("FUND MASTER EXPLORATION REPORT\n")
    report.write("=" * 40 + "\n\n")

    report.write(f"Total schemes: {len(df)}\n")
    report.write(f"Unique fund houses: {df['fund_house'].nunique()}\n\n")

    for title, column in [
        ("FUND HOUSES", "fund_house"),
        ("CATEGORIES", "category"),
        ("SUB-CATEGORIES", "sub_category"),
        ("RISK GRADES", "risk_category"),
        ("PLAN TYPES", "plan"),
    ]:
        report.write(f"{title}\n")
        report.write(df[column].value_counts().to_string())
        report.write("\n\n")

    report.write(
        f"Scheme code range: {df['amfi_code'].min()} "
        f"to {df['amfi_code'].max()}\n"
    )

print(f"\nExploration report saved to: {report_path}")
