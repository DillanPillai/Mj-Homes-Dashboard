# routers/ingest.py
from __future__ import annotations

from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import Any, Dict
from io import BytesIO, StringIO
from pathlib import Path
from datetime import datetime
import pandas as pd

from services.ingest_properties import validate_property_dataframe
from data_processing.validate_properties import save_report_csv, RowIssue  # type: ignore

router = APIRouter(prefix="/ingest", tags=["Ingestion & Validation"])

SUPPORTED_EXTS = {".csv", ".xlsx", ".xls"}
REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"  # backend/reports


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


@router.post("/file")
async def validate_file(
    file: UploadFile = File(..., description="CSV or Excel file containing property rows"),
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
    issues_dicts = result["issues"]  # list of dicts

    # Write report if there are issues
    # Recreate RowIssue objects to reuse the CSV writer neatly
    issues_objs = [RowIssue(**i) for i in issues_dicts]
    report_path = _write_report(issues_objs)

    # Build response
    response = {
        "dry_run": True if dry_run else True,  # always True here to avoid accidental writes
        "summary": result["summary"],
        "report_csv": None,
        "issues": issues_dicts,
    }
    if report_path:
        # Provide a path relative to backend/ so it's easy to find locally
        backend_root = Path(__file__).resolve().parents[1]
        rel = Path(report_path).resolve().relative_to(backend_root)
        response["report_csv"] = f"./{rel.as_posix()}"
    return response
