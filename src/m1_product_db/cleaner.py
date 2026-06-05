"""
FT Workspace v2.0 - M1: Data Cleaner

Clean and standardize product data before or after import.
"""

from typing import Optional
from src.core.database import FTDatabase


# Standardized value sets
PACKAGING_TYPES = {
    "color box", "blister card", "poly bag", "shrink wrap",
    "hang card", "display box", "bulk pack", "custom packaging",
    "彩盒", "吸塑卡", "塑料袋", "热缩膜", "挂卡", "展示盒", "散装", "定制包装",
}

PACKAGING_MAP = {
    "彩盒": "Color Box",
    "吸塑卡": "Blister Card",
    "塑料袋": "Poly Bag",
    "热缩膜": "Shrink Wrap",
    "挂卡": "Hang Card",
    "展示盒": "Display Box",
    "散装": "Bulk Pack",
    "定制包装": "Custom Packaging",
    "colour box": "Color Box",
    "blister": "Blister Card",
    "polybag": "Poly Bag",
}


def clean_product(product: dict) -> dict:
    """
    Clean and standardize a single product dict.

    Returns cleaned product dict.
    """
    cleaned = dict(product)

    # Strip whitespace from string fields
    for key, value in cleaned.items():
        if isinstance(value, str):
            cleaned[key] = value.strip()
            if cleaned[key] == "":
                cleaned[key] = None

    # Normalize packaging type
    pkg = cleaned.get("packaging_type")
    if pkg:
        pkg_lower = pkg.lower()
        if pkg_lower in PACKAGING_MAP:
            cleaned["packaging_type"] = PACKAGING_MAP[pkg_lower]

    # Ensure numeric fields are proper types
    numeric_fields = {
        "length_cm", "weight_kg", "head_width_cm",
        "gw_per_carton_kg", "moq", "qty_per_carton", "lead_time_days",
        "tine_count",
    }
    for field in numeric_fields:
        val = cleaned.get(field)
        if val is not None:
            try:
                num = float(val)
                int_fields = {"moq", "qty_per_carton", "lead_time_days", "tine_count"}
                cleaned[field] = int(num) if field in int_fields else num
            except (ValueError, TypeError):
                cleaned[field] = None

    return cleaned


def clean_all(
    db: Optional[FTDatabase] = None,
    category: Optional[str] = None,
) -> dict:
    """
    Clean all products in the database.

    Args:
        db: Database instance.
        category: Limit to specific category.

    Returns:
        Clean report dict.
    """
    report = {"cleaned": 0, "warnings": [], "errors": []}

    if db is None:
        db = FTDatabase()
        should_close = True
    else:
        should_close = False

    try:
        products = db.product_list(category=category, status=None, limit=10000)

        for p in products:
            cleaned = clean_product(p)
            code = cleaned.get("product_code")
            db.product_insert(cleaned)
            report["cleaned"] += 1

        db.commit()

    except Exception as e:
        report["errors"].append(str(e))
    finally:
        if should_close:
            db.close()

    return report


def find_missing_fields(
    db: Optional[FTDatabase] = None,
    fields: Optional[list] = None,
) -> dict:
    """
    Find products with missing required fields.

    Args:
        db: Database instance.
        fields: List of field names to check. Defaults to key fields.

    Returns:
        Dict of {field_name: [list of product_codes missing this field]}
    """
    if fields is None:
        fields = [
            "product_name_en", "category", "material",
            "length_cm", "weight_kg", "moq", "packaging_type",
        ]

    if db is None:
        db = FTDatabase()
        should_close = True
    else:
        should_close = False

    result = {}
    try:
        all_products = db.product_list(status=None, limit=10000)
        for field in fields:
            missing = [
                p["product_code"] for p in all_products
                if p.get(field) is None
            ]
            if missing:
                result[field] = missing
    finally:
        if should_close:
            db.close()

    return result
