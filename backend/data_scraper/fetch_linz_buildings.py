import os
import geopandas as gpd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
LINZ_API_KEY = os.getenv("LINZ_API_KEY")

if not LINZ_API_KEY:
    raise ValueError("Missing LINZ_API_KEY. Please add it to your .env file.")

# Base WFS URL for LINZ
BASE_URL = f"https://data.linz.govt.nz/services;key={LINZ_API_KEY}/wfs"

# Layer ID for NZ Building Outlines
LAYER_ID = "layer-101290"

# Build WFS query
WFS_URL = (
    f"{BASE_URL}?service=WFS&version=2.0.0&request=GetFeature"
    f"&typeName={LAYER_ID}"
    f"&outputFormat=application/json"
    f"&count=100"   # fetch small batch first for testing
)

print("[LINZ] Fetching building outlines (test batch)...")

try:
    gdf = gpd.read_file(WFS_URL)
    print(f"[LINZ] Retrieved {len(gdf)} building outlines")

    # Save with geometry
    gdf.to_file("linz_building_outlines.geojson", driver="GeoJSON")
    print("[LINZ] Saved: linz_building_outlines.geojson")

    # Save without geometry (attributes only)
    gdf.drop(columns="geometry").to_csv("linz_building_outlines.csv", index=False)
    print("[LINZ] Saved: linz_building_outlines.csv (attributes only)")

except Exception as e:
    print(f"[ERROR] Failed to fetch or save data: {e}")
