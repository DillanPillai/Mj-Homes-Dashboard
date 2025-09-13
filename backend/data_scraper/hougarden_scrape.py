#!/usr/bin/env python3
import re
import sys
import csv
import time
from urllib.parse import urljoin, urlparse
from urllib import robotparser

import requests
from bs4 import BeautifulSoup

# ---------- CONFIG ----------
BASE = "https://www.hougarden.com"          # root (no /nz here)
ROBOTS_PATH = "/nz/robots.txt"               # robots lives under /nz
LISTING_PATH_TPL = "/nz/suburbs/order-asc_page-{page}"
USER_AGENT = "MJHomesResearchBot/1.0 (+contact: you@example.com)"
RATE_LIMIT_SEC = 1.5                         # ~1 req / 1.5s (be polite)
TIMEOUT = 20
MAX_EMPTY_PAGES = 1                          # stop after this many empty pages

# ---------- robots.txt ----------
rp = robotparser.RobotFileParser()
rp.set_url(urljoin(BASE, ROBOTS_PATH))
rp.read()

# Disallow patterns from robots.txt you showed
disallow_re = [
    re.compile(r"_rsc="),          # *_rsc=*
    re.compile(r"/[^/]*\.php/"),   # /*.php/*
]

def allowed(url: str) -> bool:
    u = urlparse(url)
    if u.netloc != urlparse(BASE).netloc:
        return False
    path_q = u.path + ("?" + u.query if u.query else "")
    if any(p.search(path_q) for p in disallow_re):
        return False
    return rp.can_fetch(USER_AGENT, url)

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-NZ,en;q=0.9",
    "Referer": "https://www.hougarden.com/nz/"
})


def get(url: str) -> str | None:
    """Fetch HTML with polite rate limit, minor header set, 404 trailing-slash retry."""
    if not allowed(url):
        print(f"[blocked] {url}")
        return None
    time.sleep(RATE_LIMIT_SEC)
    try:
        r = session.get(
            url,
            timeout=TIMEOUT,
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-NZ,en;q=0.9",
                "Referer": BASE + "/nz/",
            },
            allow_redirects=True,
        )
        if r.status_code == 404 and not url.endswith("/"):
            # some servers expect a trailing slash on directory-like URLs
            r = session.get(url + "/", timeout=TIMEOUT, allow_redirects=True)
        if r.status_code == 200:
            return r.text
        print(f"[{r.status_code}] {url}")
        return None
    except requests.RequestException as e:
        print(f"[error] {url}: {e}")
        return None

# ---------- parsing ----------
SUBURB_HREF_RE = re.compile(r"^/nz/suburbs/[^/?#]+/?$")

def extract_suburbs(html: str) -> list[dict]:
    """Extract suburb anchor links by URL pattern; resilient to class changes."""
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for a in soup.select("a[href]"):
        href = a.get("href", "").strip()
        if SUBURB_HREF_RE.match(href):
            name = a.get_text(" ", strip=True)
            slug = href.rstrip("/").split("/")[-1]
            if not name:
                name = slug.replace("-", " ").title()
            url = urljoin(BASE, href)
            rows.append({"suburb_name": name, "suburb_slug": slug, "url": url})
    return rows

def crawl_suburb_pages(start_page: int, max_pages: int, out_csv: str = "hougarden_suburbs.csv"):
    seen = set()
    empty_in_a_row = 0
    total_saved = 0

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["suburb_name", "suburb_slug", "url"])
        w.writeheader()

        for i in range(start_page, start_page + max_pages):
            page_url = urljoin(BASE, LISTING_PATH_TPL.format(page=i))
            html = get(page_url)
            if not html:
                empty_in_a_row += 1
                if empty_in_a_row > MAX_EMPTY_PAGES:
                    break
                continue

            rows = extract_suburbs(html)
            new_rows = [r for r in rows if r["suburb_slug"] not in seen]
            for r in new_rows:
                w.writerow(r)
                seen.add(r["suburb_slug"])
            total_saved += len(new_rows)

            print(f"[page {i}] found {len(rows)} / new {len(new_rows)} / total {total_saved}")

            if len(new_rows) == 0:
                empty_in_a_row += 1
                if empty_in_a_row > MAX_EMPTY_PAGES:
                    break
            else:
                empty_in_a_row = 0

    print(f"Done. Saved {total_saved} suburbs to {out_csv}")

if __name__ == "__main__":
    # Usage: python hougarden_scrape.py [start_page] [max_pages]
    START_PAGE = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    MAX_PAGES  = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    crawl_suburb_pages(START_PAGE, MAX_PAGES)
