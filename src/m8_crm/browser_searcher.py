"""
M8: 真实客户搜索器 (Playwright 版)
通过浏览器自动化搜索 Bing/Google，支持 SOCKS5 代理。
搜索引擎可能弹验证码，用户手动解决后脚本自动继续。

用法:
    from src.m8_crm.browser_searcher import BrowserSearcher
    searcher = BrowserSearcher(proxy='socks5://127.0.0.1:10808')
    results = searcher.search('agricultural tools importer Nigeria', max_results=5)
"""
import re
import time
from urllib.parse import quote_plus, urlparse
from typing import Optional


class BrowserSearcher:
    """通过 Playwright 浏览器搜索真实公司"""

    BLOCKED_DOMAINS = {
        "bing.com", "microsoft.com", "google.com", "youtube.com",
        "facebook.com", "wikipedia.org", "twitter.com", "instagram.com",
        "linkedin.com", "amazon.com", "ebay.com",
    }

    def __init__(self, proxy: Optional[str] = None, headless: bool = False):
        self.proxy = proxy
        self.headless = headless

    def search(self, query: str, max_results: int = 10) -> list[dict]:
        """搜索并返回结构化结果"""
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            launch_args = {
                "headless": self.headless,
                "args": ["--disable-blink-features=AutomationControlled"],
            }
            if self.proxy:
                launch_args["proxy"] = {"server": self.proxy}

            browser = p.chromium.launch(**launch_args)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                locale="en-US",
            )
            page = context.new_page()

            results = []

            # 尝试 Bing
            try:
                results = self._search_bing(page, query, max_results)
            except Exception as e:
                print(f"[BrowserSearcher] Bing failed: {e}")

            # 如果 Bing 没结果，尝试 Google
            if not results:
                try:
                    results = self._search_google(page, query, max_results)
                except Exception as e:
                    print(f"[BrowserSearcher] Google failed: {e}")

            browser.close()
            return results

    def _search_bing(self, page, query: str, max_results: int) -> list[dict]:
        """Bing 搜索"""
        encoded = quote_plus(query)
        url = f"https://www.bing.com/search?q={encoded}&count={max_results}&setmkt=en-US&setlang=en"
        page.goto(url, timeout=30000)
        page.wait_for_timeout(3000)

        # 检查是否有验证码
        body_text = page.inner_text("body").lower()
        if "challenge" in body_text or "captcha" in body_text:
            print("[BrowserSearcher] Bing CAPTCHA detected! Please solve it in the browser window...")
            # 等待用户手动解决（最多 60 秒）
            for i in range(60):
                time.sleep(1)
                try:
                    if page.query_selector_all("li.b_algo"):
                        break
                except:
                    pass

        return self._parse_bing_results(page, max_results)

    def _search_google(self, page, query: str, max_results: int) -> list[dict]:
        """Google 搜索"""
        encoded = quote_plus(query)
        url = f"https://www.google.com/search?q={encoded}&num={max_results}&hl=en"
        page.goto(url, timeout=30000)
        page.wait_for_timeout(3000)

        body_text = page.inner_text("body").lower()
        if "sorry" in body_text or "captcha" in body_text:
            print("[BrowserSearcher] Google CAPTCHA detected! Please solve it in the browser window...")
            for i in range(60):
                time.sleep(1)
                try:
                    if page.query_selector_all("div.g"):
                        break
                except:
                    pass

        return self._parse_google_results(page, max_results)

    def _parse_bing_results(self, page, max_results: int) -> list[dict]:
        """解析 Bing 搜索结果"""
        results = []
        items = page.query_selector_all("li.b_algo")

        for item in items[:max_results]:
            link_el = item.query_selector("h2 a")
            snippet_el = item.query_selector(".b_caption p, .b_algoSlug")

            if not link_el:
                continue

            href = link_el.get_attribute("href") or ""
            if not href.startswith("http"):
                continue

            domain = urlparse(href).netloc
            if any(d in domain for d in self.BLOCKED_DOMAINS):
                continue

            title = link_el.inner_text().strip()
            snippet = snippet_el.inner_text().strip()[:500] if snippet_el else ""

            emails = re.findall(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', snippet)
            phones = re.findall(r'\+?\d[\d\s\-()]{7,}\d', snippet)

            results.append({
                "name": title,
                "url": href,
                "domain": domain,
                "snippet": snippet,
                "emails_from_search": emails[:3],
                "phones_from_search": phones[:3],
                "source": "bing_browser",
            })

        return results

    def _parse_google_results(self, page, max_results: int) -> list[dict]:
        """解析 Google 搜索结果"""
        results = []
        items = page.query_selector_all("div.g")

        for item in items[:max_results]:
            link_el = item.query_selector("a[href]")
            title_el = item.query_selector("h3")
            snippet_el = item.query_selector("div[data-sncf], span.st, div.VwiC3b")

            if not link_el:
                continue

            href = link_el.get_attribute("href") or ""
            if not href.startswith("http"):
                continue

            domain = urlparse(href).netloc
            if any(d in domain for d in self.BLOCKED_DOMAINS):
                continue

            title = title_el.inner_text().strip() if title_el else link_el.inner_text().strip()
            snippet = snippet_el.inner_text().strip()[:500] if snippet_el else ""

            emails = re.findall(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', snippet)
            phones = re.findall(r'\+?\d[\d\s\-()]{7,}\d', snippet)

            results.append({
                "name": title,
                "url": href,
                "domain": domain,
                "snippet": snippet,
                "emails_from_search": emails[:3],
                "phones_from_search": phones[:3],
                "source": "google_browser",
            })

        return results


if __name__ == "__main__":
    searcher = BrowserSearcher(proxy="socks5://127.0.0.1:10808", headless=False)
    results = searcher.search("agricultural tools importer Nigeria", max_results=5)
    print(f"\nFound {len(results)} results:")
    for r in results:
        print(f"  {r['name']}")
        print(f"    {r['url'][:80]}")
        print(f"    {r['snippet'][:100]}")
        print()
