import os
import joblib
import pandas as pd
from pathlib import Path

from data_processing.cleaner import prepare_features

# Trained model path
MODEL_PATH = os.path.join("Machine_Learning_Model", "rental_model.pkl")


def _pick_dataset_path() -> Path | None:
    """
    Choose MockData.xlsx or MockData.csv from data_processing (prefer the most
    recently modified file). This keeps prediction in sync with retraining.
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


def _read_dataset(path: Path) -> pd.DataFrame:
    ext = path.suffix.lower()
    if ext == ".xlsx":
        return pd.read_excel(path)
    if ext == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported dataset extension: {ext}")


# Load the trained model from disk
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)


# Dynamically extract the suburb one-hot columns used during training
def get_model_suburb_columns_from_data():
    try:
        ds = _pick_dataset_path()
        if not ds:
            return []

        df = _read_dataset(ds)
        if "Suburb" not in df.columns:
            return []

        # Clean & normalize suburb names before building dummies
        df = df.dropna(subset=["Suburb"]).copy()
        df["Suburb"] = df["Suburb"].astype(str).str.strip().str.title()

        suburb_dummies = pd.get_dummies(df["Suburb"], prefix="suburb")
        return sorted(suburb_dummies.columns.tolist())
    except Exception as e:
        print(f"[ERROR] Failed to extract suburb columns: {e}")
        return []


# Convert incoming input into a model-compatible DataFrame
def prepare_input_dataframe(input_data):
    df = pd.DataFrame([input_data.dict()])

    # Assign default floor_area if missing
    if "floor_area" not in df.columns:
        df["floor_area"] = 100

    # Columns used during training, derived from current dataset (csv/xlsx)
    all_suburb_columns = get_model_suburb_columns_from_data()
    suburb_names = [col.replace("suburb_", "") for col in all_suburb_columns]

    # Clean/normalize/one-hot the input the same way as in training
    df = prepare_features(df, valid_suburbs=suburb_names)

    # Match training column order exactly
    expected_columns = ["bedrooms", "bathrooms", "floor_area"] + all_suburb_columns
    df = df.reindex(columns=expected_columns, fill_value=0)

    return df
