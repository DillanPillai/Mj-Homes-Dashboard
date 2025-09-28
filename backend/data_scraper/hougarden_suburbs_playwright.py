#!/usr/bin/env python3
import csv, re, random, time
from typing import List, Dict, Tuple, Optional
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout, Error as PWError, Page

# -------- CONFIG --------
BASE = "https://www.hougarden.com"
START_URL = BASE + "/nz/suburbs/order-asc_page-1"
HEADLESS = False
SLOW_MS  = 60
WAIT_NAV = "domcontentloaded"
OUT_CSV  = "hougarden_suburbs.csv"
DEBUG    = True

MAX_EMPTY_RELOADS = 2
MAX_NEXT_RETRIES  = 5             # retries per page when moving forward
PAUSE_MIN_MS, PAUSE_MAX_MS = 220, 520

RE_MEDIAN  = re.compile(r"Median(?:\s+sales)?\s+price\s*\$?([\d,]+|-)", re.I)
RE_FORSALE = re.compile(r"For\s*sale[:\s]*([0-9]+|-)", re.I)
RE_SOLD    = re.compile(r"Sold[:\s]*([0-9]+|-)", re.I)

def clean_num(s: str) -> str:
    s = (s or "").strip()
    if s in ("", "-"): return "-"
    return re.sub(r"[^\d]", "", s)

def extract_slug_and_id(href: str) -> Tuple[str, str]:
    last = href.rstrip("/").split("/")[-1]
    m = re.match(r"(.+)-(\d+)$", last)
    if m: return m.group(1), m.group(2)
    return last, ""

def is_listing_url(url: str) -> bool:
    return "/nz/suburbs/" in urlsplit(url).path

def human_pause(page: Page, lo=PAUSE_MIN_MS, hi=PAUSE_MAX_MS):
    page.wait_for_timeout(random.randint(lo, hi))

def deep_scroll(page: Page, passes: int = 2):
    try:
        for _ in range(passes):
            page.evaluate("window.scrollTo(0, 0)")
            human_pause(page, 120, 200)
            doc_h = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
            y = 0
            while y < doc_h:
                y += 900
                page.evaluate("y => window.scrollTo(0, y)", y)
                page.wait_for_timeout(120)
                doc_h = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
            page.wait_for_timeout(260)
    except PWError:
        pass

def looks_like_404(page: Page) -> bool:
    try:
        txt = (page.inner_text("body", timeout=2000) or "").lower()
        return "404" in txt and ("页面找不到" in txt or "page not found" in txt)
    except Exception:
        return False

def wait_for_cards(page: Page, timeout_ms=12000) -> bool:
    try:
        page.wait_for_selector("a[href*='/nz/suburb/']", timeout=timeout_ms)
        return True
    except PWTimeout:
        return False

def ensure_loaded(page: Page, page_num: int) -> bool:
    if looks_like_404(page):
        if DEBUG: print("  ↪ landed on 404 page; going back …")
        try: page.go_back(wait_until=WAIT_NAV)
        except Exception: pass
        page.wait_for_timeout(500)
        return False

    deep_scroll(page)
    if wait_for_cards(page): return True

    for i in range(MAX_EMPTY_RELOADS):
        if DEBUG: print(f"  ↪ no cards yet on page {page_num}; reload {i+1}/{MAX_EMPTY_RELOADS} …")
        page.reload(wait_until=WAIT_NAV)
        human_pause(page)
        if looks_like_404(page):
            if DEBUG: print("  ↪ reload hit 404; going back …")
            try: page.go_back(wait_until=WAIT_NAV)
            except Exception: pass
            return False
        deep_scroll(page)
        if wait_for_cards(page): return True

    try:
        page.screenshot(path=f"hougarden_debug_page{page_num}.png", full_page=True)
        if DEBUG: print(f"  ↪ saved screenshot hougarden_debug_page{page_num}.png")
    except PWError:
        pass
    return False

def read_one_page(page: Page) -> List[Dict[str, str]]:
    links = page.locator("a[href*='/nz/suburb/']")
    cnt = links.count()
    if DEBUG: print(f"  ↪ found {cnt} suburb links")
    rows, seen = [], set()
    for i in range(cnt):
        a = links.nth(i)
        href = a.get_attribute("href") or ""
        if "/nz/suburb/" not in href:
            continue
        slug, suburb_id = extract_slug_and_id(href)
        if slug in seen:
            continue
        seen.add(slug)

        container = a.locator("xpath=ancestor::div[contains(@class,'card') or contains(@class,'Card') or contains(@class,'item')][1]")
        if container.count() == 0:
            container = a.locator("xpath=ancestor::div[1]")
        text = (container.inner_text() or "").strip()

        name = slug.replace("-", " ").title()
        first = text.split("\n", 1)[0].strip()
        if first and not first.lower().startswith("median"):
            name = first

        median = for_sale = sold = "-"
        m = RE_MEDIAN.search(text)
        if m: median = clean_num(m.group(1))
        m = RE_FORSALE.search(text)
        if m: for_sale = clean_num(m.group(1))
        m = RE_SOLD.search(text)
        if m: sold = clean_num(m.group(1))

        rows.append({
            "suburb_name": name,
            "suburb_slug": slug,
            "suburb_id": suburb_id,
            "median_price_nzd": median,
            "for_sale": for_sale,
            "sold_last_12m": sold,
        })
    return rows

