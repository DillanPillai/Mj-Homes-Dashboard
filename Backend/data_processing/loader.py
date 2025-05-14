# backend/data_processing/loader.py

import sqlite3
import pandas as pd

def save_to_db(data):
    df = pd.DataFrame(data)
    conn = sqlite3.connect('data/processed/mjhome.db')
    df.to_sql("listings", conn, if_exists="replace", index=False)
    conn.close()
    print("Data saved to SQLite database.")
