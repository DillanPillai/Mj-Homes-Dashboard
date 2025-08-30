import os
import requests
import geopandas as gpd

# Load API key from .env
from dotenv import load_dotenv
load_dotenv()
LINZ_API_KEY = os.getenv("LINZ_API_KEY")

# WFS endpoint for NZ Addresses
WFS_URL = f"https://data.linz.govt.nz/services;key={LINZ_API_KEY}/wfs"

# Layer ID for NZ Addresses (from LINZ dataset URL)
LAYER_ID = "105689"  # NZ Addresses

# Build query
params = {
    "service": "WFS",
    "version": "2.0.0",
    "request": "GetFeature",
    "typeNames": f"layer-{LAYER_ID}",
    "outputFormat": "json",
    "srsName": "EPSG:4326",   # ensures lat/long coords
    "count": 1000             # fetch batch size (paginate if needed)
}

response = requests.get(WFS_URL, params=params)

if response.status_code == 200:
    data = response.json()
    # Convert to GeoDataFrame for geospatial analysis
    gdf = gpd.GeoDataFrame.from_features(data["features"])
    gdf.to_csv("linz_addresses.csv", index=False)
    print("Saved NZ Addresses → linz_addresses.csv")
else:
    print("Error:", response.text)
