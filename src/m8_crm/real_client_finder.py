"""
M8: 真实客户搜索器
功能：通过 Google 搜索 + 网页抓取，找到目标市场中真实存在的农具/五金进口商、分销商。
提取公司名、网站、邮箱、电话、WhatsApp、LinkedIn 等真实联系方式。

用法:
    from src.m8_crm.real_client_finder import RealClientFinder
    finder = RealClientFinder()
    results = finder.search_companies("agricultural tools importer Nigeria", max_results=10)
"""

import re
import time
import random
import json
from typing import Optional
from urllib.parse import quote_plus, urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class RealClientFinder:
    """通过搜索引擎和网页抓取，找真实存在的外贸客户"""

    # 请求头，模拟浏览器
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    # 常用搜索模板：针对不同市场生成搜索关键词
    SEARCH_TEMPLATES = {
        "Africa": [
            "{product} importer {country}",
            "{product} distributor {country} contact",
            "{product} wholesale {country} email whatsapp",
            "agricultural tools supplier {country}",
            "farm equipment company {country}",
        ],
        "Europe": [
            "{product} importer {country}",
            "{product} distributor {country} contact email",
            "{product} wholesale {country}",
            "garden tools company {country}",
            "agricultural supply {country}",
        ],
        "default": [
            "{product} importer {country} contact",
            "{product} distributor {country}",
            "{product} wholesale {country} email",
        ],
    }

    # 产品关键词（用于搜索）
    DEFAULT_PRODUCTS = [
        "agricultural hand tools",
        "garden tools",
        "farm tools",
    ]

    def __init__(self, proxy: Optional[str] = None):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}

    # ── 主入口 ──────────────────────────────────────────────

    def search_companies(
        self,
        query: str,
        country: str = "",
        max_results: int = 10,
        market: str = "default",
    ) -> list[dict]:
        """
        搜索真实公司。

        Args:
            query: 用户自定义搜索词，如 "agricultural tools importer Nigeria"
            country: 目标国家（可选，用于模板搜索补充）
            max_results: 最多返回几条
            market: 市场区域 (Africa / Europe / default)

        Returns:
            公司信息列表，每条包含 name, website, snippet, source_url
        """
        all_queries = [query]

        # 如果指定了国家，用模板补充搜索词
        if country:
            templates = self.SEARCH_TEMPLATES.get(market, self.SEARCH_TEMPLATES["default"])
            for tpl in templates[:2]:  # 最多补充2个模板查询
                for product in self.DEFAULT_PRODUCTS[:1]:  # 用第一个产品词
                    q = tpl.format(product=product, country=country)
                    if q not in all_queries:
                        all_queries.append(q)

        seen_domains = set()
        results = []

        for q in all_queries:
            if len(results) >= max_results:
                break
            try:
                hits = self._google_search(q, num=min(10, max_results - len(results)))
                for hit in hits:
                    domain = urlparse(hit.get("url", "")).netloc
                    if domain and domain not in seen_domains:
                        seen_domains.add(domain)
                        results.append(hit)
                    if len(results) >= max_results:
                        break
            except Exception as e:
                print(f"[RealClientFinder] Search error for '{q}': {e}")
            # 避免被搜索引擎封IP
            time.sleep(random.uniform(1.5, 3.0))

        return results

    def extract_contact_from_url(self, url: str) -> dict:
        """
        访问一个公司网页，提取联系方式（邮箱、电话、WhatsApp、LinkedIn）。

        Args:
            url: 公司网站URL

        Returns:
            dict with keys: emails, phones, whatsapp, linkedin, page_title
        """
        result = {
            "url": url,
            "page_title": "",
            "emails": [],
            "phones": [],
            "whatsapp": [],
            "linkedin": [],
            "raw_text_snippet": "",
        }

        try:
            resp = self.session.get(url, timeout=30, allow_redirects=True)
            resp.raise_for_status()
            text = resp.text
            soup = BeautifulSoup(text, "lxml")

            # 页面标题
            if soup.title:
                result["page_title"] = soup.title.get_text(strip=True)[:200]

            # 全文提取联系方式
            page_text = soup.get_text(separator=" ", strip=True)

            # 邮箱
            emails = set(re.findall(
                r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}',
                page_text
            ))
            # 排除常见无用邮箱
            junk = {"example.com", "email.com", "test.com", "sentry.io",
                    "wixpress.com", "w3.org", "schema.org", "googleapis.com",
                    "google.com", "facebook.com", "youtube.com"}
            result["emails"] = [e for e in emails
                                if not any(j in e.lower() for j in junk)][:10]

            # 电话号码（国际格式）
            phones = set(re.findall(
                r'\+?\d[\d\s\-()]{7,}\d',
                page_text
            ))
            # 过滤掉太短或太长的
            result["phones"] = [p.strip() for p in phones
                                if 8 <= len(re.sub(r'\D', '', p)) <= 15][:10]

            # WhatsApp 链接
            wa_links = soup.find_all("a", href=re.compile(r'wa\.me|api\.whatsapp\.com|whatsapp'))
            for link in wa_links:
                href = link.get("href", "")
                wa_num = re.findall(r'\d{7,15}', href)
                if wa_num:
                    result["whatsapp"].append("+" + wa_num[0])
            # 从文本中提取 WhatsApp 号码（跟在 whatsapp 关键词后面）
            wa_text = re.findall(
                r'whatsapp[:\s]*\+?([\d\s\-()]{8,15})',
                page_text, re.IGNORECASE
            )
            for num in wa_text:
                clean = "+" + re.sub(r'\D', '', num)
                if clean not in result["whatsapp"] and len(clean) >= 9:
                    result["whatsapp"].append(clean)
            result["whatsapp"] = result["whatsapp"][:5]

            # LinkedIn
            linkedin_links = soup.find_all("a", href=re.compile(r'linkedin\.com'))
            for link in linkedin_links:
                href = link.get("href", "")
                if "/company/" in href or "/in/" in href:
                    result["linkedin"].append(href)
            result["linkedin"] = list(set(result["linkedin"]))[:3]

            # 保存一段文本摘要（用于后续AI分析）
            result["raw_text_snippet"] = page_text[:2000]

        except Exception as e:
            result["error"] = str(e)

        return result

    def search_and_extract(
        self,
        query: str,
        country: str = "",
        max_results: int = 8,
        market: str = "default",
        extract_contacts: bool = True,
    ) -> list[dict]:
        """
        一步到位：搜索公司 + 抓取联系方式。

        Args:
            query: 搜索词
            country: 目标国家
            max_results: 最多结果数
            market: 市场区域
            extract_contacts: 是否访问网页提取联系方式

        Returns:
            公司信息列表（含联系方式）
        """
        search_results = self.search_companies(query, country, max_results, market)

        if extract_contacts:
            for i, company in enumerate(search_results):
                url = company.get("url", "")
                if url:
                    try:
                        contact = self.extract_contact_from_url(url)
                        company.update(contact)
                    except Exception as e:
                        company["extract_error"] = str(e)
                    # 礼貌间隔
                    if i < len(search_results) - 1:
                        time.sleep(random.uniform(1.0, 2.0))

        return search_results

    # ── 内部方法 ──────────────────────────────────────────────

    def _google_search(self, query: str, num: int = 10) -> list[dict]:
        """
        通过 Bing 搜索获取真实公司结果（使用 curl 以支持 SOCKS5 代理）。
        """
        import subprocess
        from urllib.parse import quote_plus, urlparse
        encoded = quote_plus(query)
        url = f"https://www.bing.com/search?q={encoded}&count={num}"

        try:
            proxy = self.session.proxies.get("https", self.session.proxies.get("http", ""))
            cmd = ["curl", "-s", "-m", "20"]
            if proxy:
                cmd += ["--proxy", proxy]
            cmd += ["-H", f"User-Agent: {self.HEADERS['User-Agent']}"]
            cmd.append(url)
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
            if result.returncode != 0:
                print(f'[RealClientFinder] curl error: {result.stderr[:200]}')
                return []
        except Exception as e:
            print(f'[RealClientFinder] Search error: {e}')
            return []

        soup = BeautifulSoup(result.stdout, "html.parser")
        results = []

        for item in soup.select("li.b_algo"):
            link = item.select_one("h2 a")
            snippet_el = item.select_one(".b_caption p, .b_algoSlug")

            if not link:
                continue

            href = link.get("href", "")
            if not href.startswith("http"):
                continue

            domain = urlparse(href).netloc
            if any(d in domain for d in ["bing.com", "microsoft.com", "google.com",
                                          "youtube.com", "facebook.com", "wikipedia.org"]):
                continue

            title = link.get_text(strip=True)
            snippet = snippet_el.get_text(strip=True) if snippet_el else ""

            emails_in_snippet = re.findall(
                r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}',
                snippet
            )
            phones_in_snippet = re.findall(r'\+?\d[\d\s\-()]{7,}\d', snippet)

            results.append({
                "name": title,
                "url": href,
                "domain": domain,
                "snippet": snippet[:500],
                "emails_from_search": emails_in_snippet[:3],
                "phones_from_search": phones_in_snippet[:3],
                "source": "bing_search",
            })

        return results

    # ── 目录网站专用提取 ──────────────────────────────────────

    def extract_from_directory(self, url: str) -> list[dict]:
        """
        从常见外贸目录网站提取公司列表。
        支持: alibaba.com, made-in-china.com, globalsources.com 等
        """
        try:
            resp = self.session.get(url, timeout=30)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml")
            text = soup.get_text(separator=" ", strip=True)

            # 提取页面上所有公司相关信息
            companies = []

            # 通用：提取所有邮箱和电话
            all_emails = re.findall(
                r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', text
            )
            all_phones = re.findall(r'\+?\d[\d\s\-()]{8,15}\d', text)

            # 从页面结构提取（适配多种目录格式）
            # Alibaba 格式
            for item in soup.select(".company-name, .sc-company-name, h3 a, h2 a"):
                name = item.get_text(strip=True)
                href = item.get("href", "")
                if name and len(name) > 3:
                    companies.append({
                        "name": name,
                        "url": urljoin(url, href) if href else "",
                        "source": "directory",
                    })

            return companies

        except Exception as e:
            return [{"error": str(e)}]


