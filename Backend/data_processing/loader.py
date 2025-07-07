import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

def save_to_db(data: pd.DataFrame):
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        data.to_sql("properties", engine, if_exists="replace", index=False)
        print("Data saved to PostgreSQL successfully.")
    except Exception as e:
        print("Error saving to PostgreSQL:", e)

def fetch_processed_data(limit=100):
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM properties LIMIT {limit};"))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df.to_dict(orient="records")
    except Exception as e:
        print("Error fetching data from PostgreSQL:", e)
        return []
