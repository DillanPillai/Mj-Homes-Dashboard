import os
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

MODEL_PATH = os.path.join("backend", "Machine_Learning_Model", "rental_model.pkl")
DATA_PATH = os.path.join("backend", "data_processing", "MockData.xlsx")

def retrain_rent_model():
    try:
        if not os.path.exists(DATA_PATH):
            return "Error: MockData.xlsx not found."

        # Load dataset
        df = pd.read_excel(DATA_PATH, engine='openpyxl')

        # Validate expected columns
        required_cols = ['Bedrooms', 'Bathrooms', 'Suburb', 'Weekly Rent ($NZD)']
        if not all(col in df.columns for col in required_cols):
            return "Error: One or more required columns are missing from the Excel file."

        # Standardise column names
        df.rename(columns={
            'Bedrooms': 'bedrooms',
            'Bathrooms': 'bathrooms',
            'Suburb': 'suburb',
            'Weekly Rent ($NZD)': 'rent_price'
        }, inplace=True)

        # Drop rows with missing values
        df.dropna(subset=['bedrooms', 'bathrooms', 'rent_price', 'suburb'], inplace=True)

        # Add placeholder 'floor_area' if not present
        df['floor_area'] = 100

        # One-hot encode suburbs
        df = pd.get_dummies(df, columns=['suburb'], prefix='suburb')

        # Features and target
        X = df.drop(columns=['rent_price'])
        y = df['rent_price']

        # Split dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Evaluate
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)

        # Save model
        joblib.dump(model, MODEL_PATH)

        return f"Model retrained and saved. MSE: {mse:.2f}"

    except Exception as e:
        return f"Retraining failed: {str(e)}"
