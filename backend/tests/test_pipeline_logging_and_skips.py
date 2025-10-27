# --- import shim so tests work from repo root or /backend ---
import sys, pathlib
BACKEND_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
# ------------------------------------------------------------

import io
import logging
from pathlib import Path
import pandas as pd

import pipeline_main as pm


def _xlsx_bytes(rows):
    df = pd.DataFrame(rows)
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    return buf.getvalue()


def test_pipeline_logs_and_continues_on_row_errors(caplog, monkeypatch):
    # no-op DB so the test stays pure/unit level
    monkeypatch.setattr("data_processing.loader.save_to_db", lambda df, mode="append": None, raising=True)

    # one valid, one duplicate, one invalid
    rows = [
        {"Suburb": "CBD", "Weekly Rent ($NZD)": 800, "Days on Market": 7,  "Bedrooms": 2},
        {"Suburb": "CBD", "Weekly Rent ($NZD)": 800, "Days on Market": 14, "Bedrooms": 2},  # duplicate
        {"Suburb": "CBD", "Weekly Rent ($NZD)": "oops", "Days on Market": 7, "Bedrooms": 2}, # invalid
    ]
    raw = _xlsx_bytes(rows)

    with caplog.at_level(logging.INFO):
        out = pm.run(raw, replace_table=False)

    sc = out["stage_counts"]
    # finished without crashing; produced a report; continued despite bad rows
    assert sc["ingested"] == 3
    assert sc["validated_ok"] >= 1          # <-- was 'accepted'
    assert sc["rejected"] >= 1
    assert sc["duplicates"] >= 1
    assert sc["stored"] == sc["transformed_ok"]
    assert isinstance(out["report_path"], str) and Path(out["report_path"]).exists()

    # some informative logging happened
    joined = " ".join(r.getMessage().lower() for r in caplog.records)
    assert "pipeline_run" in joined or "validate" in joined or "duplicate" in joined