def detect_max_pages(page: Page) -> Optional[int]:
    try:
        anchors = page.locator("a[href*='order-asc_page-']")
        n = anchors.count()
        maxp = 0
        for i in range(n):
            href = anchors.nth(i).get_attribute("href") or ""
            m = re.search(r"order-asc_page-(\d+)", href)
            if m:
                maxp = max(maxp, int(m.group(1)))
        return maxp or None
    except Exception:
        return None

def click_pager_href(page: Page, next_num: int) -> bool:
    sel_variants = [
        f"a[href$='/nz/suburbs/order-asc_page-{next_num}']",
        f"a[href*='/nz/suburbs/order-asc_page-{next_num}']",
        f"a[href$='order-asc_page-{next_num}']",
        f"a[href*='order-asc_page-{next_num}']",
    ]
    for where in ("bottom","top"):
        if where=="bottom":
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        else:
            page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(200)
        for sel in sel_variants:
            try:
                loc = page.locator(sel).first
                if loc and loc.is_visible():
                    if DEBUG: print(f"  ↪ clicking pager via href: {sel}")
                    with page.expect_navigation(wait_until=WAIT_NAV, timeout=25000):
                        loc.click()
                    return True
            except Exception:
                continue
    return False

def advance_with_retries(page: Page, cur_page_num: int) -> bool:
    """
    Try to reach next page with multiple strategies & retries.
    Returns True if we ended up on a listing page for next page.
    """
    next_num = cur_page_num + 1
    next_url = f"{BASE}/nz/suburbs/order-asc_page-{next_num}"

    for attempt in range(1, MAX_NEXT_RETRIES + 1):
        if DEBUG: print(f"— advance to page {next_num}: attempt {attempt}")

        # 1) Try clicking by href
        try:
            if click_pager_href(page, next_num):
                if looks_like_404(page):
                    if DEBUG: print("  ↪ landed on 404 after click; going back & retry …")
                    try: page.go_back(wait_until=WAIT_NAV)
                    except Exception: pass
                else:
                    return True
        except Exception:
            pass

        # 2) Fallback: direct goto with backoff, then verify
        try:
            jitter = random.uniform(0.2, 0.6) + attempt * 0.2
            time.sleep(jitter)
            if DEBUG: print(f"  ↪ fallback goto -> {next_url}")
            page.goto(next_url, wait_until=WAIT_NAV, timeout=30000)
            if looks_like_404(page):
                if DEBUG: print("  ↪ goto hit 404; retrying …")
                continue
            # ensure cards exist
            if ensure_loaded(page, next_num):
                return True
        except Exception:
            continue

    return False

def open_browser():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MS)
    context = browser.new_context(
        viewport={"width": 1280, "height": 900},
        user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"),
        locale="en-NZ",
        extra_http_headers={"Accept-Language": "en-NZ,en;q=0.9","Referer": BASE + "/nz/"},
    )
    page = context.new_page()
    return p, browser, context, page

def crawl_all():
    p, browser, context, page = open_browser()
    try:
        if DEBUG: print("Opening", START_URL)
        page.goto(START_URL, wait_until=WAIT_NAV, timeout=60000)
        human_pause(page)
        if not ensure_loaded(page, 1):
            print("[page 1] failed to load cards; exiting.")
            return

        max_pages = detect_max_pages(page) or 200
        if DEBUG: print(f"Detected max pages: {max_pages}")

        # open CSV (append) and write header once
        write_header = True
        with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(
                f,
                fieldnames=["suburb_name","suburb_slug","suburb_id","median_price_nzd","for_sale","sold_last_12m"],
            )
            w.writeheader()

        total = 0
        page_num = 1

        while page_num <= max_pages:
            rows = read_one_page(page)
            if not rows:
                if DEBUG: print("  ↪ page looked empty; reload once …")
                page.reload(wait_until=WAIT_NAV)
                human_pause(page)
                if not ensure_loaded(page, page_num):
                    if DEBUG: print(f"[page {page_num}] still empty; stopping.")
                    break
                rows = read_one_page(page)
                if not rows:
                    if DEBUG: print(f"[page {page_num}] still empty after reload; stopping.")
                    break

            # append incrementally
            with open(OUT_CSV, "a", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(
                    f,
                    fieldnames=["suburb_name","suburb_slug","suburb_id","median_price_nzd","for_sale","sold_last_12m"],
                )
                w.writerows(rows)

            total += len(rows)
            print(f"[page {page_num}] {len(rows)} rows, total {total}")

            if page_num >= max_pages:
                break

            if not advance_with_retries(page, page_num):
                if DEBUG: print("No further pages reachable; done.")
                break

            if not ensure_loaded(page, page_num + 1):
                if DEBUG: print(f"[page {page_num+1}] failed to load after advance; stopping.")
                break

            page_num += 1

        print(f"Done. Saved {total} suburbs to {OUT_CSV}")

    except (PWTimeout, PWError) as e:
        print("Playwright error:", e)
    finally:
        try:
            context.close(); browser.close(); p.stop()
        except Exception:
            pass

if __name__ == "__main__":
    crawl_all()
