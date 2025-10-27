# --- import shim so tests work from repo root or /backend ---
import sys, pathlib
BACKEND_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
# ------------------------------------------------------------

import io
import pandas as pd

def _xlsx_bytes(rows):
    df = pd.DataFrame(rows)
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    buf.seek(0)
    return buf

def test_pipeline_append_success(client):
    rows = [
        {"Suburb": "Takapuna", "Weekly Rent ($NZD)": 1200, "Days on Market": 5, "Bedrooms": 2},
        {"Suburb": "Albany",   "Weekly Rent ($NZD)": 700,  "Days on Market": 9, "Bedrooms": 2},
    ]
    files = {"file": ("data.xlsx", _xlsx_bytes(rows), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    r = client.post("/ingest/pipeline?replace_table=false", files=files)
    assert r.status_code == 200, r.text

    body = r.json()
    assert set(body.keys()) == {"stage_counts", "report_csv", "duration_seconds", "mode"}
    assert body["mode"] == "append"
    sc = body["stage_counts"]
    assert set(sc.keys()) == {"ingested", "validated_ok", "rejected", "duplicates", "transformed_ok", "stored"}
    assert sc["validated_ok"] >= 2
    assert isinstance(body["report_csv"], str) and body["report_csv"]  # there is always a CSV file path emitted by pipeline

def test_pipeline_replace_success(client):
    rows = [
        {"Suburb": "Epsom", "Weekly Rent ($NZD)": 900, "Days on Market": 12, "Bedrooms": 3},
    ]
    files = {"file": ("data.xlsx", _xlsx_bytes(rows), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    r = client.post("/ingest/pipeline?replace_table=true", files=files)
    assert r.status_code == 200
    body = r.json()
    assert body["mode"] == "replace"
    assert body["stage_counts"]["validated_ok"] >= 1

def test_pipeline_400_empty_file(client):
    files = {"file": ("empty.xlsx", b"", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    r = client.post("/ingest/pipeline", files=files)
    assert r.status_code == 400
    assert r.json()["detail"] == "empty_file"

def test_pipeline_400_unsupported_type(client):
    files = {"file": ("data.txt", b"hello", "text/plain")}
    r = client.post("/ingest/pipeline", files=files)
    assert r.status_code == 400
    assert "unsupported_file_type" in r.json()["detail"]
