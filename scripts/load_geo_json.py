import pandas as pd
import geopandas as gpd

# --- CONFIGURATION ---
INPUT_CSV = 'data_raw/nypd-complaints.csv'
GEOJSON_FILE = 'data_raw/nyc-airbnb/neighbourhoods.geojson'
OUTPUT_CSV = 'data_extra/nypd-complaints-neighborhoods.csv'

def main():
    print("🚀 Loading data...")
    # 1. Load the CSV (Complaints) and the GeoJSON (Neighborhood Shapes)
    df = pd.read_csv(INPUT_CSV)
    neighborhoods = gpd.read_file(GEOJSON_FILE)

    # 2. Convert the CSV into a "GeoDataFrame" (Add Geometry)
    # Takes the Longitude/Latitude columns and turns them into mapping points
    points = gpd.GeoDataFrame(
        df, 
        geometry=gpd.points_from_xy(df.Longitude, df.Latitude),
        crs="EPSG:4326"  # GPS data (Lat/Lon)
    )

    print("🔗 Linking complaints to neighborhoods...")
    # 3. The Spatial Join
    # 'sjoin' checks which Polygon (Neighborhood) contains each Point (Complaint)
    # how="left" means "Keep all complaints, even if no neighborhood matches"
    joined = gpd.sjoin(points, neighborhoods, how="left", predicate="within")

    # Drop the extra geometry/index columns created by the join
    cols_to_drop = ['geometry', 'index_right', 'neighbourhood_group']
    joined = joined.drop(columns=[c for c in cols_to_drop if c in joined.columns])

    print(f"💾 Saving to {OUTPUT_CSV}...")
    joined.to_csv(OUTPUT_CSV, index=False)
    print("✅ Done!")

if __name__ == "__main__":
    main()