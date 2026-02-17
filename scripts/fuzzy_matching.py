import pandas as pd
import difflib
import os
import re

# ==========================================
# CONFIGURATION
# ==========================================
INPUT_DIR = "data_raw"
OUTPUT_DIR = "data_processed"

FILES = {"sales": "nyc-rolling-sales.csv", "ref": "nyc-airbnb/neighbourhoods.csv"}

MATCH_THRESHOLD = 0.7

# Map Sales Borough Codes to Reference Borough Names
BOROUGH_MAP = {
    1: "MANHATTAN",
    2: "BRONX",
    3: "BROOKLYN",
    4: "QUEENS",
    5: "STATEN ISLAND",
}

MANUAL_FIXES = {
    ('MANHATTAN', 'CLINTON'): 'HELL\'S KITCHEN', 
    ('MANHATTAN', 'ALPHABET CITY'): 'EAST VILLAGE',
    ('MANHATTAN', 'JAVITS CENTER'): 'HELL\'S KITCHEN',
    ('MANHATTAN', 'MANHATTAN VALLEY'): 'UPPER WEST SIDE',
    ('MANHATTAN', 'SOUTHBRIDGE'): 'TWO BRIDGES',
    
    ('BRONX', 'EAST RIVER'): 'HUNTS POINT', # Industrial waterfront
    
    ('BROOKLYN', 'OCEAN HILL'): 'BEDFORD-STUYVESANT', # Closest proxy if Ocean Hill missing
    ('BROOKLYN', 'WYCKOFF HEIGHTS'): 'BUSHWICK',
    ('BROOKLYN', 'DOWNTOWN-FULTON FERRY'): 'DUMBO',
    ('BROOKLYN', 'DOWNTOWN-METROTECH'): 'DOWNTOWN BROOKLYN',
    ('BROOKLYN', 'JAMAICA BAY'): 'MILL BASIN', # Approximate
    ('BROOKLYN', 'SPRING CREEK'): 'EAST NEW YORK',
    ('BROOKLYN', 'BUSH TERMINAL'): 'SUNSET PARK',
    ('BROOKLYN', 'MADISON'): 'SHEEPSHEAD BAY',
    
    ('QUEENS', 'FLORAL PARK'): 'FLORAL PARK',
    ('QUEENS', 'BEECHHURST'): 'WHITESTONE',
    ('QUEENS', 'BROAD CHANNEL'): 'ARVERNE', # Closest proxy
    ('QUEENS', 'HAMMELS'): 'ROCKAWAY BEACH',
    ('QUEENS', 'HILLCREST'): 'FRESH MEADOWS',
    ('QUEENS', 'OAKLAND GARDENS'): 'BAYSIDE',
}


def get_best_match(query, choices, cutoff):
    """
    Returns the best fuzzy match from a list of choices.
    Returns None if no match meets the cutoff score.
    """
    # get_close_matches returns a list sorted by similarity
    matches = difflib.get_close_matches(query, choices, n=1, cutoff=cutoff)
    return matches[0] if matches else None

