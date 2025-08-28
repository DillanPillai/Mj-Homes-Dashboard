"""
Orchestrator for the modular data pipeline (ingestion → validation → transformation → storage).

- New API: run(file_like, replace_table=False)  -> returns dict with stage_counts, report_path, duration_seconds
- Backward compatibility: keeps your previous "legacy" pipeline imports and main() so older flows don't break.
"""

from __future__ import annotations
from typing import Dict, Union
from io import BytesIO
from pathlib import Path
from datetime import datetime
import pandas as pd

# ---------- NEW pipeline imports ----------
from utils.logger import setup as setup_logger
from data_processing.validate_properties import validate_dataframe, save_report_csv
from data_processing.transformer import transform_data
from data_processing.loader import save_to_db

logger = setup_logger()

# ---------- LEGACY imports kept (best-effort) ----------
# Your old pipeline referenced scrape_listings / clean_data / predict_rent.
# We keep these imports optional so previous stories/scripts won't crash.
try:
    # when running from backend/
    from data_scraper.scraper import scrape_listings  # type: ignore
    from data_processing.cleaner import clean_data     # type: ignore
    from Machine_Learning_Model.rental_price_model import predict_rent  # type: ignore
except Exception:
    try:
        # when importing as backend.pipeline_main
        from backend.data_scraper.scraper import scrape_listings  # type: ignore
        from backend.data_processing.cleaner import clean_data     # type: ignore
        from backend.Machine_Learning_Model.rental_price_model import predict_rent  # type: ignore
    except Exception:
        scrape_listings = None  # type: ignore
        clean_data = None       # type: ignore
        predict_rent = None     # type: ignore


# ---------- Helpers ----------
def _read_any_table(src: Union[str, Path, bytes, BytesIO]) -> pd.DataFrame:
    """
    Load CSV/XLSX/HTML table into a DataFrame.
    Accepts: file path (str/Path) OR raw bytes/BytesIO (e.g., from UploadFile).
    """
    if isinstance(src, (bytes, BytesIO)):
        # try excel first, then csv
        b = src if isinstance(src, bytes) else src.getvalue()
        try:
            return pd.read_excel(BytesIO(b))
        except Exception:
            return pd.read_csv(BytesIO(b))
    p = Path(src) if not isinstance(src, Path) else src
    suf = p.suffix.lower()
    if suf in (".xlsx", ".xls"):
        return pd.read_excel(p)
    if suf == ".csv":
        return pd.read_csv(p)
    if suf in (".html", ".htm"):
        tables = pd.read_html(p)
        if not tables:
            raise ValueError("No HTML tables found.")
        return tables[0]
    raise ValueError(f"Unsupported file type: {suf or 'unknown'}")


# ---------- Public API for the new story ----------
def run(file_like: Union[str, Path, bytes, BytesIO], *, replace_table: bool = False) -> Dict:
    """
    End-to-end pipeline:
      1) Ingestion (read table)
      2) Validation (rule-based)
      3) Transformation (feature/typing/normalisation)
      4) Storage (append by default; can replace)

    Returns:
      {
        "stage_counts": {ingested, validated_ok, rejected, duplicates, transformed_ok, stored},
        "report_path": "backend/Machine_Learning_Model/reports/ingest_report_....csv" | None,
        "duration_seconds": float
      }
    """
    start = datetime.utcnow()

    # 1) Ingestion
    df = _read_any_table(file_like)
    total_rows = len(df)

    # 2) Validation
    accepted_df, issues, summary = validate_dataframe(df)

    # 3) Report (only if issues)
    report_path = None
    if issues:
        ts = start.strftime("%Y-%m-%dT%H-%M-%S")
        reports_dir = Path("backend/Machine_Learning_Model/reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_path = save_report_csv(issues, reports_dir / f"ingest_report_{ts}.csv")

    # 4) Transformation
    transformed = transform_data(accepted_df) if not accepted_df.empty else accepted_df

    # 5) Storage
    if not transformed.empty:
        save_to_db(transformed, mode="replace" if replace_table else "append")

    out = {
        "stage_counts": {
            "ingested": total_rows,
            "validated_ok": summary.accepted,
            "rejected": summary.rejected,
            "duplicates": summary.duplicates,
            "transformed_ok": len(transformed),
            "stored": int(len(transformed)),
        },
        "report_path": report_path,
        "duration_seconds": (datetime.utcnow() - start).total_seconds(),
    }
    logger.info(f"pipeline_run {out}")
    return out


# ---------- Legacy entrypoint (kept to avoid breaking older flows) ----------
def main():
    """
    Legacy pipeline runner.
    If your older modules are available, run the previous flow.
    Otherwise, print a friendly message telling how to use the new run() API.
    """
    print("Starting MJ Home backend pipeline (legacy main)...")
    if scrape_listings and clean_data and predict_rent:
        try:
            raw_data = scrape_listings()
            cleaned_data = clean_data(raw_data)
            predicted_data = predict_rent(cleaned_data)
            save_to_db(predicted_data, mode="append")  # safe default
            print("Legacy pipeline completed successfully!")
            return
        except Exception as ex:
            print(f"Legacy pipeline failed: {type(ex).__name__}: {ex}")

    print(
        "Legacy modules not available. "
        "Use pipeline_main.run(<path or bytes>) to execute the new modular pipeline."
    )


if __name__ == "__main__":
    # Handy manual test against a local file if you want:
    try:
        print(run("backend/data_processing/MockData.xlsx"))
    except Exception as e:
        print(f"Run error: {e}")
