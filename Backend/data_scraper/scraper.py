import pandas as pd

def scrape_listings():
    print("Loading mock listings from Excel...")
    path = "Backend/data_processing/MockData.xlsx"
    try:
        df = pd.read_excel(path)
        return df
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return pd.DataFrame()  # return empty to avoid pipeline crash
