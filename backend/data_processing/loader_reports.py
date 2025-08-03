# Import standard and external libraries
import os                                 # For file path and environment handling
import pandas as pd                       # For data manipulation
from sqlalchemy import create_engine      # For database connection
from dotenv import load_dotenv            # To load environment variables from .env file

# Import the custom transform function for MSD reports
from transform_registers import transform_register_report


# Load environment variables from the .env file
load_dotenv()

# Retrieve database credentials and configuration from environment variables
DB_NAME = os.getenv("DB_NAME")            # Name of the database (e.g., mjhome)
DB_USER = os.getenv("DB_USER")            # Database username (e.g., postgres)
DB_PASSWORD = os.getenv("DB_PASSWORD")    # Database password
DB_HOST = os.getenv("DB_HOST", "localhost")  # Database host (default: localhost)
DB_PORT = os.getenv("DB_PORT", "5432")       # Database port (default: 5432)

# Create a SQLAlchemy database engine for connecting to PostgreSQL
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def save_msd_report(file_path: str):
    """
    Reads a cleaned MSD monthly report CSV, transforms it into row-based format,
    and inserts the data into the 'housing_reports' table in PostgreSQL.

    Args:
        file_path (str): Full path to the cleaned CSV file.
    """
    try:
        # Transform the report from wide format (monthly columns) to long format
        df = transform_register_report(file_path)

        # Proceed only if the DataFrame has rows
        if not df.empty:
            # Append the data into the existing housing_reports table
            df.to_sql("housing_reports", engine, if_exists="append", index=False)
            print(f"Inserted {len(df)} rows from {os.path.basename(file_path)}")
        else:
            # Inform if the DataFrame was empty and skipped
            print(f"Skipped empty report: {file_path}")

    except Exception as e:
        # Catch and print any exceptions during transformation or DB insertion
        print(f"Failed to insert {file_path}: {e}")
