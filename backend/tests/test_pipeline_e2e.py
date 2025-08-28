# tests/test_pipeline_e2e.py
import os
from pathlib import Path
import pytest

# Make sure we can import from backend/ when running `pytest` at repo root.
BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
DATA_FILE = BACKEND_DIR / "data_processing" / "MockData.xlsx"
assert BACKEND_DIR.exists(), "Expected a 'backend' folder alongside tests/."

# Add backend to sys.path for direct imports if needed
import sys
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

def _require_mockdata():
    if not DATA_FILE.exists():
        pytest.skip(f"Sample dataset not found: {DATA_FILE}")

def _basic_stage_assertions(result: dict):
    # shape checks
    assert isinstance(result, dict)
    assert "stage_counts" in result
    assert "duration_seconds" in result
    sc = result["stage_counts"]
    for key in ["ingested", "validated_ok", "rejected", "duplicates", "transformed_ok", "stored"]:
        assert key in sc, f"missing stage count key: {key}"
        assert isinstance(sc[key], int), f"{key} must be int"
        assert sc[key] >= 0, f"{key} must be non-negative"
    # logical sanity: you can't validate/transform/store more rows than ingested
    assert sc["ingested"] >= sc["validated_ok"]
    assert sc["validated_ok"] >= sc["transformed_ok"]
    assert sc["transformed_ok"] >= sc["stored"]

@pytest.mark.order(1)
def test_pipeline_runs_without_db(monkeypatch):
    """
    E2E happy path using the real file, but monkey-patching storage so no DB is required.
    This verifies ingestion + validation + transformation and the final response shape.
    """
    _require_mockdata()

    # Import pipeline after sys.path tweak
    import pipeline_main  # type: ignore

    # Monkey-patch save_to_db used inside pipeline_main to a no-op
    monkeypatch.setattr(pipeline_main, "save_to_db", lambda df, mode="append": None)

    result = pipeline_main.run(str(DATA_FILE), replace_table=False)
    _basic_stage_assertions(result)

    # With storage disabled, 'stored' should equal transformed_ok (what would have been stored)
    assert result["stage_counts"]["stored"] == result["stage_counts"]["transformed_ok"]

@pytest.mark.order(2)
def test_pipeline_real_db_optional():
    """
    Optional: run full pipeline including DB writes.
    Enable by setting RUN_E2E_DB=1 in your environment and configuring DB_*
    variables (.env). Skips by default to keep CI simple.
    """
    if os.getenv("RUN_E2E_DB") != "1":
        pytest.skip("Set RUN_E2E_DB=1 to run this test against a real database.")
    _require_mockdata()

    import pipeline_main  # type: ignore
    result = pipeline_main.run(str(DATA_FILE), replace_table=False)
    _basic_stage_assertions(result)
