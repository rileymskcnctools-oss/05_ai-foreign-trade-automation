"""
FT Workspace v2.0 - M1: Product Importer

Import products from CSV or Excel files into SQLite database.

Supports:
- CSV (with configurable encoding, default: gbk for Chinese compatibility)
- Excel (.xlsx, .xls)

Auto-detects column names and maps them to database schema.
"""

import os
import csv
from typing import Optional
from datetime import datetime

from src.core.database import FTDatabase


# ============================================================
# Column name normalization
# ============================================================

def normalize_col(name: str) -> str:
    """
    Normalize column name to match database field names.
    Handles variations: spaces, underscores, case, Chinese aliases.
    """
    name = name.strip().lower()

    # Chinese alias mapping
    cn_aliases = {
        "产品编号": "product_id",
        "产品编码": "product_id",
        "产品名称": "product_name_en",
        "英文名": "product_name_en",
        "中文名": "product_name_cn",
        "类别": "category",
        "子类": "sub_category",
        "材质": "material",
        "手柄材质": "handle_material",
        "长度": "length_cm",
        "长度(cm)": "length_cm",
        "重量": "weight_kg",
        "重量(kg)": "weight_kg",
        "头部宽度": "head_width_cm",
        "齿数": "tine_count",
        "硬度": "hardness",
        "表面处理": "surface_treatment",
        "最小起订量": "moq",
        "包装方式": "packaging_type",
        "每箱数量": "qty_per_carton",
        "外箱尺寸": "carton_size_cm",
        "每箱毛重": "gw_per_carton_kg",
        "交货期": "lead_time_days",
        "认证": "certification",
        "目标关键词": "target_keywords",
        "使用场景": "use_scenario",
        "目标市场": "target_markets",
        "核心卖点": "selling_angle",
        "竞品参考": "competitor_ref",
        "seo标题1": "seo_title_1",
        "seo标题2": "seo_title_2",
        "seo标题3": "seo_title_3",
        "五点卖点": "selling_points",
        "whatsapp话术": "whatsapp_script",
        "阿里详情状态": "alibaba_detail_status",
    }

    if name in cn_aliases:
        name = cn_aliases[name]

    # Normalize separators
    name = name.replace(" ", "_").replace("-", "_")

    # Known column name mappings (English variations)
    english_aliases = {
        "product_id": "product_code",
        "product_code": "product_code",
        "code": "product_code",
        "product_name": "product_name_en",
        "product_name_en": "product_name_en",
        "product_name_cn": "product_name_cn",
        "category": "category",
        "sub_category": "sub_category",
        "subcategory": "sub_category",
        "material": "material",
        "handle_material": "handle_material",
        "length_cm": "length_cm",
        "length": "length_cm",
        "weight_kg": "weight_kg",
        "weight": "weight_kg",
        "head_width_cm": "head_width_cm",
        "tine_count": "tine_count",
        "hardness": "hardness",
        "surface_treatment": "surface_treatment",
        "moq": "moq",
        "min_order_quantity": "moq",
        "packaging_type": "packaging_type",
        "packaging": "packaging_type",
        "qty_per_carton": "qty_per_carton",
        "quantity_per_carton": "qty_per_carton",
        "carton_size_cm": "carton_size_cm",
        "carton_size": "carton_size_cm",
        "gw_per_carton_kg": "gw_per_carton_kg",
        "gross_weight": "gw_per_carton_kg",
        "lead_time_days": "lead_time_days",
        "lead_time": "lead_time_days",
        "certification": "certification",
        "target_keywords": "target_keywords",
        "keywords": "target_keywords",
        "use_scenario": "use_scenario",
        "scenarios": "use_scenario",
        "target_markets": "target_markets",
        "markets": "target_markets",
        "selling_angle": "selling_angle",
        "selling_point": "selling_angle",
        "competitor_ref": "competitor_ref",
        "competitors": "competitor_ref",
        "seo_title_1": "seo_title_1",
        "seo_title_2": "seo_title_2",
        "seo_title_3": "seo_title_3",
        "selling_points": "selling_points",
        "whatsapp_script": "whatsapp_script",
        "alibaba_detail_status": "alibaba_detail_status",
    }

    return english_aliases.get(name, name)


# ============================================================
# Value parsing
# ============================================================

NUMERIC_FIELDS = {
    "length_cm", "weight_kg", "head_width_cm", "moq",
    "qty_per_carton", "gw_per_carton_kg", "lead_time_days", "tine_count",
}

INT_FIELDS = {"moq", "qty_per_carton", "lead_time_days", "tine_count"}


def parse_value(value: str, field_name: str) -> Optional[object]:
    """Parse a CSV/Excel cell value to appropriate Python type."""
    if value is None:
        return None

    if isinstance(value, str):
        value = value.strip()
        if value == "" or value.lower() in ("n/a", "null", "none", "na", "-"):
            return None

    if field_name in NUMERIC_FIELDS:
        try:
            num = float(value)
            if field_name in INT_FIELDS:
                return int(num)
            return num
        except (ValueError, TypeError):
            return None

    return str(value)


