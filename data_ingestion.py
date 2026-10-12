
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


def inspect_csv_files():
    files = sorted(RAW_DIR.glob("*.csv"))
    summaries = []

    if not files:
        print("No CSV files found in data/raw/")
        return

    print(f"Found {len(files)} CSV datasets.")

    for file in files:
        print(f"\n{'=' * 60}")
        print(f"Dataset: {file.name}")

        try:
            df = pd.read_csv(file)
            missing = df.isnull().sum()
            missing_columns = {
                column: int(count)
                for column, count in missing.items()
                if count > 0
            }

            print("Shape:", df.shape)
            print("\nData types:\n", df.dtypes)
            print("\nFirst 5 rows:\n", df.head())
            print("\nMissing values by column:\n", missing[missing > 0])
            print("Duplicate rows:", int(df.duplicated().sum()))

            summaries.append({
                "filename": file.name,
                "rows": len(df),
                "columns": len(df.columns),
                "missing_cells": int(missing.sum()),
                "missing_columns": str(missing_columns),
                "duplicate_rows": int(df.duplicated().sum())
            })

        except Exception as error:
            print(f"Error reading {file.name}: {error}")

    if summaries:
        output = REPORT_DIR / "data_quality_summary.csv"
        pd.DataFrame(summaries).to_csv(output, index=False)
        print(f"\nReport saved to: {output}")


if __name__ == "__main__":
    inspect_csv_files()
