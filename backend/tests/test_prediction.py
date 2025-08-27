import pytest
from fastapi.testclient import TestClient

try:
    from main import app
except ModuleNotFoundError:
    from backend.main import app

client = TestClient(app)


def test_predict_valid_input():
    """Test prediction with valid input data."""
    response = client.post("/predict", json={
        "bedrooms": 2,
        "bathrooms": 1,
        "suburb": "Manurewa",
        "floor_area": 80
    })
    assert response.status_code == 200
    json_data = response.json()
    assert "predicted_rent" in json_data
    assert isinstance(json_data["predicted_rent"], (int, float))


def test_predict_invalid_suburb():
    """Test prediction with a suburb that wasn't seen during training."""
    response = client.post("/predict", json={
        "bedrooms": 2,
        "bathrooms": 1,
        "suburb": "GibberishTown",
        "floor_area": 80
    })
    assert response.status_code == 200
    json_data = response.json()
    assert "predicted_rent" in json_data
    assert isinstance(json_data["predicted_rent"], (int, float))


def test_predict_missing_fields():
    """Test prediction when required fields are missing."""
    response = client.post("/predict", json={
        "bedrooms": 3,
        "suburb": "Manurewa"
    })
    assert response.status_code == 422  # FastAPI will catch this as unprocessable
