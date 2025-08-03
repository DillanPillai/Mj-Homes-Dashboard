import pandas as pd
import os

# Load the raw LINZ titles CSV from the root directory
raw_csv_path = os.path.join("linz_property_titles.csv")
cleaned_csv_path = os.path.join("Backend", "data_processing", "cleaned_linz_property_titles.csv")

# Read the CSV file
df = pd.read_csv(raw_csv_path)

# Drop completely empty rows/columns
df.dropna(how='all', inplace=True)
df.dropna(axis=1, how='all', inplace=True)

# Trim whitespace from headers and string values
df.columns = df.columns.str.strip()
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.strip()

# Drop unnecessary columns (adjust as needed)
columns_to_drop = [col for col in df.columns if 'shape' in col.lower() or 'fid' in col.lower()]
df.drop(columns=columns_to_drop, inplace=True)

# Convert date columns
for col in df.columns:
    if 'date' in col.lower():
        try:
            df[col] = pd.to_datetime(df[col])
        except:
            pass

# Convert numeric columns (e.g., area, coordinates)
for col in df.columns:
    if 'area' in col.lower() or 'size' in col.lower():
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove duplicates
df.drop_duplicates(inplace=True)

# Optional: Rename columns
df.rename(columns={
    'title_no': 'title_number',
    # Add more renames here if needed
}, inplace=True)

# Save the cleaned version
df.to_csv(cleaned_csv_path, index=False)
print(f"Cleaned data saved to: {cleaned_csv_path}")
