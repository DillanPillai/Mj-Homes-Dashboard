# backend/routers/ingest.py
from __future__ import annotations

from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import Any, Dict
from io import BytesIO, StringIO
from pathlib import Path
from datetime import datetime
import pandas as pd

from services.ingest_properties import validate_property_dataframe
from data_processing.validate_properties import save_report_csv, RowIssue  # type: ignore
from pipeline_main import run as pipeline_run  # NEW: orchestrator for full pipeline

router = APIRouter(prefix="/ingest", tags=["Ingestion & Validation"])

SUPPORTED_EXTS = {".csv", ".xlsx", ".xls", ".html", ".htm"}
# Keep reports in the same place as other pipeline reports
REPORTS_DIR = Path(__file__).resolve().parents[1] / "Machine_Learning_Model" / "reports"


# ---------- Helpers ----------
def _load_dataframe_from_upload(upload: UploadFile) -> pd.DataFrame:
    """
    Load a DataFrame from an uploaded CSV/XLSX file.
    Raises HTTPException on unsupported type or parse error.
    """
    suffix = Path(upload.filename or "").suffix.lower()
    if suffix not in SUPPORTED_EXTS:
        raise HTTPException(status_code=400, detail=f"unsupported_file_type: {suffix or 'unknown'}")

    try:
        raw = upload.file.read()
        if not raw:
            raise HTTPException(status_code=400, detail="no_rows_found")

        if suffix == ".csv":
            # Try UTF-8 first; fall back to latin-1 if decoding fails.
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                text = raw.decode("latin-1")
            df = pd.read_csv(StringIO(text))
        else:
            df = pd.read_excel(BytesIO(raw))

        # Normalize header whitespace
        df.columns = [c.strip() for c in df.columns]
        return df

    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=422, detail=f"parse_error: {type(ex).__name__}: {ex}") from ex


def _write_report(issues: list[RowIssue]) -> str | None:
    """
    If there are issues, write a CSV report and return its path relative to backend/.
    """
    if not issues:
        return None
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().isoformat(timespec="seconds").replace(":", "-")
    path = REPORTS_DIR / f"ingest_report_{ts}.csv"
    return save_report_csv(issues, path)


# ---------- Validation-only endpoint (kept) ----------
@router.post("/file")
async def validate_file(
    file: UploadFile = File(..., description="CSV/XLSX file containing property rows"),
    dry_run: bool = Query(True, description="No persistence occurs; returns validation summary & report"),
) -> Dict[str, Any]:
    """
    Validate an uploaded CSV/XLSX of property rows against rule-based checks.
    Returns JSON summary, per-row issues, and a CSV report path (if any).

    Notes:
    - This endpoint focuses on validation & reporting for your user story.
    - Persistence is intentionally disabled for safety (dry_run always honored here).
    """
    # Load DF
    df = _load_dataframe_from_upload(file)

    # Run shared validator
    result = validate_property_dataframe(df)
    issues_dicts = result["issues"]

    # Write report if there are issues
    issues_objs = [RowIssue(**i) for i in issues_dicts]
    report_path = _write_report(issues_objs)

    # Build response
    response = {
        "dry_run": True,  # always True here
        "summary": result["summary"],
        "report_csv": None,
        "issues": issues_dicts,
    }
    if report_path:
        backend_root = Path(__file__).resolve().parents[1]
        rel = Path(report_path).resolve().relative_to(backend_root)
        response["report_csv"] = f"./{rel.as_posix()}"
    return response


# ---------- Full pipeline endpoint (new) ----------
@router.post("/pipeline")
async def run_pipeline(
    file: UploadFile = File(..., description="CSV/XLSX/HTML data to ingest"),
    replace_table: bool = Query(False, description="Replace properties table instead of append"),
) -> Dict[str, Any]:
    """
    End-to-end pipeline run: ingestion → validation → transformation → storage.
    Returns stage counts and the path to a CSV issues report (if any).
    """
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in SUPPORTED_EXTS:
        raise HTTPException(status_code=400, detail=f"unsupported_file_type: {suffix or 'unknown'}")

    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="empty_file")

    try:
        result = pipeline_run(raw, replace_table=replace_table)
        return {
            "stage_counts": result["stage_counts"],
            "report_csv": result["report_path"],
            "duration_seconds": result["duration_seconds"],
            "mode": "replace" if replace_table else "append",
        }
    except ValueError as ex:
        raise HTTPException(status_code=422, detail=f"pipeline_error: {ex}") from ex
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"internal_error: {type(ex).__name__}") from ex
