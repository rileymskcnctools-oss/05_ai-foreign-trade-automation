"""
FT Workspace v2.0 - M1: Product Exporter

Export product data to CSV or Excel files.
"""

import csv
import os
from typing import Optional
from src.core.database import FTDatabase


# Default columns to export (subset of all fields)
DEFAULT_EXPORT_COLS = [
    "product_code", "product_name_en", "product_name_cn",
    "category", "sub_category", "material", "handle_material",
    "length_cm", "weight_kg", "tine_count", "hardness",
    "moq", "packaging_type", "qty_per_carton", "carton_size_cm",
    "gw_per_carton_kg", "lead_time_days", "certification",
    "target_keywords", "use_scenario", "target_markets",
    "selling_angle", "seo_title_1", "seo_title_2", "seo_title_3",
    "selling_points",
]


def export_csv(
    filepath: str,
    db: Optional[FTDatabase] = None,
    columns: Optional[list] = None,
    category: Optional[str] = None,
    encoding: str = "utf-8",
) -> dict:
    """
    Export products to a CSV file.

    Args:
        filepath: Output file path.
        db: Database instance.
        columns: List of columns to export. Defaults to DEFAULT_EXPORT_COLS.
        category: Filter by category. None = all.
        encoding: File encoding.

    Returns:
        Export report dict.
    """
    report = {"filepath": filepath, "exported": 0, "errors": []}

    cols = columns or DEFAULT_EXPORT_COLS

    if db is None:
        db = FTDatabase()
        should_close = True
    else:
        should_close = False

    try:
        products = db.product_list(category=category, status=None, limit=10000)

        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

        with open(filepath, "w", encoding=encoding, newline="") as f:
            writer = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            writer.writeheader()

            for p in products:
                # Convert None to empty string for CSV
                row = {}
                for col in cols:
                    val = p.get(col)
                    row[col] = val if val is not None else ""
                writer.writerow(row)

        report["exported"] = len(products)

    except Exception as e:
        report["errors"].append(str(e))
    finally:
        if should_close:
            db.close()

    return report


def export_excel(
    filepath: str,
    db: Optional[FTDatabase] = None,
    columns: Optional[list] = None,
    category: Optional[str] = None,
) -> dict:
    """
    Export products to an Excel file.

    Args:
        filepath: Output file path.
        db: Database instance.
        columns: List of columns to export.
        category: Filter by category.

    Returns:
        Export report dict.
    """
    report = {"filepath": filepath, "exported": 0, "errors": []}

    try:
        import pandas as pd
    except ImportError:
        report["errors"].append(
            "pandas is required for Excel export. "
            "Install it: pip install pandas openpyxl"
        )
        return report

    cols = columns or DEFAULT_EXPORT_COLS

    if db is None:
        db = FTDatabase()
        should_close = True
    else:
        should_close = False

    try:
        products = db.product_list(category=category, status=None, limit=10000)

        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

        df = pd.DataFrame(products)
        # Keep only requested columns that exist
        available_cols = [c for c in cols if c in df.columns]
        df = df[available_cols]

        df.to_excel(filepath, index=False, engine="openpyxl")
        report["exported"] = len(products)

    except Exception as e:
        report["errors"].append(str(e))
    finally:
        if should_close:
            db.close()

    return report
