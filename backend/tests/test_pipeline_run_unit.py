# --- import shim so tests work from repo root or /backend ---
import sys, pathlib
BACKEND_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
# ------------------------------------------------------------

import io
import logging
import pandas as pd
from pathlib import Path

import pipeline_main as pm

def _xlsx_bytes(rows):
    df = pd.DataFrame(rows)
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    return buf.getvalue()

def test_pipeline_logs_and_continues(caplog, monkeypatch):
    # no-op DB to keep this a pure unit test
    monkeypatch.setattr("data_processing.loader.save_to_db", lambda df, mode="append": None, raising=True)

    rows = [
        {"Suburb": "CBD", "Weekly Rent ($NZD)": 800, "Days on Market": 7,  "Bedrooms": 2},
        {"Suburb": "CBD", "Weekly Rent ($NZD)": 800, "Days on Market": 14, "Bedrooms": 2},  # duplicate
        {"Suburb": "CBD", "Weekly Rent ($NZD)": "oops", "Days on Market": 7, "Bedrooms": 2}, # invalid
    ]
    raw = _xlsx_bytes(rows)

    with caplog.at_level(logging.INFO):
        out = pm.run(raw)

    sc = out["stage_counts"]
    # should not crash; should produce report because issues exist
    assert sc["ingested"] == 3
    assert sc["validated_ok"] >= 1 and sc["rejected"] >= 1
    assert isinstance(out["report_path"], str) and Path(out["report_path"]).exists()

    joined = " ".join(r.getMessage().lower() for r in caplog.records)
    assert "pipeline_run" in joined or "validate" in joined or "duplicate" in joined
