import pandas as pd
import joblib

# Load trained model
model = joblib.load('./Backend/Machine_Learning_Model/rental_model.pkl')

def predict_rent(data: pd.DataFrame) -> pd.DataFrame:
    # Debug log (optional)
    print("Predictor input columns:", data.columns.tolist())

    # Only get dummies if suburb exists
    if 'suburb' in data.columns:
        input_data = pd.get_dummies(data, columns=['suburb'], drop_first=True)
    else:
        print("⚠️ Warning: 'suburb' column missing — skipping encoding")
        input_data = data.copy()

    # Match model's training features
    model_columns = model.feature_names_in_
    input_data = input_data.reindex(columns=model_columns, fill_value=0)

    # Predict and return result
    predictions = model.predict(input_data)
    data['predicted_rent'] = predictions
    return data
