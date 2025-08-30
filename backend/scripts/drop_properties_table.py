from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables (DB URL etc.)
load_dotenv("backend/.env")

# Connect to database
engine = create_engine(os.environ["DATABASE_URL"])

# Drop table safely
with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS properties;"))

print("Dropped properties table.")
