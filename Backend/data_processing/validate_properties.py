import pandas as pd

def load_property_data(file_path):
    try:
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()
        print("Property data loaded.\n")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def validate_data(df):
    required_columns = ["Suburb", "Weekly Rent ($NZD)", "Days on Market", "Bedrooms"]
    errors_found = False

    for col in required_columns:
        if col not in df.columns:
            print(f"Missing required column: {col}")
            errors_found = True

    if not errors_found:
        missing = df[required_columns].isnull()
        for col in required_columns:
            missing_rows = missing[missing[col]].index.tolist()
            if missing_rows:
                print(f"Missing values in '{col}': rows {missing_rows}")
                errors_found = True

    if not errors_found:
        print("No missing or invalid values detected.")
    else:
        print(" Data issues found. Please clean the data.")

def main():
    file_path = "Backend/data_processing/MockData.xlsx"
    df = load_property_data(file_path)
    if df is not None:
        validate_data(df)

if __name__ == "__main__":
    main()
