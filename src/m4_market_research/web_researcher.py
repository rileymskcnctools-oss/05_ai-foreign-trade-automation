"""
实时数据采集模块
在生成报告前搜索真实数据，提升报告时效性和可信度。
通过 HTTP 代理访问 Bing 搜索。
"""

import subprocess
import re
import urllib.parse
import base64


_PROXY = "http://127.0.0.1:10808"
_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def _curl_get(url: str, timeout: int = 12) -> str:
    """用 curl 通过代理请求 URL"""
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '--connect-timeout', '8', '--max-time', str(timeout),
             '-A', _UA, '-x', _PROXY, url],
            capture_output=True, text=True, timeout=timeout + 5
        )
        return result.stdout
    except Exception:
        return ''


def _test_proxy() -> bool:
    """测试代理是否可用"""
    html = _curl_get("https://www.google.com", timeout=8)
    return len(html) > 100


def _extract_bing_url(bing_redirect_url: str) -> str:
    """从 Bing 重定向 URL 中提取真实 URL"""
    # 格式: /ck/a?...&u=a1aHR0cHM6Ly...&ntb=1
    # u= 后面是 base64 编码的 URL，去掉前缀 "a1"
    m = re.search(r'[&?]u=a1([^&"]+)', bing_redirect_url)
    if m:
        try:
            decoded = base64.b64decode(m.group(1)).decode('utf-8', errors='ignore')
            if decoded.startswith('http'):
                return decoded
        except Exception:
            pass
    return ''


def _search_bing(query: str, max_results: int = 5) -> list[dict]:
    """Bing 搜索（通过代理）"""
    encoded = urllib.parse.quote(query)
    url = f"https://www.bing.com/search?q={encoded}&setlang=en&count={max_results + 5}"
    html = _curl_get(url, timeout=15)
    if not html or len(html) < 5000:
        return []

    results = []

    # 方法1: 找 b_algo 列表项，提取标题和摘要
    algo_blocks = re.findall(
        r'<li class="b_algo"[^>]*>(.*?)</li>',
        html, re.DOTALL
    )

    for block in algo_blocks[:max_results + 3]:
        # 提取标题链接
        title_match = re.search(r'<h2[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', block, re.DOTALL)
        if not title_match:
            continue

        raw_url, raw_title = title_match.group(1), title_match.group(2)
        title = re.sub(r'<[^>]+>', '', raw_url if not raw_title else raw_title).strip()

        # 解码 Bing 重定向 URL
        real_url = _extract_bing_url(raw_url)

        # 提取摘要
        snippet = ''
        snippet_match = re.search(r'<p[^>]*>(.*?)</p>', block, re.DOTALL)
        if snippet_match:
            snippet = re.sub(r'<[^>]+>', '', snippet_match.group(1)).strip()

        # 提取 cite 中的 URL 作为备用
        if not real_url:
            cite_match = re.search(r'<cite>(.*?)</cite>', block, re.DOTALL)
            if cite_match:
                real_url = re.sub(r'<[^>]+>', '', cite_match.group(1)).strip()

        if title and len(title) > 3:
            results.append({
                'title': title,
                'url': real_url or '',
                'snippet': snippet,
            })

        if len(results) >= max_results:
            break

    return results


def research_country_market(country: str, product: str = "agricultural tools") -> str:
    """
    搜索目标国家的市场实时数据，返回结构化文本供 AI 参考。
    """
    # 测试代理
    if not _test_proxy():
        return ""

    all_data = []

    # 搜索关键词
    queries = [
        f"{country} {product} market size import 2024 2025",
        f"{country} agricultural tools import tariff certification",
        f"{country} farm tools wholesale distributor importer",
    ]

    for query in queries:
        results = _search_bing(query, max_results=3)
        for r in results:
            text = r['snippet'] or r['title']
            if text:
                source = r['url'][:60] if r['url'] else r['title'][:40]
                all_data.append(f"[{source}] {text[:250]}")

    # 额外搜索
    extra_queries = [
        f"site:alibaba.com {country} {product} buyer import",
        f"{country} farm tools import duty certification requirement",
    ]
    for query in extra_queries:
        results = _search_bing(query, max_results=2)
        for r in results:
            text = r['snippet'] or r['title']
            if text:
                all_data.append(f"[{r['title'][:50]}] {text[:250]}")

    if not all_data:
        return ""

    # 组装上下文
    context = f"""## 实时网络搜索数据（来源: Bing, {len(all_data)}条）

以下是从互联网搜索到的关于 {country} {product} 市场的最新信息：

"""
    for i, item in enumerate(all_data[:10], 1):
        context += f"{i}. {item}\n"

    context += """
注意：以上数据来自实时网络搜索，请结合你的知识综合判断。
在报告中适当标注"根据最新网络数据"等来源说明。"""

    return context
