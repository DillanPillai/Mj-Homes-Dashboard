# backend/tests/test_prediction_logging.py
import importlib
import json
from typing import Any
from datetime import datetime


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def _retrain_once(client):
    # ensure a model exists (harmless even if we later stub)
    r = client.post("/retrain-model")
    assert r.status_code == 200, r.text
    assert r.json().get("status") in ("done", "ok", "success")


def _valid_payload():
    # Matches suburbs seeded by tests/conftest.py (_seed_finaliseddataset_xlsx)
    return {"bedrooms": 3, "bathrooms": 2, "floor_area": 90, "suburb": "Epsom"}


def _patch_log_prediction(monkeypatch):
    """
    Patch whatever object the app actually calls for logging.
    Returns a list that will collect each call payload.
    Tries multiple import paths so the test tolerates refactors.
    """
    recorded: list[dict[str, Any]] = []

    def fake_log_prediction(*args, **kwargs):
        # Support both positional and keyword styles.
        payload = {}
        if args:
            # Common positional shape:
            # log_prediction(input_dict, prediction, user_id, timestamp=?)
            if len(args) >= 1:
                payload["input"] = args[0]
            if len(args) >= 2:
                payload["prediction"] = args[1]
            if len(args) >= 3:
                payload["user_id"] = args[2]

        payload.update({
            "input": kwargs.get("input_dict", kwargs.get("payload", payload.get("input"))),
            "prediction": kwargs.get("prediction", payload.get("prediction")),
            "user_id": kwargs.get("user_id", payload.get("user_id")),
            "timestamp": kwargs.get("timestamp"),
        })
        recorded.append(payload)
        return payload

    tried = 0
    main_mod = importlib.import_module("main")

    # Case 1: from predict_logger import log_prediction  (re-exported on main)
    if hasattr(main_mod, "log_prediction"):
        monkeypatch.setattr(main_mod, "log_prediction", fake_log_prediction, raising=True)
        tried += 1

    # Case 2: import predict_logger; predict_logger.log_prediction(...)
    try:
        pl = importlib.import_module("predict_logger")
        if hasattr(pl, "log_prediction"):
            monkeypatch.setattr(pl, "log_prediction", fake_log_prediction, raising=True)
            tried += 1
    except ModuleNotFoundError:
        pass

    # Case 3: namespaced module path inside Machine_Learning_Model
    try:
        pl2 = importlib.import_module("Backend.Machine_Learning_Model.predict_logger")
        if hasattr(pl2, "log_prediction"):
            monkeypatch.setattr(pl2, "log_prediction", fake_log_prediction, raising=True)
            tried += 1
    except ModuleNotFoundError:
        pass

    assert tried > 0, "Could not locate a log_prediction symbol to patch"
    return recorded


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------

def test_logs_prediction_with_user_id(client, monkeypatch):
    """
    Given a user submits input to the prediction form
    When the model returns a result
    Then the input features, predicted value, and user id are sent to the logger
    """
    _retrain_once(client)

    calls = _patch_log_prediction(monkeypatch)

    headers = {"X-User-ID": "tester-123"}
    payload = _valid_payload()

    resp = client.post("/predict", json=payload, headers=headers)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "predicted_rent" in body and isinstance(body["predicted_rent"], (int, float))

    # Exactly one logging call
    assert len(calls) == 1, f"expected 1 log call, got {len(calls)}"
    log = calls[0]

    assert log["input"] == payload
    # prediction passed to logger should match API response
    assert log["prediction"] == body["predicted_rent"]
    assert log["user_id"] == "tester-123"

    # If a timestamp is supplied, ensure it is ISO8601-parseable
    if log.get("timestamp"):
        ts = log["timestamp"].replace("Z", "+00:00")
        datetime.fromisoformat(ts)


def test_logs_prediction_with_default_user_id_when_missing(client, monkeypatch):
    """
    If no X-User-ID header is provided, the app should log with 'anonymous'.
    We stub the model & input-prep to avoid feature-name mismatch noise.
    """
    _retrain_once(client)  # harmless even if stubbed below

    import pandas as pd
    main_mod = importlib.import_module("main")

    class FakeModel:
        def predict(self, X):
            assert isinstance(X, pd.DataFrame)
            return [999.0]

    # Make /predict succeed regardless of one-hot columns / training features
    monkeypatch.setattr(main_mod, "load_model", lambda: FakeModel(), raising=True)
    monkeypatch.setattr(
        main_mod,
        "prepare_input_dataframe",
        lambda payload: pd.DataFrame([payload.model_dump() if hasattr(payload, "model_dump") else payload]),
        raising=True,
    )

    calls = _patch_log_prediction(monkeypatch)

    payload = {"bedrooms": 2, "bathrooms": 1, "floor_area": 70, "suburb": "Manurewa"}
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["predicted_rent"] == 999.0

    assert len(calls) == 1
    log = calls[0]
    assert log["input"] == payload
    assert log["prediction"] == 999.0
    assert log["user_id"] == "anonymous"


def test_logger_not_called_on_validation_error(client, monkeypatch):
    """
    Negative: if input validation fails, the logger must NOT be called.
    """
    _retrain_once(client)
    calls = _patch_log_prediction(monkeypatch)

    # missing required 'bedrooms' -> 422
    bad_payload = {"bathrooms": 1, "floor_area": 70, "suburb": "Epsom"}
    r = client.post("/predict", json=bad_payload)
    assert r.status_code == 422
    assert len(calls) == 0, "logger must not be called when validation fails"


def test_logs_include_input_without_mutation(client, monkeypatch):
    """
    Ensure the *raw* request payload (not transformed) is logged,
    and logging has no side-effects on the response.
    We stub the model & prep to avoid feature-name issues.
    """
    _retrain_once(client)

    import pandas as pd
    main_mod = importlib.import_module("main")

    class FakeModel:
        def predict(self, X):
            return [1234.5]

    monkeypatch.setattr(main_mod, "load_model", lambda: FakeModel(), raising=True)
    monkeypatch.setattr(
        main_mod,
        "prepare_input_dataframe",
        lambda payload: pd.DataFrame([payload.model_dump() if hasattr(payload, "model_dump") else payload]),
        raising=True,
    )

    calls = _patch_log_prediction(monkeypatch)

    payload = _valid_payload()
    r = client.post("/predict", json=payload, headers={"X-User-ID": "qa"})
    assert r.status_code == 200
    body = r.json()
    assert body["predicted_rent"] == 1234.5

    assert len(calls) == 1
    logged = calls[0]["input"]
    # Compare via JSON roundtrip to guarantee pure-JSON types (no numpy scalars, etc.)
    assert json.loads(json.dumps(logged)) == json.loads(json.dumps(payload))
    assert "predicted_rent" in body
