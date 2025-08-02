import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import os

def retrain_rent_model():
    try:
        # Load Excel data
        file_path = './Backend/data_processing/MockData.xlsx'
        if not os.path.exists(file_path):
            return "Error: MockData.xlsx not found."

        df = pd.read_excel(file_path)

        # Rename columns to match model requirements
        df.rename(columns={
            'Bedrooms': 'bedrooms',
            'Bathrooms': 'bathrooms',
            'Suburb': 'suburb',
            'Weekly Rent ($NZD)': 'rent_price'
        }, inplace=True)

        # Drop missing rows
        df.dropna(subset=['bedrooms', 'bathrooms', 'rent_price', 'suburb'], inplace=True)

        # Add placeholder for floor area
        df['floor_area'] = 100

        # One-hot encode suburb
        df = pd.get_dummies(df, columns=['suburb'], drop_first=True)

        # Features & target
        X = df[['bedrooms', 'bathrooms', 'floor_area'] + [col for col in df.columns if col.startswith('suburb_')]]
        y = df['rent_price']

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Evaluate model
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)

        # Save model
        model_path = './Backend/Machine_Learning_Model/rental_model.pkl'
        joblib.dump(model, model_path)

        return f"Model retrained and saved successfully! MSE: {mse:.2f}"

    except Exception as e:
        return f"Retraining failed: {str(e)}"