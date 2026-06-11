"""
FT Workspace v2.0 - M3: Independent Website Content Generator

Generate independent website (Shopify/WordPress) content:
- Meta Title (3 variants, 50-60 chars)
- Meta Description (3 variants, 150-160 chars)
- Product Description (150-250 words)

Usage:
    from src.m3_seo.website_generator import WebsiteContentGenerator
    gen = WebsiteContentGenerator()
    result = gen.generate_meta_titles("GF-001")
    result = gen.generate_description("GF-001")
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


def _parse_json_array(text: str) -> list:
    """Try to parse JSON array from LLM response."""
    # Find JSON array in text
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return []


def _parse_lines(text: str, min_len: int = 10) -> list[str]:
    """Parse non-empty lines as items."""
    return [
        line.strip()
        for line in text.split("\n")
        if line.strip() and len(line.strip()) > min_len
    ]


class WebsiteContentGenerator:
    """Generate independent website content."""

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

    def generate_meta_titles(
        self,
        product_code: str,
        count: int = 3,
        save: bool = True,
    ) -> dict:
        """
        Generate SEO meta titles for independent website.

        Returns:
            {"titles": [{"version": 1, "title": "...", "focus": "..."}, ...],
             "saved": bool, "error": str or None}
        """
        result = {"titles": [], "saved": False, "error": None}

        db, should_close = self._get_db()
        try:
            product = db.product_get(product_code)
            if not product:
                result["error"] = f"Product {product_code} not found"
                return result

            data = build_product_data(product)
            template = load_prompt("seo/website_meta")
            filled = fill_prompt(template, data)

            llm = self._get_llm()
            response = llm.chat(filled, max_tokens=500, temperature=0.7)
            response = _clean_llm_response(response)

            # Try JSON parsing first
            titles = _parse_json_array(response)
            if not titles:
                # Fallback: parse lines
                lines = _parse_lines(response)
                titles = [
                    {"version": i+1, "title": line, "focus": ""}
                    for i, line in enumerate(lines[:count])
                ]

            titles = titles[:count]
            result["titles"] = titles

            if save and titles:
                for i, t in enumerate(titles[:3]):
                    col = f"meta_title_{i+1}"
                    title_text = t.get("title", "") if isinstance(t, dict) else str(t)
                    db.execute(
                        f"UPDATE products SET {col} = ?, "
                        "updated_at = datetime('now') WHERE product_code = ?",
                        (title_text, product_code)
                    )
                db.commit()
                result["saved"] = True

        except Exception as e:
            result["error"] = str(e)
        finally:
            if should_close:
                db.close()

        return result

    def generate_meta_description(
        self,
        product_code: str,
        count: int = 3,
        save: bool = True,
    ) -> dict:
        """
        Generate SEO meta descriptions for independent website.

        Returns:
            {"descriptions": [...], "saved": bool, "error": str or None}
        """
        result = {"descriptions": [], "saved": False, "error": None}

        db, should_close = self._get_db()
        try:
            product = db.product_get(product_code)
            if not product:
                result["error"] = f"Product {product_code} not found"
                return result

            data = build_product_data(product)
            template = load_prompt("seo/website_meta")
            filled = fill_prompt(template, data)

            # Modify prompt for meta description
            desc_prompt = filled + (
                "\n\nNow generate 3 meta descriptions (150-160 characters each) "
                "instead of titles. Each should be compelling and include "
                "primary keywords. Output as JSON array:\n"
                '[{"version": 1, "description": "..."}, ...]'
            )

            llm = self._get_llm()
            response = llm.chat(desc_prompt, max_tokens=500, temperature=0.7)
            response = _clean_llm_response(response)

            descriptions = _parse_json_array(response)
            if not descriptions:
                lines = _parse_lines(response, min_len=30)
                descriptions = [
                    {"version": i+1, "description": line}
                    for i, line in enumerate(lines[:count])
                ]

            descriptions = descriptions[:count]
            result["descriptions"] = descriptions

            if save and descriptions:
                for i, d in enumerate(descriptions[:3]):
                    col = f"meta_description_{i+1}"
                    desc_text = d.get("description", "") if isinstance(d, dict) else str(d)
                    db.execute(
                        f"UPDATE products SET {col} = ?, "
                        "updated_at = datetime('now') WHERE product_code = ?",
                        (desc_text, product_code)
                    )
                db.commit()
                result["saved"] = True

        except Exception as e:
            result["error"] = str(e)
        finally:
            if should_close:
                db.close()

        return result

    def generate_description(
        self,
        product_code: str,
        save: bool = True,
    ) -> dict:
        """
        Generate product description for independent website.

        Returns:
            {"content": str, "length": int, "word_count": int,
             "saved": bool, "error": str or None}
        """
        result = {
            "content": "", "length": 0, "word_count": 0,
            "saved": False, "error": None
        }

        db, should_close = self._get_db()
        try:
            product = db.product_get(product_code)
            if not product:
                result["error"] = f"Product {product_code} not found"
                return result

            data = build_product_data(product)
            template = load_prompt("seo/website_description")
            filled = fill_prompt(template, data)

            llm = self._get_llm()
            response = llm.chat(filled, max_tokens=1000, temperature=0.7)
            response = _clean_llm_response(response)

            word_count = len(response.split())
            result["content"] = response
            result["length"] = len(response)
            result["word_count"] = word_count

            if save:
                db.execute(
                    "UPDATE products SET product_description = ?, "
                    "website_content_status = 'generated', "
                    "updated_at = datetime('now') WHERE product_code = ?",
                    (response, product_code)
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
        Generate all website content for a product.

        Returns:
            Dict with meta_titles, meta_descriptions, description.
        """
        result = {"product_code": product_code}

        result["meta_titles"] = self.generate_meta_titles(
            product_code, save=save)
        result["meta_descriptions"] = self.generate_meta_description(
            product_code, save=save)
        result["description"] = self.generate_description(
            product_code, save=save)

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
                project_root, "output", "seo_content", product_code, "website")

        os.makedirs(output_dir, exist_ok=True)

        db, should_close = self._get_db()
        result = {}

        try:
            product = db.product_get(product_code)
            if not product:
                raise ValueError(f"Product {product_code} not found")

            # Meta titles
            meta_titles = [
                product.get(f"meta_title_{i}") for i in range(1, 4)]
            meta_titles = [t for t in meta_titles if t]
            if meta_titles:
                path = os.path.join(output_dir, "meta_titles.txt")
                with open(path, "w", encoding="utf-8") as f:
                    for i, t in enumerate(meta_titles, 1):
                        f.write(f"{i}. {t}\n")
                result["meta_titles"] = path

            # Meta descriptions
            meta_descs = [
                product.get(f"meta_description_{i}") for i in range(1, 4)]
            meta_descs = [d for d in meta_descs if d]
            if meta_descs:
                path = os.path.join(output_dir, "meta_descriptions.txt")
                with open(path, "w", encoding="utf-8") as f:
                    for i, d in enumerate(meta_descs, 1):
                        f.write(f"{i}. {d}\n\n")
                result["meta_descriptions"] = path

            # Product description
            desc = product.get("product_description")
            if desc:
                path = os.path.join(output_dir, "product_description.md")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(desc)
                result["product_description"] = path

        finally:
            if should_close:
                db.close()

        return result
