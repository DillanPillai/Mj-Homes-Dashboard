# backend/data_processing/dataset_uploader.py
from __future__ import annotations

import io
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple, List

import pandas as pd
from sqlalchemy import MetaData, Table, Column, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy import insert as sa_insert


# ---------- Supported types ----------
ALLOWED_MIME = {
    "text/csv": "csv",
    "application/vnd.ms-excel": "csv",  # some browsers use this for CSV
    "text/html": "html",
    "application/xhtml+xml": "html",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",  # Excel
}


def _ext_from_name(name: str) -> str:
    name = (name or "").lower()
    if name.endswith(".csv"):
        return "csv"
    if name.endswith(".htm") or name.endswith(".html"):
        return "html"
    if name.endswith(".xlsx"):
        return "xlsx"
    return ""


# ---------- Load to DataFrame ----------
def _load_to_df(file_bytes: bytes, filename: str, content_type: str) -> pd.DataFrame:
    """
    Turn uploaded bytes into a pandas DataFrame (CSV, HTML table, or XLSX).
    If HTML has multiple tables, pick the largest non-empty one.
    """
    kind = ALLOWED_MIME.get(content_type) or _ext_from_name(filename)

    if kind == "csv":
        return pd.read_csv(io.BytesIO(file_bytes))

    if kind == "html":
        tables = pd.read_html(io.BytesIO(file_bytes), flavor="bs4")
        tables = [t for t in tables if not t.empty]
        if not tables:
            raise ValueError("No data tables found in the HTML file.")
        tables.sort(key=lambda df: (df.shape[0] * df.shape[1]), reverse=True)
        return tables[0]

    if kind == "xlsx":
        return pd.read_excel(io.BytesIO(file_bytes))

    raise ValueError("Unsupported file type. Please upload CSV, HTML, or XLSX.")


# ---------- Cleaning / Standardising ----------
def _clean_and_standardize(df: pd.DataFrame) -> pd.DataFrame:
    """
    Predictable cleaning:
      - normalise column names
      - drop fully empty columns/rows
      - trim whitespace
      - convert numeric-looking strings to numbers
    """
    df = df.copy()

    # normalise headers
    df.columns = (
        df.columns
        .map(lambda c: str(c).strip())
        .map(lambda c: c.lower().replace(" ", "_").replace("-", "_"))
    )

    # drop fully empty cols/rows
    df = df.dropna(axis=1, how="all")
    df = df.dropna(axis=0, how="all")

    # trim text
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].map(lambda x: x.strip() if isinstance(x, str) else x)

    # numeric conversion where obvious
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = pd.to_numeric(df[col], errors="ignore")

    return df.reset_index(drop=True)


# ---------- Hashing for dedupe ----------
def _row_hash(row_dict: Dict[str, Any]) -> str:
    s = json.dumps(row_dict, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def add_hashes(df: pd.DataFrame) -> pd.DataFrame:
    """Add a _row_hash column based on all columns (after cleaning)."""
    records = df.to_dict(orient="records")
    hashes = [_row_hash(r) for r in records]
    df = df.copy()
    df["_row_hash"] = hashes
    return df


# ---------- DB Table & Insert ----------
def ensure_table(engine) -> Table:
    """
    Create (if needed) a table:
      uploaded_rows(row_hash PK, data JSON/JSONB, created_at)
    Uses JSONB on Postgres; JSON on SQLite/others so local tests still pass.
    """
    meta = MetaData()
    is_postgres = engine.dialect.name == "postgresql"
    json_type = JSONB if is_postgres else JSON

    table = Table(
        "uploaded_rows",
        meta,
        Column("row_hash", String, primary_key=True),
        Column("data", json_type, nullable=False),
        Column("created_at", DateTime(timezone=True), default=datetime.utcnow),
    )
    meta.create_all(engine)
    return table


def insert_unique_rows(engine, table: Table, df_with_hash: pd.DataFrame) -> int:
    """
    Insert unique rows by row_hash.
    - Postgres: ON CONFLICT DO NOTHING
    - SQLite/others: INSERT OR IGNORE
    Returns number of rows actually inserted.
    """
    if df_with_hash.empty:
        return 0

    payload: List[Dict[str, Any]] = [
        {"row_hash": rh, "data": rec}
        for rh, rec in zip(
            df_with_hash["_row_hash"],
            df_with_hash.drop(columns=["_row_hash"]).to_dict(orient="records"),
        )
    ]

    inserted = 0
    with engine.begin() as conn:
        if engine.dialect.name == "postgresql":
            stmt = pg_insert(table).values(payload).on_conflict_do_nothing(
                index_elements=["row_hash"]
            )
            result = conn.execute(stmt)
            inserted = result.rowcount or 0
        else:
            # SQLite & others
            for row in payload:
                stmt = sa_insert(table).values(**row).prefix_with("OR IGNORE")
                res = conn.execute(stmt)
                inserted += res.rowcount or 0

    return inserted


# ---------- Public entry used by FastAPI route ----------
def process_upload(
    *,
    file_bytes: bytes,
    filename: str,
    content_type: str,
    engine,
    cleaned_dir: Path,
) -> Tuple[Dict[str, Any], Path]:
    """
    1) parse -> DataFrame
    2) clean/standardize
    3) add hashes
    4) store unique rows in DB
    5) save cleaned CSV (without _row_hash)
    6) return summary + saved path
    """
    df = _load_to_df(file_bytes, filename, content_type)
    df = _clean_and_standardize(df)
    df_h = add_hashes(df)

    total_rows = len(df_h)

    table = ensure_table(engine)
    inserted = insert_unique_rows(engine, table, df_h)

    cleaned_no_hash = df_h.drop(columns=["_row_hash"])
    cleaned_dir.mkdir(parents=True, exist_ok=True)
    stamped = f"cleaned_{Path(filename).stem}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.csv"
    out_path = cleaned_dir / stamped
    cleaned_no_hash.to_csv(out_path, index=False, encoding="utf-8-sig")

    summary = {
        "total_rows": total_rows,
        "rows_inserted": inserted,
        "rows_skipped": total_rows - inserted,  # duplicates
        "message": "Upload processed successfully.",
        "cleaned_file_name": stamped,
    }
    return summary, out_path
