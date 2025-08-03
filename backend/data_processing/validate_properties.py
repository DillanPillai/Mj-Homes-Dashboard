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
    issues = {}

    for col in required_columns:
        if col not in df.columns:
            issues[col] = "Missing column"
        else:
            missing_rows = df[df[col].isnull()].index.tolist()
            if missing_rows:
                issues[col] = missing_rows

    return issues

def main():
    file_path = "Backend/data_processing/DataValidation.xlsx"
    df = load_property_data(file_path)
    if df is not None:
        issues = validate_data(df)
        if issues:
            print("Validation issues found:")
            for field, rows in issues.items():
                print(f"- {field}: {rows}")
        else:
            print("No issues found.")

if __name__ == "__main__":
    main()
    