# ── 快捷函数 ──────────────────────────────────────────────

def find_real_clients(
    country: str,
    product: str = "agricultural tools",
    max_results: int = 8,
    market: str = "default",
) -> list[dict]:
    """
    快捷入口：给定国家和产品，搜索真实客户。

    Args:
        country: 目标国家名（英文）
        product: 产品关键词（英文）
        max_results: 最多结果数
        market: 市场区域

    Returns:
        真实公司列表（含联系方式）
    """
    query = f"{product} importer {country} contact email"
    finder = RealClientFinder()
    return finder.search_and_extract(
        query=query,
        country=country,
        max_results=max_results,
        market=market,
        extract_contacts=True,
    )


if __name__ == "__main__":
    # 命令行测试
    import sys
    country = sys.argv[1] if len(sys.argv) > 1 else "Nigeria"
    product = sys.argv[2] if len(sys.argv) > 2 else "agricultural hand tools"
    max_r = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    print(f"🔍 Searching: {product} in {country} (max {max_r} results)")
    print("=" * 60)

    results = find_real_clients(country, product, max_r)

    for i, r in enumerate(results, 1):
        print(f"\n--- [{i}] {r.get('name', 'Unknown')} ---")
        print(f"  URL: {r.get('url', 'N/A')}")
        print(f"  Domain: {r.get('domain', 'N/A')}")
        if r.get("emails"):
            print(f"  Email: {', '.join(r['emails'][:3])}")
        elif r.get("emails_from_search"):
            print(f"  Email (from search): {', '.join(r['emails_from_search'][:3])}")
        if r.get("phones"):
            print(f"  Phone: {', '.join(r['phones'][:3])}")
        if r.get("whatsapp"):
            print(f"  WhatsApp: {', '.join(r['whatsapp'][:3])}")
        if r.get("linkedin"):
            print(f"  LinkedIn: {r['linkedin'][0]}")
        if r.get("snippet"):
            print(f"  Snippet: {r['snippet'][:150]}...")
