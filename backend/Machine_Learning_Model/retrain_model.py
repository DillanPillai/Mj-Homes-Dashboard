import os
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def retrain_rent_model():
    try:
        # Path to the Excel dataset
        file_path = os.path.join(os.getcwd(), "MockData.xlsx")
        if not os.path.exists(file_path):
            return "Error: MockData.xlsx not found."

        # Load dataset
        df = pd.read_excel(file_path, engine='openpyxl')

        # Required columns
        required_cols = ['Bedrooms', 'Bathrooms', 'Suburb', 'Weekly Rent ($NZD)']
        if not all(col in df.columns for col in required_cols):
            return "Error: One or more required columns are missing from the Excel file."

        # Rename to standard lowercase
        df.rename(columns={
            'Bedrooms': 'bedrooms',
            'Bathrooms': 'bathrooms',
            'Suburb': 'suburb',
            'Weekly Rent ($NZD)': 'rent_price'
        }, inplace=True)

        # Drop rows with missing data
        df.dropna(subset=['bedrooms', 'bathrooms', 'rent_price', 'suburb'], inplace=True)

        # Assign default floor_area
        df['floor_area'] = 100

        # One-hot encode suburb column dynamically
        df = pd.get_dummies(df, columns=['suburb'])

        # Prepare features and target
        feature_cols = ['bedrooms', 'bathrooms', 'floor_area'] + [col for col in df.columns if col.startswith('suburb_')]
        X = df[feature_cols]
        y = df['rent_price']

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Evaluate
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)

        # Save model
        model_path = os.path.join("backend", "Machine_Learning_Model", "rental_model.pkl")
        joblib.dump(model, model_path)

        return f"Model retrained and saved successfully! MSE: {mse:.2f}"

    except Exception as e:
        return f"Retraining failed: {str(e)}"
