from fastapi.testclient import TestClient
from backend.main import app
import psycopg2
import os

client = TestClient(app)

def test_fetch_mock_inserts_or_updates():
    r = client.post("/properties/fetch", params={"provider": "mock"})
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    s = body["summary"]
    assert s["provider"] == "mock"
    assert all(k in s for k in ["fetched", "inserted", "updated", "skipped_invalid"])

    # Optional: verify DB rows exist for mock
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))  # or build DSN from env vars
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM properties WHERE source = 'mock';")
    count = cur.fetchone()[0]
    assert count >= s["inserted"]
    cur.close()
    conn.close()
