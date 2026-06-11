"""
FT Workspace v2.0 - M3: Alibaba International Content Generator

Generate Alibaba International Station content:
- SEO titles (3 variants, 128 chars max)
- Full detail page content

Usage:
    from src.m3_seo.alibaba_generator import AlibabaContentGenerator
    gen = AlibabaContentGenerator()
    result = gen.generate_titles("GF-001")
    result = gen.generate_detail("GF-001")
    result = gen.generate_all("GF-001")
"""

import json
import os
import re
from typing import Optional
from datetime import datetime

from src.core.database import FTDatabase
from src.core.llm_client import LLMClient
from src.utils.prompts import load_prompt, fill_prompt, build_product_data


def _clean_llm_response(text: str) -> str:
    """Clean common LLM wrapper artifacts."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    return text.strip()


def _parse_numbered_list(text: str) -> list[str]:
    """Parse a numbered list from LLM response."""
    items = []
    for line in text.split("\n"):
        line = line.strip()
        match = re.match(r'^[\d\-\*\•]+\.[\s)]*\s*(.*)', line) or \
                re.match(r'^[\-\*\•]\s+(.*)', line)
        if match:
            item = match.group(1).strip()
            if item and len(item) > 5:
                items.append(item)
    return items


class AlibabaContentGenerator:
    """Generate Alibaba International Station content."""

    def __init__(
        self,
        db: Optional[FTDatabase] = None,
        llm: Optional[LLMClient] = None,
    ):
        self._db = db
        self._llm = llm

    def _get_db(self) -> tuple[FTDatabase, bool]:
        if self._db:
            return self._db, False
        db = FTDatabase()
        return db, True

    def _get_llm(self) -> LLMClient:
        if self._llm:
            return self._llm
        return LLMClient(scenario="seo_content")

    def generate_titles(
        self,
        product_code: str,
        count: int = 3,
        save: bool = True,
    ) -> dict:
        """
        Generate SEO titles for Alibaba.

        Args:
            product_code: Product code (e.g., 'GF-001').
            count: Number of titles (default 3).
            save: Save to database.

        Returns:
            {"titles": [...], "saved": bool, "error": str or None}
        """
        result = {"titles": [], "saved": False, "error": None}

        db, should_close = self._get_db()
        try:
            product = db.product_get(product_code)
            if not product:
                result["error"] = f"Product {product_code} not found"
                return result

            data = build_product_data(product)
            template = load_prompt("seo/alibaba_title")
            filled = fill_prompt(template, data)

            llm = self._get_llm()
            response = llm.chat(filled, max_tokens=500, temperature=0.7)
            response = _clean_llm_response(response)

            titles = _parse_numbered_list(response)
            if not titles:
                titles = [
                    line.strip()
                    for line in response.split("\n")
                    if line.strip() and len(line.strip()) > 10
                ]

            titles = titles[:count]
            while len(titles) < count:
                titles.append(f"SEO Title {len(titles) + 1} (placeholder)")

            result["titles"] = titles

            if save and len(titles) >= 3:
                db.execute(
                    "UPDATE products SET seo_title_1 = ?, seo_title_2 = ?, "
                    "seo_title_3 = ?, alibaba_detail_status = 'generated', "
                    "updated_at = datetime('now') WHERE product_code = ?",
                    (titles[0], titles[1] if len(titles) > 1 else "",
                     titles[2] if len(titles) > 2 else "", product_code)
                )
                db.commit()
                result["saved"] = True

        except Exception as e:
            result["error"] = str(e)
        finally:
            if should_close:
                db.close()

        return result

    def generate_detail(
        self,
        product_code: str,
        save: bool = True,
    ) -> dict:
        """
        Generate Alibaba detail page content.

        Returns:
            {"content": str, "length": int, "saved": bool, "error": str or None}
        """
        result = {"content": "", "length": 0, "saved": False, "error": None}

        db, should_close = self._get_db()
        try:
            product = db.product_get(product_code)
            if not product:
                result["error"] = f"Product {product_code} not found"
                return result

            data = build_product_data(product)
            template = load_prompt("seo/alibaba_detail")
            filled = fill_prompt(template, data)

            llm = self._get_llm()
            response = llm.chat(filled, max_tokens=4000, temperature=0.7)
            response = _clean_llm_response(response)

            result["content"] = response
            result["length"] = len(response)

            if save:
                db.execute(
                    "UPDATE products SET alibaba_detail_status = 'generated', "
                    "updated_at = datetime('now') WHERE product_code = ?",
                    (product_code,)
                )
                db.commit()
                result["saved"] = True

        except Exception as e:
            result["error"] = str(e)
        finally:
            if should_close:
                db.close()

        return result

    def generate_all(
        self,
        product_code: str,
        save: bool = True,
    ) -> dict:
        """
        Generate all Alibaba content for a product.

        Returns:
            Dict with titles, detail, and summary.
        """
        result = {"product_code": product_code, "titles": {}, "detail": {}}

        result["titles"] = self.generate_titles(product_code, save=save)
        result["detail"] = self.generate_detail(product_code, save=save)

        return result

    def export_to_file(
        self,
        product_code: str,
        output_dir: Optional[str] = None,
    ) -> dict:
        """
        Export generated content to files.

        Returns:
            Dict of {type: file_path}.
        """
        if output_dir is None:
            project_root = os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))))
            output_dir = os.path.join(
                project_root, "output", "seo_content", product_code, "alibaba")

        os.makedirs(output_dir, exist_ok=True)

        db, should_close = self._get_db()
        result = {}

        try:
            product = db.product_get(product_code)
            if not product:
                raise ValueError(f"Product {product_code} not found")

            # SEO titles
            titles = [product.get(f"seo_title_{i}") for i in range(1, 4)]
            titles = [t for t in titles if t]
            if titles:
                path = os.path.join(output_dir, "seo_titles.txt")
                with open(path, "w", encoding="utf-8") as f:
                    for i, t in enumerate(titles, 1):
                        f.write(f"{i}. {t}\n")
                result["seo_titles"] = path

            # Check for alibaba detail in DB or regenerate
            detail = product.get("alibaba_detail")
            if detail:
                path = os.path.join(output_dir, "detail_page.md")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(detail)
                result["detail_page"] = path

        finally:
            if should_close:
                db.close()

        return result
