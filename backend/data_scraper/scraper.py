import pandas as pd

def scrape_listings():
    print("Loading finalised dataset listings from Excel...")
    path = "backend/data_processing/FinalisedDataset.xlsx"
    try:
        df = pd.read_excel(path)
        return df
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return pd.DataFrame()  # return empty to avoid pipeline crash
