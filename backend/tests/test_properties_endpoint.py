import os
TEST_DB_URL = "sqlite:///./test_properties.sqlite3"
os.environ["DATABASE_URL"] = TEST_DB_URL

import sys
import contextlib
from pathlib import Path
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool  

THIS_FILE = Path(__file__).resolve()
BACKEND_DIR = THIS_FILE.parents[1]   
REPO_ROOT = BACKEND_DIR.parent      

for p in (str(REPO_ROOT), str(BACKEND_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

properties_router = None
Base = Property = None
get_db_backend = get_db_plain = None
engine_backend = engine_plain = None

with contextlib.suppress(Exception):
    from backend.routers.properties import router as properties_router  # type: ignore
    from backend.models import Base, Property  # type: ignore
    import backend.db as backend_db  # type: ignore
    get_db_backend = backend_db.get_db
    engine_backend = backend_db.engine

# Fallback: local path
with contextlib.suppress(Exception):
    if properties_router is None:
        from routers.properties import router as properties_router  # type: ignore
        from models import Base, Property  # type: ignore
        import db as plain_db  # type: ignore
        get_db_plain = plain_db.get_db
        engine_plain = plain_db.engine

assert properties_router is not None, "Could not import properties router."
assert Base is not None and Property is not None, "Failed to import models.Base/Property."

test_engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    future=True,
)
TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False, future=True)

# Create tables on ALL engines that might be used by the app/router
Base.metadata.create_all(bind=test_engine)
if engine_backend is not None:
    Base.metadata.create_all(bind=engine_backend)
if engine_plain is not None:
    Base.metadata.create_all(bind=engine_plain)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="MJ Home API (tests-only)")
app.include_router(properties_router)

if get_db_backend is not None:
    app.dependency_overrides[get_db_backend] = override_get_db
if get_db_plain is not None:
    app.dependency_overrides[get_db_plain] = override_get_db

# No re-raising server exceptions so we can assert on 500s
client = TestClient(app, raise_server_exceptions=False)


def clear():
    """Delete all rows so each test starts with a known state."""
    with TestingSessionLocal.begin() as s:
        s.execute(delete(Property))

def seed():
    """Insert a single property record."""
    now = datetime.now(timezone.utc)
    with TestingSessionLocal.begin() as s:
        s.add(
            Property(
                address="12 Example St",
                suburb="Manurewa",
                bedrooms=3,
                bathrooms=1,
                floor_area=85,
                rent_weekly=650,
                property_type="House",
                created_at=now,
                updated_at=now,
            )
        )

def _drop_properties_table_on_all_engines():
    """Force a DB failure by removing the table used by the endpoint query."""
    for eng in (test_engine, engine_backend, engine_plain):
        if eng is None:
            continue
        with contextlib.suppress(Exception):
            # check first guards against missing table; suppress to keep test clean
            Property.__table__.drop(bind=eng, checkfirst=True)

def test_200_and_expected_fields():
    clear(); seed()
    r = client.get("/properties")
    assert r.status_code == 200, r.text
    data = r.json()
    assert isinstance(data, list) and len(data) == 1
    item = data[0]
    for k in [
        "id", "address", "suburb", "bedrooms", "bathrooms",
        "floor_area", "rent_weekly", "property_type",
        "created_at", "updated_at",
    ]:
        assert k in item, f"Missing field {k}"

def test_empty_returns_empty_array():
    clear()
    r = client.get("/properties")
    assert r.status_code == 200, r.text
    assert r.json() == []

def test_db_failure_returns_500():
    # Force the SELECT to fail regardless of which engine or router path is utilised
    _drop_properties_table_on_all_engines()

    r = client.get("/properties")
    assert r.status_code == 500, r.text
    # Recreate tables for later tests
    Base.metadata.create_all(bind=test_engine)
    if engine_backend is not None:
        Base.metadata.create_all(bind=engine_backend)
    if engine_plain is not None:
        Base.metadata.create_all(bind=engine_plain)

def test_repeated_requests_reflect_live_data():
    clear()
    assert client.get("/properties").json() == []  # first call is empty
    seed()
    assert len(client.get("/properties").json()) == 1  # now sees the new row
