# --- import shim so tests work from repo root or /backend ---
import sys, pathlib
BACKEND_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
# ------------------------------------------------------------

import io
import pandas as pd
import pytest

try:
    from data_processing.loader import load_from_bytes
except Exception:
    load_from_bytes = None

@pytest.mark.skipif(load_from_bytes is None, reason="loader.load_from_bytes not exposed")
def test_loader_accepts_xlsx_and_normalises_headers():
    df = pd.DataFrame([{" Suburb ": "Epsom", "Weekly Rent ($NZD)": 900, "Days on Market": 3, "Bedrooms": 3}])
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    out = load_from_bytes(buf.getvalue())
    assert list(out.columns) == ["Suburb", "Weekly Rent ($NZD)", "Days on Market", "Bedrooms"]
    assert out.shape[0] == 1
