import pandas as pd
from pathlib import Path

raw_folder = Path("data/raw/canadian_retail_prices")
processed_folder = Path("data/processed")

processed_folder.mkdir(parents=True, exist_ok=True)

csv_files = list(raw_folder.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV file found in data/raw/canadian_retail_prices")

raw_csv = csv_files[0]

df = pd.read_csv(raw_csv)

clean_df = df[["REF_DATE", "GEO", "Products", "UOM", "VALUE"]].copy()

clean_df = clean_df.rename(
    columns={
        "REF_DATE": "date",
        "GEO": "location",
        "Products": "product",
        "UOM": "unit",
        "VALUE": "price",
    }
)

clean_df["date"] = pd.to_datetime(clean_df["date"], format="%Y-%m")
clean_df["price"] = pd.to_numeric(clean_df["price"], errors="coerce")

clean_df = clean_df.dropna(subset=["date", "location", "product", "unit", "price"])

clean_df = clean_df.drop_duplicates()

output_path = processed_folder / "retail_prices_clean.csv"

clean_df.to_csv(output_path, index=False)

print("Data transformation completed successfully.")
print(f"Cleaned file saved to: {output_path}")
print(f"Rows: {clean_df.shape[0]}")
print(f"Columns: {clean_df.shape[1]}")
print(clean_df.head())