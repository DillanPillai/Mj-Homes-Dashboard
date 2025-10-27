import sys, pathlib
BACKEND_DIR = pathlib.Path(__file__).resolve().parents[1]  # .../backend
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
    
import pandas as pd

from data_processing.validate_properties import (
    validate_dataframe, RowIssue, ValidationSummary
)

REQ = ["Suburb", "Weekly Rent ($NZD)", "Days on Market", "Bedrooms"]

def DF(rows):
    return pd.DataFrame(rows, columns=REQ)

def test_missing_required_columns_rejects_all():
    # Drop "Bedrooms" on purpose
    df = pd.DataFrame([{"Suburb": "Albany", "Weekly Rent ($NZD)": 600, "Days on Market": 10}])
    accepted, issues, summary = validate_dataframe(df)

    assert accepted.empty
    assert any(i.code == "missing_column" and i.field == "Bedrooms" for i in issues)
    assert summary.total == 1
    assert summary.accepted == 0
    assert summary.rejected == 1
    assert summary.duplicates == 0

def test_missing_required_fields_in_rows():
    df = DF([
        ["Epsom", 900, 12, 3],      # OK
        ["Manurewa", None, 50, 3],  # missing rent
        [None, 520, 30, 2],         # missing suburb
        ["CBD", 700, None, 2],      # missing days
        ["CBD", 700, 15, None],     # missing bedrooms
    ])
    accepted, issues, summary = validate_dataframe(df)

    assert summary.total == 5
    assert summary.accepted == 1
    assert summary.rejected == 4
    assert any(i.code == "missing_required" and i.field == "Weekly Rent ($NZD)" for i in issues)
    assert any(i.code == "missing_required" and i.field == "Suburb" for i in issues)
    assert any(i.code == "missing_required" and i.field == "Days on Market" for i in issues)
    assert any(i.code == "missing_required" and i.field == "Bedrooms" for i in issues)

def test_numeric_coercion_and_invalid_number_and_integer_check():
    # "1,200" must coerce; "600x" should fail; Bedrooms 2.5 invalid_integer
    df = DF([
        ["Takapuna", "1,200", 7, 2],   # OK after coercion
        ["Takapuna", "600x", 7, 2],    # invalid rent
        ["Takapuna", 700, "seven", 2], # invalid days
        ["Takapuna", 700, 7, 2.5],     # invalid_integer bedrooms
    ])
    accepted, issues, summary = validate_dataframe(df)

    assert summary.total == 4
    assert summary.accepted == 1
    assert summary.rejected == 3
    assert any(i.code == "invalid_number" and i.field == "Weekly Rent ($NZD)" for i in issues)
    assert any(i.code == "invalid_number" and i.field == "Days on Market" for i in issues)
    assert any(i.code == "invalid_integer" and i.field == "Bedrooms" for i in issues)

def test_range_limits_out_of_range():
    # Limits: rent [100, 10000], days [0, 730], bedrooms [0, 12]
    df = DF([
        ["CBD", 150, 10, 1],        # OK
        ["CBD", 99, 10, 1],         # rent too low
        ["CBD", 10001, 10, 1],      # rent too high
        ["CBD", 500, -1, 1],        # days too low
        ["CBD", 500, 900, 1],       # days too high
        ["CBD", 500, 10, 13],       # bedrooms too high (will be out_of_range)
    ])
    accepted, issues, summary = validate_dataframe(df)

    assert summary.total == 6
    assert summary.accepted == 1
    assert summary.rejected == 5
    msgs = " | ".join(i.message.lower() for i in issues if i.code == "out_of_range")
    assert "weekly rent ($nzd)" in msgs or "days on market" in msgs or "bedrooms" in msgs

def test_infile_duplicates_are_flagged_and_rejected():
    # DUP_KEYS = ["Suburb", "Weekly Rent ($NZD)", "Bedrooms"]
    df = DF([
        ["Albany", 600, 14, 2],
        ["Albany", 600, 29, 2],   # duplicate by (Suburb, Rent, Bedrooms) despite different days
        ["Albany", 620, 14, 2],   # not a duplicate
    ])
    accepted, issues, summary = validate_dataframe(df)

    assert summary.total == 3
    assert summary.duplicates == 1
    assert summary.accepted == 2
    # the duplicate row should have a "duplicate" issue
    assert any(i.code == "duplicate" for i in issues)
