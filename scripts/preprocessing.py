import pandas as pd
import numpy as np
import os

# ==========================================
# FILE & FOLDER CONFIGURATION
# ==========================================
INPUT_DIR = 'data_raw'
OUTPUT_DIR = 'data_clean'

# Define your specific filenames here
FILENAMES = {
    "nypd": "nypd-complaints.csv",
    "sales": "nyc-rolling-sales.csv",
    "airbnb": "nyc-airbnb/listings_detail.csv"
}

# ==========================================
# 1. SCHEMA DEFINITIONS (Source -> Target)
# ==========================================

# NYPD: Maps original CSV headers to clean Database/VKG columns
NYPD_COL_MAP = {
    "CMPLNT_NUM": "complaint_id",
    "BORO_NM": "borough",
    "CMPLNT_FR_DT": "date_str",
    "CMPLNT_FR_TM": "time_str",
    "CRM_ATPT_CPTD_CD": "offense_status",
    "LAW_CAT_CD": "offense_level",     
    "LOC_OF_OCCUR_DESC": "premise_pos", 
    "OFNS_DESC": "offense_type",
    "PREM_TYP_DESC": "premise_type",    
    "VIC_SEX": "victim_sex",
    "VIC_AGE_GROUP": "victim_age_group",
    "Latitude": "latitude",
    "Longitude": "longitude"
}

# SALES: Maps original CSV headers to clean Database/VKG columns
SALES_COL_MAP = {
    # 'sale_id' will be generated dynamically
    "BOROUGH": "borough_code", # Requires ID->Name mapping
    "NEIGHBORHOOD": "neighborhood",
    "BUILDING CLASS CATEGORY": "building_category",
    "TOTAL UNITS": "total_units",
    "GROSS SQUARE FEET": "gross_sqft",
    "YEAR BUILT": "year_built",
    "SALE PRICE": "sale_price",
    "SALE DATE": "sale_date"
}

# AIRBNB: Maps original CSV headers to clean Database/VKG columns
AIRBNB_COL_MAP = {
    "id": "listing_id",
    "last_scraped": "scrape_date",
    "name": "listing_name",
    "host_id": "host_id",
    "host_name": "host_name",
    "host_since": "host_since",
    "host_location": "host_location",
    "host_neighbourhood": "host_neighborhood",
    "neighbourhood_cleansed": "neighborhood",      
    "neighbourhood_group_cleansed": "borough",     
    "latitude": "latitude",
    "longitude": "longitude",
    "property_type": "property_type",
    "room_type": "room_type",
    "accommodates": "capacity",
    "square_feet": "square_feet",
    "price": "daily_price",
    "minimum_nights": "min_nights",
    "maximum_nights": "max_nights",
    "availability_365": "availability_year",
    "first_review": "first_review_date",
    "last_review": "last_review_date",
    "review_scores_location": "location_score",
    "calculated_host_listings_count": "host_listings_count"
}


# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================

def clean_types(df, id_cols=[], date_cols=[], float_cols=[], int_cols=[], text_cols=[]):
    # 1. Clean Text
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().replace({'': np.nan, 'nan': np.nan, 'None': np.nan})

    # 2. Clean Floats
    for col in float_cols:
        if col in df.columns:
            if df[col].dtype == 'object':
                 df[col] = df[col].str.replace(r'[$,]', '', regex=True)
                 df[col] = df[col].replace([' -  ', '-'], np.nan)
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 3. Clean Integers (Handle '2.0' -> 2)
    for col in int_cols:
        if col in df.columns:
            if df[col].dtype == 'object':
                 df[col] = df[col].str.replace(r'[$,]', '', regex=True)
                 df[col] = df[col].replace([' -  ', '-'], np.nan)
            # Convert to float first to handle '2.0', then round, then cast to Int64 (nullable int)
            vals = pd.to_numeric(df[col], errors='coerce')
            df[col] = vals.round().astype('Int64')

    # 4. Clean Dates
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
    # 5. Enforce IDs
    for col in id_cols:
        if col in df.columns:
             # Remove .0 from IDs if they were read as floats
             df[col] = df[col].astype(str).str.replace(r'\.0$', '', regex=True)

    return df

def get_path(filename, directory):
    return os.path.join(directory, filename)

# ==========================================
# 3. ETL PIPELINES
# ==========================================

def process_nypd(filename):
    print(f"--- Processing {filename} ---")
    
    input_path = get_path(filename, INPUT_DIR)
    
    # Check if file exists to avoid crashes
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return None

    df = pd.read_csv(input_path, usecols=NYPD_COL_MAP.keys())
    df = df.rename(columns=NYPD_COL_MAP)
    
    df = clean_types(
        df, 
        id_cols=['complaint_id'],
        date_cols=['date_str'], 
        float_cols=['latitude', 'longitude'],
        int_cols=[], # No pure integers here
        text_cols=['borough', 'offense_desc', 'premise_desc', 'crime_status']
    )
    
    # Filter null PKs
    df = df.dropna(subset=['complaint_id'])
    
    # Upper case for joining
    df['borough'] = df['borough'].str.upper()
    
    print(f" -> NYPD Cleaned: {len(df)} rows")
    return df

