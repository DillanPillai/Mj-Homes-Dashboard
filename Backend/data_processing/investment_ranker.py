import pandas as pd

def load_property_data(file_path):
    """
    Loads the property dataset from an Excel file.
    """
    try:
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
        print("Property data loaded successfully.\n")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def rank_top_suburbs(df, top_n=10):
    """
    Ranks suburbs based on highest rent and lowest days on market.
    """
    # Drop rows with missing values in key columns
    df_clean = df.dropna(subset=["Suburb", "Weekly Rent ($NZD)", "Days on Market"])

    # Sort suburbs by highest Rent and lowest Days on Market
    ranked = df_clean.sort_values(
        by=["Weekly Rent ($NZD)", "Days on Market"],
        ascending=[False, True]
    )

    print(f"Top {top_n} Suburbs by Investment Potential:\n")
    print(ranked[["Suburb", "Weekly Rent ($NZD)", "Days on Market", "Bedrooms", "Listing Type"]].head(top_n))

def main():
    file_path = "Backend/data_processing/MockData.xlsx"  # Path relative to root
    df = load_property_data(file_path)

    if df is not None:
        rank_top_suburbs(df)

if __name__ == "__main__":
    main()
