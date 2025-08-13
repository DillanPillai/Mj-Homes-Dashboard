import os
import requests
import pandas as pd
from dotenv import load_dotenv
import json

load_dotenv()

# API setup
API_KEY = os.getenv("MARKET_RENT_API_KEY_SANDBOX")
BASE_URL = "https://api.business.govt.nz/sandbox/tenancy-services/market-rent/v2"

headers = {
    "Ocp-Apim-Subscription-Key": API_KEY
}

# Step 1: Get area codes
area_definition = "territorial-authority-2019"
print(f"Fetching area codes from {area_definition}...")
area_url = f"{BASE_URL}/area-definitions/{area_definition}"
area_resp = requests.get(area_url, headers=headers)
area_resp.raise_for_status()
areas = area_resp.json()

# Extract only Auckland, Hamilton, and Wellington
desired_labels = {"Auckland", "Hamilton City", "Wellington City"}
area_codes = [(a["code"], a["label"]) for a in areas["items"] if a["label"] in desired_labels]

print(f"Found {len(area_codes)} target areas: {area_codes}")

# Step 2: Fetch statistics for each selected area
all_data = []

for code, label in area_codes:
    print(f"Fetching statistics for {label} ({code})...")
    stats_url = f"{BASE_URL}/statistics"
    params = {
        "period-ending": "2024-06",  # last available in sandbox
        "num-months": 12,
        "area-definition": "territorial-authority-2019",
        "area-codes": code
    }

    resp = requests.get(stats_url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()

    # Get the list of records
    records = data.get("items", data) if isinstance(data, dict) else data

    for record in records:
        if isinstance(record, dict):
            record["area_label"] = label
            record["area_code"] = code
            all_data.append(record)

# Step 3: Save to CSV
df = pd.DataFrame(all_data)
df.to_csv("market_rent_sample.csv", index=False)
print(f"Saved {len(df)} rows to market_rent_sample.csv")
