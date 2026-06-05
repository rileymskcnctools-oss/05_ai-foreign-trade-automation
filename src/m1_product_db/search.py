"""
FT Workspace v2.0 - M1: Product Search

Search and filter products in the database.
"""

from typing import Optional
from src.core.database import FTDatabase


def search(
    query: str,
    db: Optional[FTDatabase] = None,
    limit: int = 20,
) -> list[dict]:
    """
    Full-text search across product fields.

    Searches: product_code, product_name_en, product_name_cn, target_keywords
    """
    should_close = False
    if db is None:
        db = FTDatabase()
        should_close = True

    try:
        return db.product_search(query, limit=limit)
    finally:
        if should_close:
            db.close()


def filter_products(
    db: Optional[FTDatabase] = None,
    category: Optional[str] = None,
    sub_category: Optional[str] = None,
    material: Optional[str] = None,
    handle_material: Optional[str] = None,
    min_weight: Optional[float] = None,
    max_weight: Optional[float] = None,
    min_length: Optional[float] = None,
    max_length: Optional[float] = None,
    packaging_type: Optional[str] = None,
    status: Optional[str] = "active",
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    """
    Filter products by various criteria.

    Returns list of matching product dicts.
    """
    should_close = False
    if db is None:
        db = FTDatabase()
        should_close = True

    try:
        sql = "SELECT * FROM products WHERE 1=1"
        params = []

        if category:
            sql += " AND category = ?"
            params.append(category)

        if sub_category:
            sql += " AND sub_category = ?"
            params.append(sub_category)

        if material:
            sql += " AND material LIKE ?"
            params.append(f"%{material}%")

        if handle_material:
            sql += " AND handle_material LIKE ?"
            params.append(f"%{handle_material}%")

        if min_weight is not None:
            sql += " AND weight_kg >= ?"
            params.append(min_weight)

        if max_weight is not None:
            sql += " AND weight_kg <= ?"
            params.append(max_weight)

        if min_length is not None:
            sql += " AND length_cm >= ?"
            params.append(min_length)

        if max_length is not None:
            sql += " AND length_cm <= ?"
            params.append(max_length)

        if packaging_type:
            sql += " AND packaging_type = ?"
            params.append(packaging_type)

        if status:
            sql += " AND status = ?"
            params.append(status)

        sql += " ORDER BY product_code LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        return db.fetchall(sql, tuple(params))
    finally:
        if should_close:
            db.close()


def get_categories(db: Optional[FTDatabase] = None) -> list[dict]:
    """Get list of categories with product counts."""
    should_close = False
    if db is None:
        db = FTDatabase()
        should_close = True

    try:
        return db.fetchall(
            "SELECT category, COUNT(*) as product_count "
            "FROM products GROUP BY category ORDER BY product_count DESC"
        )
    finally:
        if should_close:
            db.close()


def get_sub_categories(
    category: str,
    db: Optional[FTDatabase] = None,
) -> list[dict]:
    """Get sub-categories for a given category."""
    should_close = False
    if db is None:
        db = FTDatabase()
        should_close = True

    try:
        return db.fetchall(
            "SELECT sub_category, COUNT(*) as product_count "
            "FROM products WHERE category = ? GROUP BY sub_category "
            "ORDER BY product_count DESC",
            (category,)
        )
    finally:
        if should_close:
            db.close()
