
import pandas as pd
from pathlib import Path

# Define input and output paths
input_file = Path("data/raw/04_monthly_sip_inflows.csv")
output_dir = Path("data/processed")
output_file = output_dir / "04_monthly_sip_inflows_cleaned.csv"

# Create the processed-data folder if it doesn't exist
output_dir.mkdir(parents=True, exist_ok=True)

# Load the original dataset
df = pd.read_csv(input_file)

# Validate the dataset
print("Original shape:", df.shape)
print("Duplicate rows:", df.duplicated().sum())
print("Missing values before cleaning:")
print(df.isna().sum())

# Ensure month is stored as text in YYYY-MM format
df["month"] = df["month"].astype(str)

# Preserve missing yoy_growth_pct values.
# Do not replace them with zero or estimate them without source data.

# Save the cleaned copy
df.to_csv(output_file, index=False)

# Verify the saved copy
cleaned_df = pd.read_csv(output_file)

print("\nSaved cleaned dataset:", output_file)
print("Cleaned shape:", cleaned_df.shape)
print("Missing values after cleaning:")
print(cleaned_df.isna().sum())