def process_sales(filename):
    print(f"--- Processing {filename} ---")
    
    input_path = get_path(filename, INPUT_DIR)
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return None

    df = pd.read_csv(input_path, usecols=SALES_COL_MAP.keys())
    df = df.rename(columns=SALES_COL_MAP)
    
    df = clean_types(
        df,
        date_cols=['sale_date'],
        float_cols=['sale_price', 'gross_sqft'], 
        int_cols=['year_built', 'total_units'],
        text_cols=['neighborhood', 'building_category']
    )
    
    # Since there is no PK, we create a surrogate key.
    # Using index + 1 ensures a unique integer sequence (1, 2, 3...)
    df.insert(0, 'sale_id', range(1, 1 + len(df)))
    
    # Borough Code -> Name
    boro_map = {1: 'MANHATTAN', 2: 'BRONX', 3: 'BROOKLYN', 4: 'QUEENS', 5: 'STATEN ISLAND'}
    df['borough'] = df['borough_code'].map(boro_map)
    df = df.drop(columns=['borough_code'])
    
    # Clean Data
    # Filter trivial sales (price < $10k often transfer between family members, noise for ROI)    
    df = df.dropna(subset=['sale_price'])
    df = df[df['sale_price'] > 10000]
    
    print(f" -> Sales Cleaned: {len(df)} rows")
    return df

def process_airbnb(filename):
    print(f"--- Processing {filename} ---")
    
    input_path = get_path(filename, INPUT_DIR)

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return None
    
    # Handling "Misaligned Columns":
    # 1. quotechar='"': Handles newlines inside descriptions.
    # 2. escapechar='\\': Handles escaped quotes.
    # 3. on_bad_lines='skip': Skips rows that are physically broken (critical fix for "misaligned" rows).
    try:
        df = pd.read_csv(
            input_path, 
            usecols=AIRBNB_COL_MAP.keys(),
            quotechar='"',
            escapechar='\\',
            on_bad_lines='skip', 
            low_memory=False
        )
    except Exception as e:
        print(f"Error reading Airbnb file: {e}")
        return pd.DataFrame()

    df = df.rename(columns=AIRBNB_COL_MAP)
    
    df = clean_types(
        df,
        id_cols=['listing_id', 'host_id'],
        date_cols=['host_since', 'scrape_date', 'last_review_date'],
        float_cols=['price', 'latitude', 'longitude', 'square_feet'],
        int_cols=['host_listings_count', 'accommodates', 'min_nights', 
                  'max_nights', 'num_reviews', 'review_score_loc', 'availability_365'],
        text_cols=['neighborhood', 'borough', 'property_type', 'room_type', 'host_location']
    )
    
    # Host Analysis Tags
    nyc_keys = ['NEW YORK', 'NY', 'QUEENS', 'BROOKLYN', 'BRONX', 'MANHATTAN', 'STATEN ISLAND']
    # If host_location is valid string, check for NYC keys. If NaN, assume False (Conservative)
    df['host_is_outside_nyc'] = ~df['host_location'].str.upper().str.contains('|'.join(nyc_keys), na=False)
    
    # Upper case for joining
    df['neighborhood'] = df['neighborhood'].str.upper()
    df['borough'] = df['borough'].str.upper()
    
    # Filter Null PKs
    df = df.dropna(subset=['listing_id'])
    
    print(f" -> Airbnb Cleaned: {len(df)} rows")
    return df

# ==========================================
# 4. EXECUTION
# ==========================================
if __name__ == "__main__":
    # Create Output Directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Reading from: {INPUT_DIR}")
    print(f"Writing to:   {OUTPUT_DIR}\n")

    # Process nypd
    nypd_df = process_nypd(FILENAMES["nypd"])
    if nypd_df is not None:
        nypd_df.to_csv(get_path(FILENAMES["nypd"], OUTPUT_DIR), index=False)

    # Process sales
    sales_df = process_sales(FILENAMES["sales"])
    if sales_df is not None:
        sales_df.to_csv(get_path(FILENAMES["sales"], OUTPUT_DIR), index=False)

    # Process airbnb
    airbnb_df = process_airbnb(FILENAMES["airbnb"])
    if airbnb_df is not None:
        # Check and create output subdirectory for airbnb if needed
        out_path = get_path(FILENAMES["airbnb"], OUTPUT_DIR)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        
        # quoting=1 (QUOTE_ALL) ensures text fields with commas don't break the output CSV
        airbnb_df.to_csv(out_path, index=False, quoting=1)
    
    print("\nSUCCESS! All files generated.")