# ============================================================
# CSV Importer
# ============================================================

def import_csv(
    filepath: str,
    encoding: str = "gbk",
    db: Optional[FTDatabase] = None,
    dry_run: bool = False,
) -> dict:
    """
    Import products from a CSV file.

    Args:
        filepath: Path to CSV file.
        encoding: File encoding (default: gbk for Chinese CSV files).
        db: Database instance. Creates new one if None.
        dry_run: If True, parse but don't insert.

    Returns:
        Import report dict.
    """
    report = {
        "source": filepath,
        "format": "csv",
        "encoding": encoding,
        "total_rows": 0,
        "imported": 0,
        "skipped": 0,
        "errors": [],
        "warnings": [],
        "column_map": {},
        "dry_run": dry_run,
    }

    if not os.path.exists(filepath):
        report["errors"].append(f"File not found: {filepath}")
        return report

    if db is None:
        db = FTDatabase()
        should_close = True
    else:
        should_close = False

    try:
        with open(filepath, "r", encoding=encoding) as f:
            reader = csv.DictReader(f)
            raw_headers = reader.fieldnames or []

            # Build column map
            col_map = {}
            for raw in raw_headers:
                normalized = normalize_col(raw)
                col_map[raw] = normalized
            report["column_map"] = col_map

            rows = list(reader)
            report["total_rows"] = len(rows)

            # Process rows
            products = []
            for i, row in enumerate(rows, 1):
                product = {}
                for raw_col, db_col in col_map.items():
                    if raw_col in row:
                        product[db_col] = parse_value(row[raw_col], db_col)

                # Add metadata
                product["source"] = "csv_import"
                product["source_file"] = os.path.basename(filepath)
                product["updated_at"] = datetime.now().isoformat()

                # Validate required
                if not product.get("product_code"):
                    report["warnings"].append(
                        f"Row {i}: missing product_code, skipped"
                    )
                    report["skipped"] += 1
                    continue

                products.append(product)

            # Insert
            if not dry_run:
                result = db.product_insert_many(products)
                report["imported"] = result["success"]
                report["skipped"] += len(result["errors"])
                report["errors"].extend(result["errors"])
                db.commit()
            else:
                report["imported"] = len(products)

    except UnicodeDecodeError as e:
        report["errors"].append(
            f"Encoding error: {e}. Try a different encoding "
            f"(e.g., 'utf-8', 'gbk', 'gb2312', 'latin-1')."
        )
    except Exception as e:
        report["errors"].append(f"Import error: {str(e)}")
    finally:
        if should_close:
            db.close()

    return report


# ============================================================
# Excel Importer
# ============================================================

def import_excel(
    filepath: str,
    sheet_name: Optional[str] = None,
    db: Optional[FTDatabase] = None,
    dry_run: bool = False,
) -> dict:
    """
    Import products from an Excel file.

    Args:
        filepath: Path to Excel file (.xlsx or .xls).
        sheet_name: Specific sheet to read. None = first sheet.
        db: Database instance. Creates new one if None.
        dry_run: If True, parse but don't insert.

    Returns:
        Import report dict.
    """
    report = {
        "source": filepath,
        "format": "excel",
        "sheet": sheet_name or "first",
        "total_rows": 0,
        "imported": 0,
        "skipped": 0,
        "errors": [],
        "warnings": [],
        "column_map": {},
        "dry_run": dry_run,
    }

    if not os.path.exists(filepath):
        report["errors"].append(f"File not found: {filepath}")
        return report

    try:
        import pandas as pd
    except ImportError:
        report["errors"].append(
            "pandas is required for Excel import. "
            "Install it: pip install pandas openpyxl"
        )
        return report

    if db is None:
        db = FTDatabase()
        should_close = True
    else:
        should_close = False

    try:
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        report["total_rows"] = len(df)

        # Build column map
        col_map = {}
        for col in df.columns:
            col_map[str(col)] = normalize_col(str(col))
        report["column_map"] = col_map

        # Convert to products
        products = []
        for i, row in df.iterrows():
            product = {}
            for orig_col, db_col in col_map.items():
                val = row.get(orig_col)
                product[db_col] = parse_value(val, db_col)

            product["source"] = "excel_import"
            product["source_file"] = os.path.basename(filepath)
            product["updated_at"] = datetime.now().isoformat()

            if not product.get("product_code"):
                report["warnings"].append(
                    f"Row {i + 1}: missing product_code, skipped"
                )
                report["skipped"] += 1
                continue

            products.append(product)

        if not dry_run:
            result = db.product_insert_many(products)
            report["imported"] = result["success"]
            report["skipped"] += len(result["errors"])
            report["errors"].extend(result["errors"])
            db.commit()
        else:
            report["imported"] = len(products)

    except Exception as e:
        report["errors"].append(f"Import error: {str(e)}")
    finally:
        if should_close:
            db.close()

    return report
