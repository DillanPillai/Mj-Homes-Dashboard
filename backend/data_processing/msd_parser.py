import os
import pandas as pd

# Input directory: where MSD Excel files are downloaded
INPUT_DIR = os.path.join("..", "..", "Data", "MSD")

# Output directory: where cleaned CSVs will be stored
OUTPUT_DIR = os.path.join(INPUT_DIR, "cleaned")
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Create if not exists

def clean_excel_files():
    """
    Scans all Excel files in the INPUT_DIR,
    removes empty rows/columns, normalizes headers,
    and saves cleaned versions as CSVs.
    """
    # Loop through all files in the input directory
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".xls") or filename.endswith(".xlsx"):
            file_path = os.path.join(INPUT_DIR, filename)

            try:
                # Read the Excel file into a DataFrame
                df = pd.read_excel(file_path)

                # Drop completely empty rows and columns
                df.dropna(axis=0, how='all', inplace=True)
                df.dropna(axis=1, how='all', inplace=True)

                # Normalize column names: lowercase, strip whitespace
                df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]

                # Save cleaned data to CSV with a matching name
                cleaned_filename = f"cleaned_{os.path.splitext(filename)[0]}.csv"
                cleaned_path = os.path.join(OUTPUT_DIR, cleaned_filename)
                df.to_csv(cleaned_path, index=False)

                print(f"[CLEANED] {filename} → {cleaned_filename}")

            except Exception as e:
                print(f"[ERROR] Failed to process {filename}: {e}")

if __name__ == "__main__":
    print("=== Cleaning MSD Excel Files ===")
    clean_excel_files()
    print("=== Cleaning Complete ===")
