import os
import joblib
import pandas as pd

# Load the trained rental model from disk
def load_model():
    model_path = os.path.join("backend", "Machine_Learning_Model", "rental_model.pkl")
    if not os.path.exists(model_path):
        return None
    return joblib.load(model_path)

# Prepare the input for prediction
def prepare_input_dataframe(input_data):
    """
    Converts input JSON into a one-hot encoded DataFrame
    to match the model's expected input format.
    """
    # Convert to DataFrame
    df = pd.DataFrame([input_data.dict()])

    # Add default floor_area if missing
    if 'floor_area' not in df.columns:
        df['floor_area'] = 100

    # Match model training suburb columns
    for suburb_col in get_model_suburb_columns():
        df[suburb_col] = 1 if f"suburb_{df['suburb'][0]}" == suburb_col else 0

    # Drop original suburb
    df.drop(columns=['suburb'], inplace=True)

    return df

# List of suburbs used in model training (based on training data)
def get_model_suburb_columns():
    return [
        'suburb_Auckland Central Business District',
        'suburb_Birkenhead',
        'suburb_Epsom',
        'suburb_Glenfield',
        'suburb_Henderson',
        'suburb_Manukau',
        'suburb_Mt Roskill',
        'suburb_New Lynn',
        'suburb_Pakuranga',
        'suburb_Remuera',
        'suburb_Takapuna'
    ]
