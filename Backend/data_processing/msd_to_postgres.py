# Import necessary libraries
import os                      # For interacting with the file system
import pandas as pd            # For reading and manipulating CSV data
from sqlalchemy import create_engine  # For connecting to PostgreSQL
from dotenv import load_dotenv        # For loading environment variables from .env file

# Load environment variables (DB credentials) from the .env file
load_dotenv()

# Fetch database credentials from the environment variables
DB_HOST = os.getenv("DB_HOST")         # Hostname of the PostgreSQL server
DB_PORT = os.getenv("DB_PORT")         # Port number of PostgreSQL
DB_NAME = os.getenv("DB_NAME")         # Name of the target database
DB_USER = os.getenv("DB_USER")         # Database username
DB_PASSWORD = os.getenv("DB_PASSWORD") # Database password

# Name of the PostgreSQL table to insert the data into
TABLE_NAME = "msd_housing_reports"

# Directory where the cleaned MSD CSV files are stored
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEANED_DIR = os.path.join(BASE_DIR, "..", "..", "Data", "MSD", "cleaned")
CLEANED_DIR = os.path.normpath(CLEANED_DIR)


def connect_to_db():
    """
    Establish a connection to the PostgreSQL database using SQLAlchemy.
    Returns a SQLAlchemy engine instance.
    """
    db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(db_url)

def insert_cleaned_data():
    """
    Reads all cleaned CSV files from the CLEANED_DIR and inserts their contents
    into the specified PostgreSQL table.
    """
    engine = connect_to_db()  # Connect to the database

    # Loop through all files in the cleaned data directory
    for filename in os.listdir(CLEANED_DIR):
        # Process only CSV files
        if filename.endswith(".csv"):
            file_path = os.path.join(CLEANED_DIR, filename)
            try:
                # Read CSV into a DataFrame
                df = pd.read_csv(file_path, skiprows=6)

                # Drop unnamed columns or clean up headers
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                df.dropna(how='all', inplace=True)  # Drop any fully empty rows

                print(df.head())  # Optional: Check column names



                # Insert the DataFrame into the PostgreSQL table
                df.to_sql(TABLE_NAME, con=engine, if_exists="append", index=False)
                print(f"[INSERTED] {filename} → {TABLE_NAME}")

            except Exception as e:
                # Handle any issues during insertion (e.g., bad format, DB errors)
                print(f"[ERROR] Could not insert {filename}: {e}")

if __name__ == "__main__":
    # Start the script
    print("=== Inserting Cleaned MSD Data into PostgreSQL ===")
    insert_cleaned_data()
    print("=== Done ===")
