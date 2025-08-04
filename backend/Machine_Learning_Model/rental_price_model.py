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

# Dynamically extract the suburb one-hot columns used during training
def get_model_suburb_columns_from_data():
    try:
        df = pd.read_excel(DATA_PATH, engine="openpyxl")
        if 'Suburb' not in df.columns:
            return []

        # Drop NA and strip spaces
        df = df.dropna(subset=["Suburb"])
        df['Suburb'] = df['Suburb'].astype(str).str.strip()

        # One-hot encode to get actual training columns
        suburb_dummies = pd.get_dummies(df['Suburb'], prefix="suburb")
        return sorted(suburb_dummies.columns.tolist())
    except Exception as e:
        print(f"[ERROR] Failed to extract suburb columns: {e}")
        return []

# Convert incoming input into a model-compatible DataFrame
def prepare_input_dataframe(input_data):
    df = pd.DataFrame([input_data.dict()])

    # Ensure floor_area is present
    if 'floor_area' not in df.columns:
        df['floor_area'] = 100

    # Suburb handling
    all_suburb_columns = get_model_suburb_columns_from_data()
    current_suburb = df['suburb'][0].strip()
    
    for col in all_suburb_columns:
        suburb_name = col.replace("suburb_", "")
        df[col] = 1 if current_suburb == suburb_name else 0

    # Drop original 'suburb' column
    df.drop(columns=["suburb"], inplace=True)

    # Ensure column order matches model training
    expected_columns = ['bedrooms', 'bathrooms', 'floor_area'] + all_suburb_columns
    df = df.reindex(columns=expected_columns, fill_value=0)

    return df
