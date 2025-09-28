# backend/data_scraper/oneroof_sep_2025_scrape.py
# pip install requests beautifulsoup4 pandas openpyxl

import os
import re
import io
import time
import argparse
from typing import List, Tuple

import requests
import pandas as pd
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry

ARTICLE_URL = "https://www.oneroof.co.nz/insights/house-price-report/oneroof-house-price-report-september-2025-48104"

BASE_DIR = os.path.dirname(__file__)                         # .../backend/data_scraper
OUT_DIR  = os.path.abspath(os.path.join(BASE_DIR, "..", "data_processing"))
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HTTP session --------
def get_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/126.0 Safari/537.36"
    })
    retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[429,500,502,503,504])
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.mount("http://",  HTTPAdapter(max_retries=retries))
    return s

# -------- find all Datawrapper embeds on the page --------
DW_IFRAME_RE = re.compile(r"https://datawrapper\.dwcdn\.net/([A-Za-z0-9]+)/(\d+)/?")

def find_all_datawrappers(html: str) -> List[Tuple[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    ids = []

    # explicit iframe/script src
    for tag in soup.find_all(["iframe", "script"], src=True):
        m = DW_IFRAME_RE.search(tag["src"])
        if m:
            ids.append((m.group(1), m.group(2)))

    # inline <script> bodies
    for sc in soup.find_all("script"):
        if sc.string:
            m = DW_IFRAME_RE.search(sc.string)
            if m:
                ids.append((m.group(1), m.group(2)))

    # de-dupe while preserving order
    seen = set()
    ordered = []
    for t in ids:
        if t not in seen:
            seen.add(t)
            ordered.append(t)
    return ordered

# -------- CSV reading utilities --------
def read_csv_auto(csv_bytes: bytes) -> pd.DataFrame:
    """
    DW datasets can be comma- or tab-separated. Try auto detection first,
    then fall back to tabs explicitly.
    """
    # try pandas engine='python' sep=None (sniff)
    try:
        return pd.read_csv(io.BytesIO(csv_bytes), engine="python", sep=None)
    except Exception:
        pass
    # try tab
    try:
        return pd.read_csv(io.BytesIO(csv_bytes), sep="\t")
    except Exception:
        # last resort: raw decode & split (will at least show something)
        text = csv_bytes.decode("utf-8", errors="replace")
        lines = [ln.split("\t") for ln in text.splitlines()]
        return pd.DataFrame(lines[1:], columns=lines[0] if lines else [])

def tidy_headers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().replace("\xa0"," ").replace("\u2009"," ").replace("  "," ") for c in df.columns]
    return df

def classify_chart(df: pd.DataFrame) -> str:
    """
    Heuristic labelling to name files nicely.
    - Timeseries: first column looks like Date or contains many '-' (e.g., 2021-06)
    - Metros table: has 'Location' and 'Average property value'
    - Regions changes: has a 'Region' (or similar) plus columns with 'change'
    """
    cols = [c.lower() for c in df.columns]
    if cols:
        if cols[0].startswith("date") or "date" in cols[0]:
            return "timeseries"
    if "location" in cols and "average property value" in cols:
        return "metros"
    if any("region" in c for c in cols) and any("change" in c for c in cols):
        return "regions"
    if any("3-month change" in c for c in cols) and ("tla" in cols or "suburb" in cols):
        return "suburbs"
    return "chart"

def save_both(df: pd.DataFrame, basepath_no_ext: str):
    """Save CSV (utf-8-sig) and XLSX. Adds suffix if target file is locked."""
    csv_path = basepath_no_ext + ".csv"
    xlsx_path = basepath_no_ext + ".xlsx"

    def _attempt(path, writer):
        for i in range(3):
            try:
                return writer(path)
            except PermissionError:
                # file open in Excel; write with a suffix
                path = basepath_no_ext + f"_{int(time.time())}.csv" if path.endswith(".csv") else basepath_no_ext + f"_{int(time.time())}.xlsx"
        raise

    _attempt(csv_path, lambda p: df.to_csv(p, index=False, encoding="utf-8-sig", lineterminator="\n"))
    _attempt(xlsx_path, lambda p: df.to_excel(p, index=False))

    print(f"Saved -> {csv_path}")
    print(f"Saved -> {xlsx_path}")

# -------- main --------
def main(article_url: str):
    sess = get_session()
    print("Opening article:", article_url)
    r = sess.get(article_url, timeout=30)
    r.raise_for_status()

    charts = find_all_datawrappers(r.text)
    if not charts:
        raise RuntimeError("No Datawrapper charts found on the page.")

    print("Found Datawrapper charts:", charts)

    for idx, (chart_id, ver) in enumerate(charts, start=1):
        dataset_url = f"https://datawrapper.dwcdn.net/{chart_id}/{ver}/dataset.csv"
        print(f"[{idx}/{len(charts)}] Fetching: {dataset_url}")
        cr = sess.get(dataset_url, timeout=30)
        cr.raise_for_status()

        # read & tidy
        df = read_csv_auto(cr.content)
        df = tidy_headers(df)

        # classify & name
        label = classify_chart(df)
        base = os.path.join(OUT_DIR, f"oneroof_{label}_{chart_id}")

        # save both formats
        save_both(df, base)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--article", default=ARTICLE_URL, help="OneRoof article URL")
    args = ap.parse_args()
    main(args.article)
