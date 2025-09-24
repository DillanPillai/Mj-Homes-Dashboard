from __future__ import annotations

from typing import Union, List
import pandas as pd

# Use the shared model helpers (consistent encoding & column order)
from Machine_Learning_Model import rental_price_model as rpm

# Simple cache so we don't reload the model on every call
_model_cache = None


def _get_model():
    """Lazy-load and cache the trained model."""
    global _model_cache
    if _model_cache is None:
        _model_cache = rpm.load_model()
    return _model_cache


def predict_rent(data: Union[pd.DataFrame, dict]) -> pd.DataFrame:
    """
    Predict rent for:
      - a pandas DataFrame with columns: bedrooms, bathrooms, floor_area, suburb
        (adds a 'predicted_rent' column and returns the same DataFrame), OR
      - a dict with those keys (returns a single-row DataFrame with prediction).

    This function delegates encoding/column-order logic to
    Machine_Learning_Model.rental_price_model.prepare_input_dataframe
    to keep behavior consistent across training/prediction.
    """
    model = _get_model()
    if model is None:
        raise RuntimeError(
            "Model not found. Please call /retrain-model to generate "
            "Machine_Learning_Model/rental_model.pkl first."
        )

    # If a dict was provided, convert to a one-row DataFrame
    if isinstance(data, dict):
        data = pd.DataFrame([data])

    if not isinstance(data, pd.DataFrame):
        raise TypeError("predict_rent expects a pandas DataFrame or a dict.")

    required_cols = {"bedrooms", "bathrooms", "floor_area", "suburb"}
    missing = required_cols - set(map(str.lower, data.columns))
    # Be permissive about column case by normalizing a copy
    # (keeps original DataFrame intact for the returned value)
    normalized = data.copy()
    normalized.columns = [c.lower() for c in normalized.columns]

    if missing:
        raise ValueError(
            f"Missing required input columns: {', '.join(sorted(missing))}. "
            f"Expected: {', '.join(sorted(required_cols))}"
        )

    # Row-wise prediction so we can reuse your canonical preparation function
    preds: List[float] = []
    for row in normalized.to_dict(orient="records"):
        # Build the expected pydantic-like object for prepare_input_dataframe
        class _Shim:
            def __init__(self, d):  # minimal shim to match your RentalInput fields
                self.bedrooms = int(d["bedrooms"])
                self.bathrooms = int(d["bathrooms"])
                self.floor_area = float(d["floor_area"])
                self.suburb = str(d["suburb"])

            def dict(self):
                return {
                    "bedrooms": self.bedrooms,
                    "bathrooms": self.bathrooms,
                    "floor_area": self.floor_area,
                    "suburb": self.suburb,
                }

        shim = _Shim(row)
        X = rpm.prepare_input_dataframe(shim)
        yhat = float(model.predict(X)[0])
        preds.append(yhat)

    # Attach predictions to the original (unmodified) DataFrame shape
    data = data.copy()
    data["predicted_rent"] = preds
    return data
