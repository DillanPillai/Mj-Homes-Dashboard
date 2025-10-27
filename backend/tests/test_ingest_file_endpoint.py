import sys, pathlib
BACKEND_DIR = pathlib.Path(__file__).resolve().parents[1]  # .../backend
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import io
import pandas as pd

REQ = ["Suburb", "Weekly Rent ($NZD)", "Days on Market", "Bedrooms"]

def _xlsx_bytes(rows):
    df = pd.DataFrame(rows, columns=REQ)
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    buf.seek(0)
    return buf

def test_file_ingest_200_with_summary_and_report_when_issues(client):
    rows = [
        ["Albany", 650, 10, 2],   # ok
        ["Albany", 650, 20, 2],   # duplicate (by SUBURB, RENT, BEDROOMS)
        ["CBD", "600x", 7, 2],    # invalid number
    ]
    files = {"file": ("props.xlsx", _xlsx_bytes(rows), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    r = client.post("/ingest/file", files=files)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["dry_run"] is True
    assert set(body["summary"].keys()) == {"total", "accepted", "rejected", "duplicates"}
    # with issues present, report_csv should be set to a relative path
    assert body["summary"]["total"] == 3
    assert body["summary"]["duplicates"] == 1
    assert body["report_csv"] is not None
    assert body["report_csv"].startswith("./Machine_Learning_Model/reports/ingest_report_")

def test_file_ingest_200_no_report_when_clean(client):
    rows = [
        ["Epsom", 900, 12, 3],
        ["Manurewa", 520, 30, 2],
    ]
    files = {"file": ("clean.xlsx", _xlsx_bytes(rows), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    r = client.post("/ingest/file", files=files)
    assert r.status_code == 200
    body = r.json()
    assert body["summary"]["accepted"] == 2
    assert body["summary"]["rejected"] == 0
    assert body["summary"]["duplicates"] == 0
    assert body["report_csv"] is None

def test_file_ingest_400_no_rows_found(client):
    # Empty upload (no bytes) should hit the "no_rows_found" 400
    files = {"file": ("empty.xlsx", b"", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    r = client.post("/ingest/file", files=files)
    assert r.status_code == 400
    assert r.json()["detail"] == "no_rows_found"

def test_file_ingest_400_unsupported_type(client):
    files = {"file": ("data.txt", b"hello", "text/plain")}
    r = client.post("/ingest/file", files=files)
    assert r.status_code == 400
    assert "unsupported_file_type" in r.json()["detail"]
