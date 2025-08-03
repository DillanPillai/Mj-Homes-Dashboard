import os
import psycopg2
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Prints the loaded values for debugging
print("Loaded values:")
print("DB_NAME:", os.getenv("DB_NAME"))
print("DB_USER:", os.getenv("DB_USER"))
print("DB_HOST:", os.getenv("DB_HOST"))

try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    print("Connected to PostgreSQL database successfully!")
    conn.close()

except Exception as e:
    print("Failed to connect to the database.")
    print("Error:", e)
