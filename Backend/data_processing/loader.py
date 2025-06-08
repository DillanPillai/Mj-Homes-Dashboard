import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection config
DB_NAME = "mjhome"
DB_USER = "postgres"
DB_PASSWORD = "pass123"  # <- enter your actual password here
DB_HOST = "localhost"
DB_PORT = "5432"

def save_to_db(data: pd.DataFrame):
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        data.to_sql("properties", engine, if_exists="replace", index=False)
        print("✅ Data saved to PostgreSQL successfully.")
    except Exception as e:
        print("❌ Error saving to PostgreSQL:", e)
