# Import required libraries
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Retrieve DB credentials
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Define the path to the cleaned CSV file
csv_path = "cleaned_linz_property_titles.csv"

# Load the CSV into a pandas DataFrame
df = pd.read_csv(csv_path)

# Replace NaN values with None
df = df.where(pd.notnull(df), None)

# List of columns in the correct order matching the table schema
columns = [
    'id',
    'title_number',
    'status',
    'type',
    'land_district',
    'issue_date',
    'guarantee_status',
    'estate_description',
    'number_owners',
    'spatial_extents_shared'
]

# Validate CSV columns
missing = [col for col in columns if col not in df.columns]
if missing:
    raise ValueError(f"Missing columns in CSV file: {missing}")

# Reorder DataFrame columns to match PostgreSQL table
df = df[columns]

# Main function to create and populate the table
def insert_linz_data(df):
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    # Drop and recreate table
    cursor.execute("DROP TABLE IF EXISTS linz_properties CASCADE;")
    conn.commit()
    print("Dropped existing 'linz_properties' table (if any)")

    create_table_query = """
    CREATE TABLE IF NOT EXISTS linz_properties (
        id BIGINT PRIMARY KEY,
        title_number TEXT,
        status TEXT,
        "type" TEXT,
        land_district TEXT,
        issue_date TIMESTAMPTZ,
        guarantee_status TEXT,
        estate_description TEXT,
        number_owners INTEGER,
        spatial_extents_shared BOOLEAN
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    print("Table 'linz_properties' created or verified.")

    insert_query = f"""
        INSERT INTO linz_properties ({', '.join(['"' + col + '"' if col == 'type' else col for col in columns])})
        VALUES %s
        ON CONFLICT (id) DO NOTHING;
    """

    values = [tuple(row) for row in df.to_numpy()]
    print(f"Inserting {len(values)} rows into 'linz_properties'...")
    execute_values(cursor, insert_query, values)
    conn.commit()

    cursor.close()
    conn.close()
    print("Data inserted successfully into 'linz_properties'.")

# Run the script
if __name__ == "__main__":
    insert_linz_data(df)
