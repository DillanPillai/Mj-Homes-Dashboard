import math
import pytest
from fastapi.testclient import TestClient

def test_predict_valid_input(client: TestClient):
    """Valid input -> 200 and numeric prediction."""
    resp = client.post("/predict", json={
        "bedrooms": 2,
        "bathrooms": 1,
        "suburb": "Manurewa",
        "floor_area": 80,
    })
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "predicted_rent" in data
    assert isinstance(data["predicted_rent"], (int, float))
    assert math.isfinite(float(data["predicted_rent"]))

def test_predict_invalid_suburb_returns_422(client: TestClient):
    """
    main.py validator enforces suburb ∈ ALLOWED_SUBURBS -> 422 on unknown.
    """
    resp = client.post("/predict", json={
        "bedrooms": 2,
        "bathrooms": 1,
        "suburb": "GibberishTown",
        "floor_area": 80,
    })
    assert resp.status_code == 422
    detail = resp.json().get("detail")
    assert isinstance(detail, str) or isinstance(detail, list)

def test_predict_missing_fields_returns_422(client: TestClient):
    """Missing required fields -> 422 via Pydantic validation."""
    resp = client.post("/predict", json={
        "bedrooms": 3,
        "suburb": "Manurewa",
    })
    assert resp.status_code == 422
    detail = resp.json().get("detail")
    assert isinstance(detail, list) and len(detail) > 0

def test_openapi_has_predict_and_examples(client: TestClient):
    """
    Swagger should include /predict and show examples coming from Field(..., example=...).
    """
    r = client.get("/openapi.json")
    assert r.status_code == 200
    spec = r.json()
    assert "/predict" in spec.get("paths", {})

    schemas = spec.get("components", {}).get("schemas", {})
    rental_input = schemas.get("RentalInput") or {}
    props = rental_input.get("properties", {})

    # ensure examples exist for the documented fields
    for name in ("bedrooms", "bathrooms", "floor_area", "suburb"):
        assert name in props, f"{name} missing from schema"
        assert ("example" in props[name]) or ("examples" in props[name]), \
            f"{name} missing example in schema"
