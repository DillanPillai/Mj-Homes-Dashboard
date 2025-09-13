#!/usr/bin/env python3
from playwright.sync_api import sync_playwright

URL = "https://www.hougarden.com/nz/suburbs/order-asc_page-1"
HEADLESS = False
SLOW_MS = 60
WAIT_NAV = "domcontentloaded"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MS)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0.0.0 Safari/537.36"),
            locale="en-NZ",
            extra_http_headers={
                "Accept-Language": "en-NZ,en;q=0.9",
                "Referer": "https://www.hougarden.com/nz/",
            },
        )
        page = context.new_page()
        print("Opening:", URL)
        page.goto(URL, wait_until=WAIT_NAV, timeout=60000)

        # gentle scroll to trigger lazy content and footer pager
        def deep_scroll(p, passes=2):
            for _ in range(passes):
                p.evaluate("window.scrollTo(0, 0)")
                p.wait_for_timeout(300)
                p.evaluate("""
                    () => {
                        const h = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
                        let y = 0;
                        function step() {
                            y += 800;
                            window.scrollTo(0, y);
                        }
                        for (let i = 0; i < Math.ceil(h/800); i++) step();
                    }
                """)
                p.wait_for_timeout(400)

        deep_scroll(page, passes=2)

        # Collect likely pagination blocks
        selectors = [
            ".ant-pagination",
            "nav .ant-pagination",
            "nav:has(.pagination)",
            ".pagination",
            "nav[role='navigation']",
        ]

        print("\n=== Pagination blocks present (counts) ===")
        for sel in selectors:
            try:
                cnt = page.locator(sel).count()
                print(f"{sel}: {cnt}")
            except Exception:
                print(f"{sel}: error")

        # Print the first few pagination blocks' HTML
        print("\n=== First .ant-pagination outerHTML (up to 2 blocks) ===")
        try:
            pagers = page.locator(".ant-pagination")
            n = min(pagers.count(), 2)
            for i in range(n):
                html = pagers.nth(i).evaluate("el => el.outerHTML")
                print(f"\n--- .ant-pagination [{i}] ---")
                print(html[:3000])  # truncate to avoid flooding
        except Exception as e:
            print("No .ant-pagination or error:", e)

        # Print any anchors that look like page links (…order-asc_page-*)
        print("\n=== All anchors with href containing 'order-asc_page-' ===")
        try:
            links = page.locator("a[href*='order-asc_page-']")
            count = links.count()
            print(f"count: {count}")
            for i in range(min(count, 20)):
                href = links.nth(i).get_attribute("href")
                txt = (links.nth(i).inner_text() or "").strip()
                print(f"{i:02d}: text='{txt}'  href='{href}'")
        except Exception as e:
            print("Error scanning anchors:", e)

        # Try to show the active page item
        try:
            active_txt = page.locator("li.ant-pagination-item-active").inner_text().strip()
            print(f"\nActive pager item text: {active_txt}")
        except Exception:
            print("\nActive pager item not found.")

        # Save a screenshot to inspect visually
        try:
            page.screenshot(path="hougarden_pager_debug.png", full_page=True)
            print("\nSaved screenshot: hougarden_pager_debug.png")
        except Exception:
            pass

        context.close()
        browser.close()

if __name__ == "__main__":
    main()
