import pandas as pd
import pytest

# Import the functions under test
from backend.data_processing.cleaner import clean_data, prepare_features
from backend.Machine_Learning_Model import rental_price_model as rpm

# clean_data() tests (clean + normalise)
def test_clean_data_standardises_columns_and_parses_numeric():
    raw = pd.DataFrame({
        "Weekly Rent ($NZD)": ["$720", "  650 NZD  ", None],
        "Floor Area (m2)": ["90 m2", "abc", "120"],
        "Bedrooms": ["3", "two", 4],
        "Bathrooms": [2, " 1 ", "??"],
        "Suburb": ["  epsom  ", None, "Mt  roskill "],
        "Irrelevant": [None, None, None],  # ensure thresh drop keeps some rows
    })

    cleaned = clean_data(raw)

    # column names normalised
    assert {"rent_price", "floor_area", "bedrooms", "bathrooms", "suburb"} <= set(cleaned.columns)

    # numerics parsed
    assert cleaned["rent_price"].dtype.kind in ("f", "i")
    assert cleaned["floor_area"].dtype.kind in ("f", "i")
    assert cleaned["bedrooms"].dtype.kind in ("f", "i")
    assert cleaned["bathrooms"].dtype.kind in ("f", "i")

    # suburb normalised to Title Case, missing filled then title-cased
    assert all(isinstance(s, str) for s in cleaned["suburb"])
    assert all(s == s.title() for s in cleaned["suburb"])

    # obvious junk removed from numerics by coercion/fillna(0)
    for col in ["bedrooms", "bathrooms", "floor_area", "rent_price"]:
        assert not cleaned[col].astype(str).str.contains(r"[a-zA-Z?]").any()


def test_clean_data_drops_rows_with_too_many_missing_values():
    # Create a row that is mostly NaN to trigger the 70% threshold drop
    mostly_nan = {"Weekly Rent ($NZD)": None, "Floor Area (m2)": None, "Bedrooms": None,
                  "Bathrooms": None, "Suburb": None}
    ok_row = {"Weekly Rent ($NZD)": "500", "Floor Area (m2)": "80", "Bedrooms": "2",
              "Bathrooms": "1", "Suburb": "Epsom"}

    df = pd.DataFrame([mostly_nan, ok_row])
    cleaned = clean_data(df)
    # Only the OK row should survive
    assert len(cleaned) == 1
    assert cleaned["suburb"].iloc[0] == "Epsom"


# prepare_features() tests (validation + encoding)
def test_prepare_features_filters_invalid_suburbs_and_encodes_dynamically():
    raw = pd.DataFrame({
        "bedrooms": [3, 2, 4, 3],
        "bathrooms": [2, 1, 2, 1],
        "floor_area": [90, 70, 110, 85],
        "suburb": ["  epsom ", "??", "Manurewa", "Unknown"],  # invalid tokens present
    })

    features = prepare_features(raw)

    # 'suburb' text column should be replaced by dummies
    assert "suburb" not in features.columns
    suburb_dummy_cols = [c for c in features.columns if c.startswith("suburb_")]
    assert len(suburb_dummy_cols) >= 1

    # Invalid tokens removed (rows with "??" and "Unknown" drop out)
    # So remaining dummies should reflect only valid suburbs seen
    assert all(x in {"suburb_Epsom", "suburb_Manurewa"} for x in suburb_dummy_cols)

    # Dummies are numeric and 0/1
    for c in suburb_dummy_cols:
        assert pd.api.types.is_numeric_dtype(features[c])
        assert set(features[c].dropna().astype(int).unique()).issubset({0, 1})

    # Numeric fields stay numeric
    for col in ["bedrooms", "bathrooms", "floor_area"]:
        assert pd.api.types.is_numeric_dtype(features[col])


def test_prepare_features_respects_valid_suburbs_filter():
    raw = pd.DataFrame({
        "bedrooms": [2, 3],
        "bathrooms": [1, 2],
        "floor_area": [70, 95],
        "suburb": ["Kumeu", "Waiuku"],
    })

    # Only allow Kumeu to Waiuku row should be filtered out
    feats = prepare_features(raw, valid_suburbs=["Kumeu"])
    cols = [c for c in feats.columns if c.startswith("suburb_")]
    assert any("Kumeu" in c for c in cols)
    assert not any("Waiuku" in c for c in cols)
    # and only one row remains
    assert len(feats) == 1


# rental_price_model.prepare_input_dataframe() integration
class _FakeInput:
    def __init__(self, **k):
        self._k = k
    def dict(self):
        return self._k


def test_prepare_input_dataframe_uses_dynamic_columns_and_default_floor_area(monkeypatch):
    # Pretend training used these two suburb dummies
    monkeypatch.setattr(
        rpm, "get_model_suburb_columns_from_data",
        lambda: ["suburb_Epsom", "suburb_Manurewa"]
    )

    # Missing floor_area on purpose to test default=100 in rental_price_model.prepare_input_dataframe
    payload = _FakeInput(bedrooms=3, bathrooms=2, suburb="Epsom")
    df = rpm.prepare_input_dataframe(payload)

    expected_cols = ["bedrooms", "bathrooms", "floor_area", "suburb_Epsom", "suburb_Manurewa"]
    assert list(df.columns) == expected_cols

    # floor_area defaulted to 100
    assert df.at[df.index[0], "floor_area"] == 100

    # Correct dummy set (Epsom=1, Manurewa=0 assuming drop_first not used here)
    assert df.at[df.index[0], "suburb_Epsom"] == 1
    assert df.at[df.index[0], "suburb_Manurewa"] == 0
