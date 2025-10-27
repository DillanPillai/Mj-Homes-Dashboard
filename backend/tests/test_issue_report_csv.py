import sys, pathlib
BACKEND_DIR = pathlib.Path(__file__).resolve().parents[1]  # .../backend
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from pathlib import Path
from data_processing.validate_properties import RowIssue, save_report_csv

def test_save_report_csv_writes_file(tmp_path: Path):
    issues = [
        RowIssue(row=2, field="Weekly Rent ($NZD)", code="invalid_number", message="Cannot parse number"),
        RowIssue(row=3, field="Bedrooms", code="invalid_integer", message="Bedrooms must be an integer"),
    ]
    dest = tmp_path / "reports" / "issues.csv"
    out_path = save_report_csv(issues, dest)

    p = Path(out_path)
    assert p.exists()
    content = p.read_text(encoding="utf-8")
    assert "invalid_number" in content and "invalid_integer" in content
