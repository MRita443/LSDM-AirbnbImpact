import pandas as pd
import os

INPUT_CSV = 'data_raw/nyc-airbnb/listings_detail.csv'
OUTPUT_CSV = 'data_processed/nyc-airbnb/listings_detail_no_bad_lines.csv'

try:
    df = pd.read_csv(
        INPUT_CSV,
        quotechar='"',
        escapechar='\\',
        on_bad_lines='skip', 
        low_memory=False
    )
except Exception as e:
    print(f"Error reading Airbnb file: {e}")

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

# quoting=1 (QUOTE_ALL) ensures text fields with commas don't break the output CSV
df.to_csv(OUTPUT_CSV, index=False, quoting=1, encoding="utf-8")
