import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# Prefer DATABASE_URL if present, else build from individual pieces
DATABASE_URL = os.getenv("DATABASE_URL")

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")


def _engine():
    """
    Create and return a SQLAlchemy engine for PostgreSQL.
    Tries DATABASE_URL first, else uses DB_* pieces.
    """
    if DATABASE_URL:
        print("[loader] Using DATABASE_URL for DB connection")
        return create_engine(DATABASE_URL)

    if DB_NAME and DB_USER and DB_PASSWORD:
        print("[loader] Using DB_NAME/DB_USER/DB_PASSWORD for DB connection")
        return create_engine(
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    raise RuntimeError(
        "Database connection settings missing. Please set DATABASE_URL or DB_NAME/DB_USER/DB_PASSWORD."
    )


def save_to_db(data: pd.DataFrame, *, mode: str = "append"):
    """
    Save a DataFrame to the 'properties' table in PostgreSQL.

    Args:
        data (pd.DataFrame): Data to store.
        mode (str): 'append' (default) to add rows, or 'replace' to overwrite table.
    """
    try:
        engine = _engine()
        data.to_sql("properties", engine, if_exists=mode, index=False)
        print(f"Data saved to PostgreSQL successfully (mode={mode}).")
    except Exception as e:
        print("Error saving to PostgreSQL:", e)


def fetch_processed_data(limit: int = 100):
    """
    Fetch rows from the 'properties' table for inspection or API use.

    Args:
        limit (int): Maximum number of rows to fetch (default=100).

    Returns:
        list[dict]: List of property rows as dictionaries.
    """
    try:
        engine = _engine()
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM properties LIMIT {limit};"))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df.to_dict(orient="records")
    except Exception as e:
        print("Error fetching data from PostgreSQL:", e)
        return []
