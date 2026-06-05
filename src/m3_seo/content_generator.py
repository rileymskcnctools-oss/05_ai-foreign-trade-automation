"""
FT Workspace v2.0 - M3: SEO & Platform Content Generator

Generate content for products using AI + prompt templates.

Usage:
    from src.m3_seo.content_generator import generate_seo_titles

    titles = generate_seo_titles("GF-001")
    print(titles)
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
    # Remove markdown code fences
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    return text.strip()


def _parse_selling_points(text: str) -> list[str]:
    """Parse selling points with Feature/Benefit blocks."""
    points = []
    blocks = re.split(r'\*\*\d+\.\s', text)
    for block in blocks:
        block = block.strip()
        if block:
            # Remove trailing ** from dimension name (e.g., "Material & Durability**")
            block = re.sub(r'^([^\n]+?)\*\*', r'\1', block, count=1)
            if block:
                points.append(block.strip())
    return points


def _parse_numbered_list(text: str) -> list[str]:
    """Parse a numbered list from LLM response."""
    items = []
    for line in text.split("\n"):
        line = line.strip()
        # Match: "1. ", "1) ", "- ", "* "
        match = re.match(r'^[\d\-\*\•]+\.[\s)]*\s*(.*)', line) or \
                re.match(r'^[\-\*\•]\s+(.*)', line)
        if match:
            item = match.group(1).strip()
            # Skip lines that look like JSON keys or short headers
            if item and len(item) > 5 and not item.endswith('**'):
                items.append(item)
    return items


# ============================================================
# SEO Title Generator
# ============================================================

def generate_seo_titles(
    product_code: str,
    count: int = 3,
    db: Optional[FTDatabase] = None,
    llm: Optional[LLMClient] = None,
    save: bool = True,
) -> list[str]:
    """
    Generate SEO titles for a product.

    Args:
        product_code: Product code (e.g., 'GF-001').
        count: Number of titles to generate (default 3).
        db: Database instance.
        llm: LLM client instance.
        save: Whether to save results to database.

    Returns:
        List of generated SEO titles.
    """
    should_close_db = False
    if db is None:
        db = FTDatabase()
        should_close_db = True

    try:
        product = db.product_get(product_code)
        if not product:
            raise ValueError(f"Product {product_code} not found")

        data = build_product_data(product)
        template = load_prompt("seo/alibaba_title")
        filled = fill_prompt(template, data)

        if llm is None:
            llm = LLMClient(scenario="seo_content")

        response = llm.chat(
            filled,
            max_tokens=500,
            temperature=0.7,
        )

        response = _clean_llm_response(response)
        titles = _parse_numbered_list(response)

        # Fallback: if parsing failed, treat each line as a title
        if not titles:
            titles = [
                line.strip()
                for line in response.split("\n")
                if line.strip() and len(line.strip()) > 10
            ]

        # Truncate to requested count
        titles = titles[:count]

        # Pad if fewer than requested
        while len(titles) < count:
            titles.append(f"SEO Title {len(titles) + 1} (placeholder)")

        # Save to database
        if save and len(titles) >= 3:
            db.execute(
                "UPDATE products SET seo_title_1 = ?, seo_title_2 = ?, "
                "seo_title_3 = ?, alibaba_detail_status = 'generated', "
                "updated_at = datetime('now') WHERE product_code = ?",
                (titles[0], titles[1] if len(titles) > 1 else "",
                 titles[2] if len(titles) > 2 else "", product_code)
            )
            db.commit()

        return titles

    finally:
        if should_close_db:
            db.close()


# ============================================================
# Selling Points Generator
# ============================================================

def generate_selling_points(
    product_code: str,
    count: int = 5,
    db: Optional[FTDatabase] = None,
    llm: Optional[LLMClient] = None,
    save: bool = True,
) -> list[str]:
    """
    Generate selling points for a product.

    Returns:
        List of selling point strings.
    """
    should_close_db = False
    if db is None:
        db = FTDatabase()
        should_close_db = True

    try:
        product = db.product_get(product_code)
        if not product:
            raise ValueError(f"Product {product_code} not found")

        data = build_product_data(product)
        template = load_prompt("seo/selling_points")
        filled = fill_prompt(template, data)

        if llm is None:
            llm = LLMClient(scenario="seo_content")

        response = llm.chat(
            filled,
            max_tokens=1000,
            temperature=0.7,
        )

        response = _clean_llm_response(response)
        points = _parse_selling_points(response)

        # Fallback: try numbered list parser
        if not points:
            points = _parse_numbered_list(response)

        # Final fallback: treat each non-empty line as a point
        if not points:
            points = [
                line.strip()
                for line in response.split("\n")
                if line.strip() and len(line.strip()) > 10
            ]

        points = points[:count]

        if save and points:
            joined = " | ".join(points)
            db.execute(
                "UPDATE products SET selling_points = ?, "
                "updated_at = datetime('now') WHERE product_code = ?",
                (joined, product_code)
            )
            db.commit()

        return points

    finally:
        if should_close_db:
            db.close()


# ============================================================
# WhatsApp Script Generator
# ============================================================

def generate_whatsapp_script(
    product_code: str,
    db: Optional[FTDatabase] = None,
    llm: Optional[LLMClient] = None,
    save: bool = True,
) -> str:
    """
    Generate WhatsApp outreach script for a product.

    Returns:
        WhatsApp script text.
    """
    should_close_db = False
    if db is None:
        db = FTDatabase()
        should_close_db = True

    try:
        product = db.product_get(product_code)
        if not product:
            raise ValueError(f"Product {product_code} not found")

        data = build_product_data(product)
        template = load_prompt("social/whatsapp")
        filled = fill_prompt(template, data)

        if llm is None:
            llm = LLMClient(scenario="seo_content")

        response = llm.chat(
            filled,
            max_tokens=500,
            temperature=0.7,
        )

        response = _clean_llm_response(response)

        if save:
            db.execute(
                "UPDATE products SET whatsapp_script = ?, "
                "updated_at = datetime('now') WHERE product_code = ?",
                (response, product_code)
            )
            db.commit()

        return response

    finally:
        if should_close_db:
            db.close()


# ============================================================
# Alibaba Detail Page Generator
# ============================================================

def generate_alibaba_detail(
    product_code: str,
    db: Optional[FTDatabase] = None,
    llm: Optional[LLMClient] = None,
    save: bool = True,
) -> str:
    """
    Generate Alibaba detail page content for a product.

    Returns:
        Markdown detail page content.
    """
    should_close_db = False
    if db is None:
        db = FTDatabase()
        should_close_db = True

    try:
        product = db.product_get(product_code)
        if not product:
            raise ValueError(f"Product {product_code} not found")

        data = build_product_data(product)
        template = load_prompt("seo/alibaba_detail")
        filled = fill_prompt(template, data)

        if llm is None:
            llm = LLMClient(scenario="seo_content")

        response = llm.chat(
            filled,
            max_tokens=4000,
            temperature=0.7,
        )

        response = _clean_llm_response(response)

        if save:
            db.execute(
                "UPDATE products SET alibaba_detail_status = 'generated', "
                "updated_at = datetime('now') WHERE product_code = ?",
                (product_code,)
            )
            db.commit()

        return response

    finally:
        if should_close_db:
            db.close()


# ============================================================
# Bulk Generator
# ============================================================

def generate_all_for_product(
    product_code: str,
    db: Optional[FTDatabase] = None,
    llm: Optional[LLMClient] = None,
) -> dict:
    """
    Generate all content types for a single product.

    Returns:
        Dict with results for each content type.
    """
    should_close_db = False
    if db is None:
        db = FTDatabase()
        should_close_db = True

    results = {"product_code": product_code, "content": {}}

    try:
        print(f"  Generating SEO titles for {product_code}...")
        try:
            titles = generate_seo_titles(product_code, db=db, llm=llm)
            results["content"]["seo_titles"] = titles
            results["content"]["seo_titles_count"] = len(titles)
            print(f"    OK: {len(titles)} titles")
        except Exception as e:
            results["content"]["seo_titles"] = []
            results["content"]["seo_titles_error"] = str(e)
            print(f"    FAIL: {e}")

        print(f"  Generating selling points for {product_code}...")
        try:
            points = generate_selling_points(product_code, db=db, llm=llm)
            results["content"]["selling_points"] = points
            results["content"]["selling_points_count"] = len(points)
            print(f"    OK: {len(points)} points")
        except Exception as e:
            results["content"]["selling_points"] = []
            results["content"]["selling_points_error"] = str(e)
            print(f"    FAIL: {e}")

        print(f"  Generating WhatsApp script for {product_code}...")
        try:
            script = generate_whatsapp_script(product_code, db=db, llm=llm)
            results["content"]["whatsapp_script"] = script
            results["content"]["whatsapp_script_len"] = len(script)
            print(f"    OK: {len(script)} chars")
        except Exception as e:
            results["content"]["whatsapp_script"] = ""
            results["content"]["whatsapp_script_error"] = str(e)
            print(f"    FAIL: {e}")

        print(f"  Generating Alibaba detail for {product_code}...")
        try:
            detail = generate_alibaba_detail(product_code, db=db, llm=llm)
            results["content"]["alibaba_detail"] = detail
            results["content"]["alibaba_detail_len"] = len(detail)
            print(f"    OK: {len(detail)} chars")
        except Exception as e:
            results["content"]["alibaba_detail"] = ""
            results["content"]["alibaba_detail_error"] = str(e)
            print(f"    FAIL: {e}")

    finally:
        if should_close_db:
            db.close()

    return results


# ============================================================
# Export to files
# ============================================================

def export_content_to_files(
    product_code: str,
    output_dir: Optional[str] = None,
    db: Optional[FTDatabase] = None,
) -> dict:
    """
    Export generated content from database to files.

    Args:
        product_code: Product code.
        output_dir: Output directory. Defaults to output/seo_content/<code>/
        db: Database instance.

    Returns:
        Dict of {content_type: file_path}.
    """
    should_close_db = False
    if db is None:
        db = FTDatabase()
        should_close_db = True

    if output_dir is None:
        project_root = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))
        output_dir = os.path.join(project_root, "output", "seo_content", product_code)

    os.makedirs(output_dir, exist_ok=True)

    results = {}

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
            results["seo_titles"] = path

        # Selling points
        sp = product.get("selling_points")
        if sp:
            path = os.path.join(output_dir, "selling_points.txt")
            with open(path, "w", encoding="utf-8") as f:
                for point in sp.split(" | "):
                    f.write(f"- {point.strip()}\n")
            results["selling_points"] = path

        # WhatsApp script
        wa = product.get("whatsapp_script")
        if wa:
            path = os.path.join(output_dir, "whatsapp_script.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(wa)
            results["whatsapp_script"] = path

    finally:
        if should_close_db:
            db.close()

    return results
