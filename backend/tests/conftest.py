import io
import os
import sys
import shutil
import tempfile
import importlib
from pathlib import Path

import pandas as pd
import pytest
from fastapi.testclient import TestClient

def _seed_mockdata_xlsx(base_dir: Path):
    dp = base_dir / "data_processing"
    dp.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame({
        "Bedrooms": [2, 3],
        "Bathrooms": [1, 2],
        "Suburb": ["Manurewa", "Epsom"],
        "Weekly Rent ($NZD)": [520, 900],
        # code defaults to 100 if missing
    })
    (dp / "MockData.xlsx").unlink(missing_ok=True)
    df.to_excel(dp / "MockData.xlsx", index=False)


@pytest.fixture(scope="session", autouse=True)
def _seed():
    import numpy as np, random
    np.random.seed(42)
    random.seed(42)


@pytest.fixture()
def client(tmp_path, monkeypatch):
    """
    - Work in a temporary copy of backend/
    - cd into it so relative imports like `routers` / `services` resolve
    - set DATABASE_URL to a temp sqlite file before importing main
    - add backend_tmp to sys.path so `import main` works
    - retrain the model once per test function so /predict always has a model
    """
    repo_root = Path(__file__).resolve().parents[2]       # .../Mj-Homes-Dashboard
    backend_src = repo_root / "backend"

    workdir = Path(tempfile.mkdtemp(prefix="mjhomes_pytests_"))
    backend_tmp = workdir / "backend"
    shutil.copytree(backend_src, backend_tmp)

    old_cwd = Path.cwd()
    os.chdir(backend_tmp) 

    # Seed dataset so ALLOWED_SUBURBS loads at import time
    _seed_mockdata_xlsx(backend_tmp)

    # Point DB to a throwaway SQLite file so db.py doesn't crash
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./test_py.db")

    # Make main.py importable
    sys.path.insert(0, str(backend_tmp))

    try:
        app_module = importlib.import_module("main")
        app = getattr(app_module, "app")
        tc = TestClient(app)

        # Retrain here to avoid scope conflicts and ensure a model exists
        r = tc.post("/retrain-model")
        assert r.status_code == 200, r.text
        assert r.json().get("status", "").lower() in {"done", "ok", "success"}

        yield tc
    finally:
        # cleanup
        if str(backend_tmp) in sys.path:
            sys.path.remove(str(backend_tmp))
        os.chdir(old_cwd)
        shutil.rmtree(workdir, ignore_errors=True)


def excel_bytes(rows: list[dict]) -> io.BytesIO:
    df = pd.DataFrame(rows)
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    buf.seek(0)
    return buf
