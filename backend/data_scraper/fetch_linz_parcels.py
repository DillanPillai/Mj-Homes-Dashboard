import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

API_KEY = os.getenv("LINZ_API_KEY")
if not API_KEY:
    raise ValueError("LINZ_API_KEY not set in .env")

# LINZ WFS endpoint for Primary Parcels
BASE_URL = "https://data.linz.govt.nz/services;key={key}/wfs".format(key=API_KEY)

# Parameters for the WFS GetFeature request
params = {
    "service": "WFS",
    "version": "2.0.0",
    "request": "GetFeature",
    "typeName": "layer-50772",   # NZ Primary Parcels layer ID
    "outputFormat": "json",
    "count": 1000                # number of records per request
}

print("[LINZ] Requesting NZ Primary Parcels data...")

resp = requests.get(BASE_URL, params=params)
resp.raise_for_status()

data = resp.json()
features = data.get("features", [])

if not features:
    print("[LINZ] No features returned.")
else:
    print(f"[LINZ] Retrieved {len(features)} features")

    # Flatten features into a DataFrame
    rows = []
    for f in features:
        props = f.get("properties", {})
        rows.append(props)

    df = pd.DataFrame(rows)

    # Save to CSV
    out_file = "linz_primary_parcels.csv"
    df.to_csv(out_file, index=False)
    print(f"[LINZ] Saved {len(df)} rows to {out_file}")
