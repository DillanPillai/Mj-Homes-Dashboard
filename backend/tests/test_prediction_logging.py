import importlib
from typing import Any

from .conftest import excel_bytes


def _retrain_once(client):
    # to ensure a model exists before calling /predict
    r = client.post("/retrain-model")
    assert r.status_code == 200
    assert r.json().get("status") == "done"


def test_logs_prediction_with_user_id(client, monkeypatch):
    """
    Given a user submits input to the prediction form
    When the model returns a result
    Then the input features, predicted value, and user id are sent to the logger
    """
    _retrain_once(client)

    main_mod = importlib.import_module("main")
    calls: list[dict[str, Any]] = []

    def fake_log_prediction(input_dict, prediction, user_id):
        calls.append({"input": input_dict, "prediction": prediction, "user_id": user_id})

    monkeypatch.setattr(main_mod, "log_prediction", fake_log_prediction, raising=True)

    headers = {"X-User-ID": "tester-123"}
    payload = {"bedrooms": 3, "bathrooms": 2, "floor_area": 90, "suburb": "Epsom"}

    resp = client.post("/predict", json=payload, headers=headers)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "predicted_rent" in body and isinstance(body["predicted_rent"], (int, float))

    assert len(calls) == 1, "log_prediction should be called exactly once"
    log = calls[0]
    assert log["input"] == payload
    assert isinstance(log["prediction"], (int, float))
    assert log["user_id"] == "tester-123"


def test_logs_prediction_with_default_user_id_when_missing(client, monkeypatch):
    """
    If no X-User-ID header is provided, app should log with 'anonymous'.
    We stub the model + input prep to avoid feature-name mismatch noise.
    """
    _retrain_once(client)  # keep it, but we won't depend on its columns

    import importlib, pandas as pd
    main_mod = importlib.import_module("main")

    # stub the model & prep so /predict can succeed regardless of columns
    class FakeModel:
        def predict(self, X):
            # return a stable numeric prediction
            return [999.0]

    monkeypatch.setattr(main_mod, "load_model", lambda: FakeModel(), raising=True)
    monkeypatch.setattr(
        main_mod,
        "prepare_input_dataframe",
        lambda payload: pd.DataFrame([payload.model_dump() if hasattr(payload, "model_dump") else payload]),
        raising=True,
    )

    recorded = {}

    def fake_log_prediction(input_dict, prediction, user_id):
        recorded["input"] = input_dict
        recorded["prediction"] = prediction
        recorded["user_id"] = user_id

    monkeypatch.setattr(main_mod, "log_prediction", fake_log_prediction, raising=True)

    # No X-User-ID header
    payload = {"bedrooms": 2, "bathrooms": 1, "floor_area": 70, "suburb": "Manurewa"}

    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["predicted_rent"] == 999.0  # from our FakeModel

    # Logger should fire with anonymous and the exact payload
    assert recorded, "log_prediction should have been called"
    assert recorded["input"] == payload
    assert recorded["prediction"] == 999.0
    assert recorded["user_id"] == "anonymous"

def test_logger_not_called_on_validation_error(client, monkeypatch):
    """
    Negative: if input validation fails, the logger must NOT be called.
    """
    _retrain_once(client)

    main_mod = importlib.import_module("main")
    called = {"count": 0}

    def fake_log_prediction(*_args, **_kwargs):
        called["count"] += 1

    monkeypatch.setattr(main_mod, "log_prediction", fake_log_prediction, raising=True)

    # missing required 'bedrooms', so FastAPI/Pydantic returns 422
    bad_payload = {"bathrooms": 1, "floor_area": 70, "suburb": "Epsom"}
    r = client.post("/predict", json=bad_payload)
    assert r.status_code == 422
    assert called["count"] == 0, "logger must not be called when validation fails"
