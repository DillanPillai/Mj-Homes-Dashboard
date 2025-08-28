import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

load_dotenv()

# API setup (PROD key for real data)
API_KEY = os.getenv("MARKET_RENT_API_KEY_PROD")
BASE_URL = "https://api.business.govt.nz/gateway/tenancy-services/market-rent/v2"

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

# Extract Auckland, Hamilton, Wellington
desired_labels = {"Auckland", "Hamilton City", "Wellington City"}
area_codes = [(a["code"], a["label"]) for a in areas["items"] if a["label"] in desired_labels]
print(f"Target areas: {area_codes}")

# Step 2: Fetch data month-by-month for up to 60 months (5 years)
today = datetime.today()
# start from last full month
current = today.replace(day=1) - relativedelta(months=1)

all_data = []

for code, label in area_codes:
    print(f"\nFetching up to 60 months of data for {label} ({code})...")
    for i in range(60):  # go back 5 years
        period = (current - relativedelta(months=i)).strftime("%Y-%m")
        print(f"  Trying {label} {period}...")

        stats_url = f"{BASE_URL}/statistics"
        params = {
            "period-ending": period,
            "num-months": 1,   # single month at a time
            "area-definition": "territorial-authority-2019",
            "area-codes": code
        }

        resp = requests.get(stats_url, headers=headers, params=params)
        if resp.status_code == 200:
            data = resp.json()
            records = data.get("items", data) if isinstance(data, dict) else data
            if records:  # only append if there’s data
                for record in records:
                    if isinstance(record, dict):
                        record["area_label"] = label
                        record["area_code"] = code
                        record["period"] = period
                        all_data.append(record)
        else:
            print(f"    Skipped {label} {period} (HTTP {resp.status_code})")

# Step 3: Save results
df = pd.DataFrame(all_data)
output_file = "market_rent_timeseries.csv"
df.to_csv(output_file, index=False)
print(f"\nSaved {len(df)} rows to {output_file}")
