import os
import joblib
import pandas as pd

# Constants
MODEL_PATH = os.path.join("Machine_Learning_Model", "rental_model.pkl")
DATA_PATH = os.path.join("data_processing", "MockData.xlsx")


# Load the trained model from disk
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)

# Load all suburb columns from the dataset to match one-hot encoding
def get_model_suburb_columns():
    try:
        df = pd.read_excel(DATA_PATH, engine="openpyxl")
        if 'Suburb' not in df.columns:
            return []

        # Clean column and drop NA
        suburbs = df['Suburb'].dropna().unique()
        return sorted([f"suburb_{s.strip()}" for s in suburbs])
    except Exception as e:
        print(f"[ERROR] Failed to load suburbs: {e}")
        return []

# Convert incoming input into a model-compatible DataFrame
def prepare_input_dataframe(input_data):
    df = pd.DataFrame([input_data.dict()])

    # Handle missing floor_area
    if 'floor_area' not in df.columns:
        df['floor_area'] = 100

    # One-hot encode suburb using training-time format
    all_suburb_columns = get_model_suburb_columns()
    current_suburb = df['suburb'][0]

    for col in all_suburb_columns:
        suburb_name = col.replace("suburb_", "")
        df[col] = 1 if current_suburb == suburb_name else 0

    # Drop original suburb
    df.drop(columns=["suburb"], inplace=True)

    return df
