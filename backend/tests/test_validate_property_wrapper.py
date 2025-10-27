import sys, pathlib
BACKEND_DIR = pathlib.Path(__file__).resolve().parents[1]  # .../backend
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import pandas as pd
from services.ingest_properties import validate_property_dataframe

REQ = ["Suburb", "Weekly Rent ($NZD)", "Days on Market", "Bedrooms"]

def test_wrapper_shapes_return_and_counts():
    df = pd.DataFrame([
        {"Suburb": "Epsom", "Weekly Rent ($NZD)": 900, "Days on Market": 3, "Bedrooms": 3},
        {"Suburb": "Epsom", "Weekly Rent ($NZD)": 900, "Days on Market": 12, "Bedrooms": 3},  # duplicate
        {"Suburb": "CBD", "Weekly Rent ($NZD)": "600x", "Days on Market": 7, "Bedrooms": 2},  # invalid number
    ])

    out = validate_property_dataframe(df)
    assert set(out.keys()) == {"summary", "issues", "accepted_df"}
    assert set(out["summary"].keys()) == {"total", "accepted", "rejected", "duplicates"}
    assert isinstance(out["issues"], list)
    assert "dataframe" in str(type(out["accepted_df"])).lower()

    s = out["summary"]
    assert s["total"] == 3
    assert s["duplicates"] == 1
    assert s["accepted"] == 1   # only the first row
    assert s["rejected"] == 2
