import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

API_KEY = os.getenv("LINZ_API_KEY")
if not API_KEY:
    raise ValueError("LINZ_API_KEY not set in .env")

base_url = f"https://data.linz.govt.nz/services;key={API_KEY}/wfs"

params = {
    "service": "WFS",
    "version": "2.0.0",
    "request": "GetFeature",
    "typeName": "data.linz.govt.nz:layer-50804",  # type name
    "outputFormat": "json",
    "count": 100  
}

print("Requesting data from LINZ WFS...")

response = requests.get(base_url, params=params)

if response.status_code == 200:
    data = response.json()
    features = data["features"]
    
    if not features:
        print("No features returned.")
    else:
        records = [feature["properties"] for feature in features]
        df = pd.DataFrame(records)
        df.to_csv("linz_property_titles.csv", index=False)
        print("Data saved to linz_property_titles.csv")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