def get_root_name(name):
    """
    String cleaning to handle 'FLATBUSH-EAST' or 'UPPER EAST SIDE (59-79)'
    """
    # 1. Remove text in parentheses: "UPPER WEST SIDE (59-79)" -> "UPPER WEST SIDE"
    name = re.sub(r'\s*\(.*?\)', '', name)
    
    # 2. Split by slash and take first: "CASTLE HILL/UNIONPORT" -> "CASTLE HILL"
    if '/' in name:
        name = name.split('/')[0]
    
    # 3. Handle specific direction suffixes
    # "FLATBUSH-EAST" -> "FLATBUSH"
    # Note: We must be careful not to strip "EAST" from "EAST VILLAGE"
    # So we only strip if it follows a hyphen
    name = re.sub(r'-(EAST|WEST|NORTH|SOUTH|CENTRAL)$', '', name)
    
    return name.strip()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("--- Loading Data ---")
    sales_path = os.path.join(INPUT_DIR, FILES["sales"])
    ref_path = os.path.join(INPUT_DIR, FILES["ref"])

    if not os.path.exists(sales_path) or not os.path.exists(ref_path):
        print("Error: Input files not found.")
        return

    sales_df = pd.read_csv(sales_path, index_col=0)
    ref_df = pd.read_csv(ref_path)

    # 1. Prepare Reference Dictionary
    # Structure: { 'MANHATTAN': {'CHELSEA', 'SOHO'...}, 'BRONX': {...} }
    print("--- Building Reference Index ---")
    ref_df["borough_upper"] = ref_df["neighbourhood_group"].str.upper().str.strip()
    ref_df["hood_upper"] = ref_df["neighbourhood"].str.upper().str.strip()
    ref_dict = ref_df.groupby("borough_upper")["hood_upper"].apply(set).to_dict()

    # 2. Prepare Sales Data
    # Convert numeric codes to names to match reference
    sales_df["borough_name_upper"] = sales_df["BOROUGH"].map(BOROUGH_MAP)
    sales_df["hood_upper"] = sales_df["NEIGHBORHOOD"].str.upper().str.strip()

    # 3. Perform Fuzzy Matching
    print("--- Fuzzy Matching Neighborhoods ---")

    # Get unique pairs to avoid re-calculating the same string matches multiple times
    unique_pairs = sales_df[["borough_name_upper", "hood_upper"]].drop_duplicates()
    match_map = {}

    stats = {'manual': 0, 'exact': 0, 'root': 0, 'fuzzy': 0, 'fail': 0}

    for _, row in unique_pairs.iterrows():
        boro = row["borough_name_upper"]
        original = row["hood_upper"]
        
        if (boro, original) in MANUAL_FIXES:
             match_map[(boro, original)] = MANUAL_FIXES[(boro, original)]
             stats['manual'] += 1
             print(f"Manual Fix: {original} -> {MANUAL_FIXES[(boro, original)]}")
             continue # Skip the rest

        # Get valid choices for this borough
        choices = ref_dict.get(boro, set())

        # A. Exact Match (Fastest)
        if original in choices:
            match_map[(boro, original)] = original
            stats['exact'] += 1
            continue
        
        # B. Root Match
        root = get_root_name(original)
        if root in choices:
            match_map[(boro, original)] = root
            stats['root'] += 1
            print(f"Root Match: {original} -> {root}")
            continue
        
        # C. Fuzzy Match (Slower)
        best_guess = get_best_match(original, choices, cutoff=MATCH_THRESHOLD)

        if best_guess:
            match_map[(boro, original)] = best_guess
            stats['fuzzy'] += 1
            print(f"Fixed: {original} -> {best_guess}")
        else:
            # C. No Match (Keep Original)
            match_map[(boro, original)] = original
            stats['fail'] += 1
            print(f"No match for: {original} in {boro}")

    print("\n--- Summary ---")
    print(f"Exact Matches: {stats['exact']}")
    print(f"Manual Fixes:  {stats['manual']}")
    print(f"Root Matches:  {stats['root']}")
    print(f"Fuzzy Matches: {stats['fuzzy']}")
    print(f"Failed:        {stats['fail']}")

    # 4. Apply Map & Save
    print("\n--- Saving Standardized File ---")

    # Create the new column
    def apply_match(row):
        return match_map.get(
            (row["borough_name_upper"], row["hood_upper"]), row["hood_upper"]
        )

    sales_df["NEIGHBORHOOD"] = sales_df.apply(apply_match, axis=1)

    # Cleanup auxiliary columns
    output_df = sales_df.drop(columns=["borough_name_upper", "hood_upper"])

    out_path = os.path.join(OUTPUT_DIR, "nyc-rolling-sales-std-neighborhoods.csv")
    output_df.to_csv(out_path, index=False)
    print(f"✅ Success! Saved to {out_path}")


if __name__ == "__main__":
    main()
