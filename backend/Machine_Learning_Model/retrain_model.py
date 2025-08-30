# backend/Machine_Learning_Model/retrain_model.py
import os
from pathlib import Path
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def _pick_dataset_path() -> Path | None:
    """
    Look for MockData.xlsx or MockData.csv under backend/data_processing.
    If both exist, use the one most recently modified.
    """
    data_dir = Path("data_processing")
    xlsx = data_dir / "MockData.xlsx"
    csvp = data_dir / "MockData.csv"

    if xlsx.exists() and csvp.exists():
        return xlsx if xlsx.stat().st_mtime >= csvp.stat().st_mtime else csvp
    if xlsx.exists():
        return xlsx
    if csvp.exists():
        return csvp
    return None


def _load_dataset(path: Path) -> pd.DataFrame:
    """
    Load the dataset from CSV or XLSX based on the file extension.
    """
    ext = path.suffix.lower()
    if ext == ".csv":
        return pd.read_csv(path)
    if ext == ".xlsx":
        return pd.read_excel(path)  # openpyxl is auto-picked
    raise ValueError(f"Unsupported dataset extension: {ext}")


def retrain_rent_model():
    """
    Retrain the rental price model using the most recent MockData.(xlsx|csv).
    Accepts either format without changing the upload flow.
    """
    try:
        src_path = _pick_dataset_path()
        if not src_path:
            return "Error: Neither MockData.xlsx nor MockData.csv found in data_processing/."

        # Load dataset
        df = _load_dataset(src_path)

        # Required columns
        required_cols = ['Bedrooms', 'Bathrooms', 'Suburb', 'Weekly Rent ($NZD)']
        if not all(col in df.columns for col in required_cols):
            return (
                "Error: One or more required columns are missing from the dataset. "
                "Expected: Bedrooms, Bathrooms, Suburb, Weekly Rent ($NZD)."
            )

        # Standardize column names
        df = df.copy()
        df.rename(
            columns={
                'Bedrooms': 'bedrooms',
                'Bathrooms': 'bathrooms',
                'Suburb': 'suburb',
                'Weekly Rent ($NZD)': 'rent_price',
            },
            inplace=True,
        )

        # Clean rows
        df.dropna(subset=['bedrooms', 'bathrooms', 'rent_price', 'suburb'], inplace=True)

        # Provide default floor_area if missing
        if 'floor_area' not in df.columns:
            df['floor_area'] = 100

        # One-hot encode suburbs dynamically
        df = pd.get_dummies(df, columns=['suburb'])

        # Features and target
        feature_cols = ['bedrooms', 'bathrooms', 'floor_area'] + [
            c for c in df.columns if c.startswith('suburb_')
        ]
        X = df[feature_cols]
        y = df['rent_price']

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Evaluate
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)

        # Save model
        model_path = Path(__file__).with_name("rental_model.pkl")
        joblib.dump(model, model_path)

        return f"Model retrained and saved successfully! MSE: {mse:.2f} (source: {src_path.name})"

    except Exception as e:
        return f"Retraining failed: {str(e)}"
