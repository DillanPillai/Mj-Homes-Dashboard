import os
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"  # isolated test DB

from datetime import datetime, timezone
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from db import get_db
from models import Base, Property

# shared in-memory SQLite so multiple sessions see same data
engine = create_engine(
    os.environ["DATABASE_URL"],
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    future=True,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Prevents TestClient from re-raising server exceptions so we can assert 500
client = TestClient(app, raise_server_exceptions=False)

def clear():
    with TestingSessionLocal.begin() as s:
        s.query(Property).delete()

def seed():
    now = datetime.now(timezone.utc)
    with TestingSessionLocal.begin() as s:
        s.add(Property(
            address="12 Example St",
            suburb="Manurewa",
            bedrooms=3,
            bathrooms=1,
            floor_area=85,
            rent_weekly=650,
            property_type="House",
            created_at=now,
            updated_at=now,
        ))

def test_200_and_expected_fields():
    clear(); seed()
    r = client.get("/properties")
    assert r.status_code == 200
    item = r.json()[0]
    for k in ["rent_weekly","suburb","property_type","address","bedrooms","bathrooms"]:
        assert k in item

def test_empty_returns_empty_array():
    clear()
    r = client.get("/properties")
    assert r.status_code == 200 and r.json() == []

def test_db_failure_returns_500():
    def bad_db():
        raise Exception("boom")
    app.dependency_overrides[get_db] = bad_db
    r = client.get("/properties")
    assert r.status_code == 500
    app.dependency_overrides[get_db] = override_get_db

def test_repeated_requests_reflect_live_data():
    clear()
    assert client.get("/properties").json() == []
    seed()
    assert len(client.get("/properties").json()) == 1
