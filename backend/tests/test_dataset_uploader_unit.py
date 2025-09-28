from pathlib import Path
import sys
import io
import pandas as pd
import pytest
from sqlalchemy import create_engine

# Robust import so this test runs from repo root
ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
for p in (str(ROOT), str(BACKEND)):
    if p not in sys.path:
        sys.path.insert(0, p)

import backend.data_processing.dataset_uploader as du

def test__load_to_df_csv_and_normalise():
    df0 = pd.DataFrame({" A ": [1, 2], "B-b": [" x ", "y "]})
    csv_bytes = df0.to_csv(index=False).encode("utf-8")

    df = du._load_to_df(csv_bytes, "x.csv", "text/csv")
    df = du._clean_and_standardize(df)

    assert list(df.columns) == ["a", "b_b"]
    assert df["a"].tolist() == [1, 2]
    assert df["b_b"].tolist() == ["x", "y"]

@pytest.mark.skipif(pytest.importorskip("bs4") is None, reason="bs4 not installed for HTML parsing")
def test__load_to_df_html_picks_largest():
    small = pd.DataFrame({"a": [1]})
    big = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    html = small.to_html(index=False) + big.to_html(index=False)
    df = du._load_to_df(html.encode("utf-8"), "x.html", "text/html")
    assert df.shape == big.shape  # picks largest non-empty table

def test_add_hashes_unique_and_repeatable():
    df = pd.DataFrame({"x": [1, 1], "y": ["a", "a"]})
    h = du.add_hashes(df)
    assert "_row_hash" in h.columns
    assert h["_row_hash"].nunique() == 1  # identical rows -> identical hashes

def test_ensure_table_and_insert_unique_sqlite(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path/'t.db'}", future=True)
    table = du.ensure_table(engine)

    df = pd.DataFrame({"col": [1, 2, 2, 3]})
    df = du._clean_and_standardize(df)
    dfh = du.add_hashes(df)

    inserted = du.insert_unique_rows(engine, table, dfh)
    assert inserted == 3

    inserted2 = du.insert_unique_rows(engine, table, dfh)
    assert inserted2 == 0
