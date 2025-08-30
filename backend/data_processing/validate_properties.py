# validate_properties.py
from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd


# =========================
# Simple, editable settings
# =========================
REQUIRED = ["Suburb", "Weekly Rent ($NZD)", "Days on Market", "Bedrooms"]

# Range checks (min, max). Keep numbers generous for rentals.
RANGE_LIMITS = {
    "Weekly Rent ($NZD)": (100, 10000),   # $100 – $10,000 / week
    "Days on Market": (0, 730),           # 0 – 2 years
    "Bedrooms": (0, 12),                  # integer only (see integer check below)
}

# Heuristic duplicate key for the DataValidation sheet (no address column here).
DUP_KEYS = ["Suburb", "Weekly Rent ($NZD)", "Bedrooms"]


# =========================
# Public data structures
# =========================
@dataclass
class RowIssue:
    row: int          # 1-based row number in the file (includes header line offset)
    field: str        # column name (or a pipe-joined key group)
    code: str         # missing_column | missing_required | invalid_number | invalid_integer | out_of_range | duplicate
    message: str


@dataclass
class ValidationSummary:
    total: int
    accepted: int
    rejected: int
    duplicates: int
    report_csv: str | None = None


# =========================
# Helper utilities
# =========================
def _is_nan(x: Any) -> bool:
    try:
        return x is None or (isinstance(x, float) and math.isnan(x))
    except Exception:
        return False


def _coerce_number(x: Any) -> float | None:
    """Coerce common numeric strings like '1,200' to float; return None if impossible."""
    if x is None:
        return None
    if isinstance(x, (int, float)) and not math.isnan(float(x)):
        return float(x)
    if isinstance(x, str):
        s = x.replace(",", "").strip()
        if s == "":
            return None
        try:
            return float(s)
        except Exception:
            return None
    return None


# =========================
# Main validation API
# =========================
def validate_dataframe(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[RowIssue], ValidationSummary]:
    """
    Validate a dataframe of property rows according to REQUIRED fields,
    numeric/type checks, value ranges, and in-file duplicates.

    Returns:
      accepted_df: DataFrame containing only rows that passed all rules
      issues:      list of RowIssue records describing rejections
      summary:     ValidationSummary with counts
    """
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    issues: List[RowIssue] = []
    total_rows = len(df)

    # A) Required columns exist
    for col in REQUIRED:
        if col not in df.columns:
            issues.append(RowIssue(
                row=-1,
                field=col,
                code="missing_column",
                message=f"Required column '{col}' not found",
            ))

    if any(i.code == "missing_column" for i in issues):
        # If structure is wrong, reject everything early
        return pd.DataFrame(), issues, ValidationSummary(
            total=total_rows, accepted=0, rejected=total_rows, duplicates=0, report_csv=None
        )

    # B) Per-row checks
    def record_issue(idx_zero_based: int, field: str, code: str, msg: str):
        # +2 to present a human-friendly 1-based row number including header line
        issues.append(RowIssue(row=idx_zero_based + 2, field=field, code=code, message=msg))

    for idx, row in df.iterrows():
        # Required fields present
        for col in REQUIRED:
            if _is_nan(row.get(col)):
                record_issue(idx, col, "missing_required", f"Missing value for {col}")

        # Coerce numeric & range checks
        for col, (mn, mx) in RANGE_LIMITS.items():
            raw = row.get(col)
            val = _coerce_number(raw)
            if val is None:
                record_issue(idx, col, "invalid_number", f"Cannot parse number from '{raw}'")
                continue
            if not (mn <= val <= mx):
                record_issue(idx, col, "out_of_range", f"{col}={val} not in [{mn}, {mx}]")
            # write back normalized numeric
            df.at[idx, col] = val

        # Bedrooms must be an integer value if provided
        b = _coerce_number(row.get("Bedrooms"))
        if b is not None and not float(b).is_integer():
            record_issue(idx, "Bedrooms", "invalid_integer", "Bedrooms must be an integer")

    # C) Duplicate detection within the file (keep first, flag later)
    duplicates = 0
    if all(k in df.columns for k in DUP_KEYS):
        dup_mask = df.duplicated(subset=DUP_KEYS, keep="first")
        duplicates = int(dup_mask.sum())
        for idx, is_dup in enumerate(dup_mask.tolist()):
            if is_dup:
                record_issue(idx, "|".join(DUP_KEYS), "duplicate",
                             "Duplicate based on " + ", ".join(DUP_KEYS))

    # D) Build accepted_df by excluding any row that had an issue
    bad_rows = {i.row for i in issues if i.row != -1}
    bad_idx = [r - 2 for r in bad_rows]  # convert back to 0-based
    accepted_df = df.drop(index=bad_idx) if bad_idx else df.copy()

    summary = ValidationSummary(
        total=total_rows,
        accepted=len(accepted_df),
        rejected=total_rows - len(accepted_df),
        duplicates=duplicates,
        report_csv=None,
    )
    return accepted_df, issues, summary


def save_report_csv(issues: List[RowIssue], dest: str | Path) -> str:
    """
    Write the issues list to a CSV (row, field, code, message) and return its path.
    """
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    rows = [{"row": i.row, "field": i.field, "code": i.code, "message": i.message} for i in issues]
    pd.DataFrame(rows).to_csv(dest, index=False)
    return str(dest)


# ===========================================================
# Backwards-compat wrappers (keeps your older flow working)
# ===========================================================
def load_property_data(file_path: str) -> pd.DataFrame | None:
    """
    Legacy loader used in earlier stories/tests.
    """
    try:
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()
        print("Property data loaded.\n")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def validate_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Legacy function that returns a dict of issues for REQUIRED fields only.
    Preserved so previous unit tests or scripts keep passing.
    """
    issues: Dict[str, Any] = {}
    for col in REQUIRED:
        if col not in df.columns:
            issues[col] = "Missing column"
        else:
            missing_rows = df[df[col].isnull()].index.tolist()
            if missing_rows:
                issues[col] = missing_rows
    return issues


def main():
    """
    Manual run helper against DataValidation.xlsx (optional).
    """
    file_path = "Backend/data_processing/DataValidation.xlsx"
    df = load_property_data(file_path)
    if df is None:
        return

    accepted, problems, summary = validate_dataframe(df)
    if problems:
        print("Validation issues found:")
        for p in problems:
            print(f"- row {p.row:<5} field={p.field:<22} code={p.code:<16} msg={p.message}")
        print(f"\nSummary: {summary}")
        # Save a quick CSV report next to the sheet
        report_path = Path(file_path).with_name("DataValidation_issues.csv")
        save_report_csv(problems, report_path)
        print(f"CSV report -> {report_path}")
    else:
        print("No issues found.")
    print(f"Accepted rows: {len(accepted)}/{len(df)}")


if __name__ == "__main__":
    main()
