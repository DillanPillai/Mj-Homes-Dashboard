import os
from pathlib import Path
import joblib
import pandas as pd

# Robust import for cleaner.prepare_features
try:
    # when CWD is backend
    from data_processing.cleaner import prepare_features  # type: ignore
except ModuleNotFoundError:
    # when CWD is repo root
    from backend.data_processing.cleaner import prepare_features  # type: ignore

# Paths resolved relative to this file so CWD doesn't matter
_THIS_DIR = Path(__file__).resolve().parent                         # .../backend/Machine_Learning_Model
_BACKEND_DIR = _THIS_DIR.parent                                     # .../backend
_DATA_DIR = _BACKEND_DIR / "data_processing"                        # .../backend/data_processing
_MODEL_PATH = _THIS_DIR / "rental_model.pkl"                        # .../backend/Machine_Learning_Model/rental_model.pkl


def _pick_dataset_path() -> Path | None:
    """
    Choose MockData.xlsx or MockData.csv from data_processing (prefer the most
    recently modified file). This keeps prediction in sync with retraining.
    """
    xlsx = _DATA_DIR / "MockData.xlsx"
    csvp = _DATA_DIR / "MockData.csv"

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


def load_model():
    """
    Load the trained model from disk (returns None if it doesn't exist).
    """
    if not _MODEL_PATH.exists():
        return None
    return joblib.load(_MODEL_PATH)


def get_model_suburb_columns_from_data() -> list[str]:
    """
    Dynamically infer the one-hot suburb columns from the current dataset.
    This mirrors how training derived its dummy columns so prediction aligns.
    """
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
        # Keep this silent-ish for production; tests can monkeypatch
        print(f"[ERROR] Failed to extract suburb columns: {e}")
        return []


def prepare_input_dataframe(input_data) -> pd.DataFrame:
    """
    Convert incoming Pydantic model (or dict-like) into a model-compatible DataFrame:
    - ensures floor_area default (100) if missing
    - cleans/validates/encodes suburb using prepare_features()
    - reindexes columns to exactly match the training feature order
    """
    # Pydantic model compatibility
    payload = input_data.dict() if hasattr(input_data, "dict") else dict(input_data)
    df = pd.DataFrame([payload])

    # Assign default floor_area if missing
    if "floor_area" not in df.columns:
        df["floor_area"] = 100

    # Columns used during training, derived from current dataset (csv/xlsx)
    all_suburb_columns = get_model_suburb_columns_from_data()
    suburb_names = [col.replace("suburb_", "") for col in all_suburb_columns]

    # Clean/normalise/one-hot the input the same way as in training
    df = prepare_features(df, valid_suburbs=suburb_names)

    # Match training column order exactly
    expected_columns = ["bedrooms", "bathrooms", "floor_area"] + all_suburb_columns
    df = df.reindex(columns=expected_columns, fill_value=0)

    return df
