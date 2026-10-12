
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "reports"

fund_master = pd.read_csv(RAW_DIR / "01_fund_master.csv")
nav_history = pd.read_csv(RAW_DIR / "02_nav_history.csv")

master_codes = set(fund_master["amfi_code"].dropna().astype(int))
nav_codes = set(nav_history["amfi_code"].dropna().astype(int))

missing_codes = sorted(master_codes - nav_codes)
extra_codes = sorted(nav_codes - master_codes)

print("Fund master unique scheme codes:", len(master_codes))
print("NAV history unique scheme codes:", len(nav_codes))
print("Master codes missing from NAV history:", len(missing_codes))
print("NAV codes absent from fund master:", len(extra_codes))

if missing_codes:
    print("\nCodes in fund master but missing from NAV history:")
    print(missing_codes)
else:
    print("\nAll fund master codes exist in NAV history.")

if extra_codes:
    print("\nCodes in NAV history but absent from fund master:")
    print(extra_codes)

REPORT_DIR.mkdir(parents=True, exist_ok=True)

report = pd.DataFrame({
    "check": [
        "fund_master_unique_codes",
        "nav_history_unique_codes",
        "master_codes_missing_from_nav",
        "nav_codes_absent_from_master",
    ],
    "count": [
        len(master_codes),
        len(nav_codes),
        len(missing_codes),
        len(extra_codes),
    ],
})

report.to_csv(REPORT_DIR / "scheme_code_validation.csv", index=False)
print("\nValidation report saved to reports/scheme_code_validation.csv")
