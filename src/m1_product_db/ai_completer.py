"""
FT Workspace v2.0 - M1: AI Product Info Completer

Use AI to fill in missing product fields.
"""

from typing import Optional
from src.core.database import FTDatabase


# AI completion prompts by field
FILL_PROMPTS = {
    "hs_code": (
        "You are a trade classification expert. "
        "Given the product info below, determine the most likely HS Code "
        "(Harmonized System Code, 6 digits) for this garden/farm tool.\n\n"
        "Product: {product_name_en}\n"
        "Category: {category}\n"
        "Material: {material}\n\n"
        "Respond with ONLY the 6-digit HS code (e.g., 820130), nothing else."
    ),
    "target_markets": (
        "You are a foreign trade market analyst. "
        "Based on the product info, recommend 3-5 target export markets "
        "for this garden/farm tool.\n\n"
        "Product: {product_name_en}\n"
        "Category: {category}\n"
        "Material: {material}\n\n"
        "Respond with ONLY a comma-separated list of country names (English), "
        "e.g., Kenya, Tanzania, Nigeria, Ghana, Sri Lanka"
    ),
    "use_scenario": (
        "You are a product description expert. "
        "Write 3-4 practical use scenarios for this garden/farm tool, "
        "comma-separated.\n\n"
        "Product: {product_name_en}\n"
        "Category: {category}\n"
        "Material: {material}\n\n"
        "Respond with ONLY the scenarios, comma-separated, in English."
    ),
}


def complete_field(
    product_code: str,
    field_name: str,
    db: Optional[FTDatabase] = None,
    dry_run: bool = False,
) -> dict:
    """
    Use AI to fill in a missing field for one product.

    Args:
        product_code: The product to update.
        field_name: The field to complete.
        db: Database instance.
        dry_run: If True, return AI result without saving.

    Returns:
        Result dict with {product_code, field, value, saved}.
    """
    result = {
        "product_code": product_code,
        "field": field_name,
        "value": None,
        "saved": False,
        "error": None,
    }

    if db is None:
        db = FTDatabase()
        should_close = True
    else:
        should_close = False

    try:
        product = db.product_get(product_code)
        if not product:
            result["error"] = f"Product {product_code} not found"
            return result

        if product.get(field_name) and not dry_run:
            result["value"] = product[field_name]
            result["saved"] = True
            return result

        # Get prompt
        prompt_template = FILL_PROMPTS.get(field_name)
        if not prompt_template:
            result["error"] = f"No AI prompt defined for field '{field_name}'"
            return result

        # Fill template with product data
        prompt = prompt_template.format(
            product_name_en=product.get("product_name_en", ""),
            category=product.get("category", ""),
            material=product.get("material", ""),
        )

        # Call AI
        from src.core.llm_client import LLMClient
        client = LLMClient(scenario="seo_content")
        value = client.chat(prompt, max_tokens=200, temperature=0.3)
        value = value.strip()

        result["value"] = value

        if not dry_run:
            db.execute(
                f"UPDATE products SET {field_name} = ?, updated_at = datetime('now') "
                "WHERE product_code = ?",
                (value, product_code)
            )
            db.commit()
            result["saved"] = True

    except Exception as e:
        result["error"] = str(e)
    finally:
        if should_close:
            db.close()

    return result


def complete_missing_fields(
    product_code: str,
    fields: Optional[list] = None,
    db: Optional[FTDatabase] = None,
    dry_run: bool = False,
) -> dict:
    """
    Use AI to fill in multiple missing fields for one product.

    Args:
        product_code: The product to update.
        fields: List of field names. Defaults to all supported fields.
        db: Database instance.
        dry_run: If True, don't save.

    Returns:
        Report dict with results per field.
    """
    if fields is None:
        fields = list(FILL_PROMPTS.keys())

    report = {"product_code": product_code, "results": [], "completed": 0}

    for field in fields:
        r = complete_field(product_code, field, db, dry_run)
        report["results"].append(r)
        if r.get("saved") or (r.get("value") and dry_run):
            report["completed"] += 1

    return report
