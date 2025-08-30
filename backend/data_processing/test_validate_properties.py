# test_validate_properties.py
import pandas as pd
from validate_properties import validate_dataframe


def _sample_df():
    """Helper to generate a dataframe with known issues for testing."""
    return pd.DataFrame({
        "Suburb": ["Manurewa", None, "Epsom", "Epsom", "Epsom", "Epsom"],
        "Weekly Rent ($NZD)": ["650", "1800", "120000", "650", "700", "abc"],
        "Days on Market": [12, 5, 15, 12, 9999, 8],
        "Bedrooms": [3, 2, 4.5, 3, 2, 2],
    })


def test_required_fields_and_missing_values():
    df = _sample_df()
    _, issues, _ = validate_dataframe(df)
    assert any(i.code == "missing_required" and i.field == "Suburb" for i in issues)


def test_invalid_number_and_out_of_range():
    df = _sample_df()
    _, issues, _ = validate_dataframe(df)
    assert any(i.code == "invalid_number" and i.field == "Weekly Rent ($NZD)" for i in issues)  # 'abc'
    assert any(i.code == "out_of_range" and i.field == "Weekly Rent ($NZD)" for i in issues)   # 120000
    assert any(i.code == "out_of_range" and i.field == "Days on Market" for i in issues)       # 9999


def test_integer_check_for_bedrooms():
    df = _sample_df()
    _, issues, _ = validate_dataframe(df)
    assert any(i.code == "invalid_integer" and i.field == "Bedrooms" for i in issues)          # 4.5


def test_duplicate_detection():
    df = _sample_df()
    _, issues, summary = validate_dataframe(df)
    assert any(i.code == "duplicate" for i in issues)
    assert summary.duplicates >= 1


def test_persistence_behavior_counts():
    df = _sample_df()
    accepted, issues, summary = validate_dataframe(df)
    assert summary.total == len(df)
    assert summary.accepted + summary.rejected == summary.total
    assert len(accepted) < len(df)  # because some rows were rejected


def test_all_valid_rows_pass():
    df = pd.DataFrame({
        "Suburb": ["A", "B"],
        "Weekly Rent ($NZD)": [600, 620],
        "Days on Market": [10, 12],
        "Bedrooms": [2, 3],
    })
    accepted, issues, summary = validate_dataframe(df)
    assert len(issues) == 0
    assert summary.accepted == 2
    assert len(accepted) == 2
