"""
FT Workspace v2.0 — v1.0 to v2.0 Data Migration Script

Migrates product data from v1.0 CSV to v2.0 SQLite database.

Usage:
    cd <project_root>
    python scripts/migrate_v1_to_v2.py

Or with custom paths:
    python scripts/migrate_v1_to_v2.py --csv path/to/csv --db path/to/db

This script is idempotent — safe to run multiple times.
Uses INSERT OR REPLACE to avoid duplicates.
"""

import csv
import os
import sys
import json
from datetime import datetime

# Add project root to path so we can import src
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.core.database import FTDatabase

# ============================================================
# Column Mapping: v1.0 CSV → v2.0 SQLite
# ============================================================
# v1.0 CSV has 31 columns. Map them to v2.0 products table.

COLUMN_MAP = {
    "product_id": "product_code",
    "product_name_cn": "product_name_cn",
    "product_name_en": "product_name_en",
    "category": "category",
    "sub_category": "sub_category",
    "material": "material",
    "handle_material": "handle_material",
    "length_cm": "length_cm",
    "weight_kg": "weight_kg",
    "head_width_cm": "head_width_cm",
    "tine_count": "tine_count",
    "hardness": "hardness",
    "surface_treatment": "surface_treatment",
    "moq": "moq",
    "packaging_type": "packaging_type",
    "qty_per_carton": "qty_per_carton",
    "carton_size_cm": "carton_size_cm",
    "gw_per_carton_kg": "gw_per_carton_kg",
    "lead_time_days": "lead_time_days",
    "certification": "certification",
    "target_keywords": "target_keywords",
    "use_scenario": "use_scenario",
    "target_markets": "target_markets",
    "selling_angle": "selling_angle",
    "competitor_ref": "competitor_ref",
    "seo_title_1": "seo_title_1",
    "seo_title_2": "seo_title_2",
    "seo_title_3": "seo_title_3",
    "selling_points": "selling_points",
    "whatsapp_script": "whatsapp_script",
    "alibaba_detail_status": "alibaba_detail_status",
}


def parse_value(value: str, col_name: str):
    """Parse CSV value to appropriate Python type."""
    if value is None or value.strip() == "":
        return None

    # Numeric fields
    numeric_fields = {
        "length_cm", "weight_kg", "head_width_cm", "moq",
        "qty_per_carton", "gw_per_carton_kg", "lead_time_days", "tine_count"
    }

    if col_name in numeric_fields:
        try:
            # Some fields are integer (moq, qty, lead_time, tine_count)
            int_fields = {"moq", "qty_per_carton", "lead_time_days", "tine_count"}
            if col_name in int_fields:
                return int(float(value))
            return float(value)
        except (ValueError, TypeError):
            return None

    return value.strip()


def migrate(csv_path: str, db_path: str = None) -> dict:
    """
    Run migration from v1.0 CSV to v2.0 SQLite.

    Args:
        csv_path: Path to v1.0 CSV file
        db_path: Path to v2.0 SQLite database (optional, auto-detected if None)

    Returns:
        Migration report dict
    """
    report = {
        "started_at": datetime.now().isoformat(),
        "csv_path": csv_path,
        "db_path": None,
        "total_csv_rows": 0,
        "migrated": 0,
        "skipped": 0,
        "errors": [],
        "warnings": [],
        "category_summary": {},
        "completed_at": None,
    }

    # Step 1: Verify CSV exists
    if not os.path.exists(csv_path):
        report["errors"].append(f"CSV file not found: {csv_path}")
        return report

    # Step 2: Initialize database
    db = FTDatabase(db_path)
    report["db_path"] = db.db_path

    # Drop old v1.0 products table if it exists (uses product_id instead of product_code)
    # Safe because we re-import all data from CSV below.
    db.execute("DROP TABLE IF EXISTS products")
    db.commit()

    db.init_schema()

    # Step 3: Read CSV and migrate
    try:
        with open(csv_path, "r", encoding="gbk") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        report["total_csv_rows"] = len(rows)

        # Categorize rows for summary
        for row in rows:
            cat = row.get("category", "Unknown").strip()
            if cat not in report["category_summary"]:
                report["category_summary"][cat] = 0
            report["category_summary"][cat] += 1

        # Convert rows to product dicts
        products = []
        for i, row in enumerate(rows, 1):
            product = {}
            for csv_col, db_col in COLUMN_MAP.items():
                if csv_col in row:
                    product[db_col] = parse_value(row[csv_col], db_col)

            # Add v2.0 metadata
            product["source"] = "csv_import"
            product["source_file"] = os.path.basename(csv_path)
            product["updated_at"] = datetime.now().isoformat()

            # Validate required field
            if not product.get("product_code"):
                report["warnings"].append(
                    f"Row {i}: missing product_code, skipped"
                )
                report["skipped"] += 1
                continue

            products.append(product)

        # Bulk insert
        result = db.product_insert_many(products)
        report["migrated"] = result["success"]
        report["skipped"] += len(result["errors"])
        report["errors"].extend(result["errors"])

    except Exception as e:
        report["errors"].append(f"Migration error: {str(e)}")
    finally:
        db.close()

    report["completed_at"] = datetime.now().isoformat()
    return report


def print_report(report: dict) -> None:
    """Print migration report to console."""
    print("=" * 60)
    print("  FT Workspace v2.0 — Migration Report")
    print("=" * 60)
    print()

    if report["errors"] and not report["migrated"]:
        print("  ERROR: Migration failed")
        for err in report["errors"]:
            print(f"    - {err}")
        return

    print(f"  CSV Source:     {report['csv_path']}")
    print(f"  Database:       {report['db_path']}")
    print(f"  CSV Rows:       {report['total_csv_rows']}")
    print(f"  Migrated:       {report['migrated']}")
    print(f"  Skipped:        {report['skipped']}")
    print()

    if report["category_summary"]:
        print("  Category Summary:")
        for cat, count in sorted(report["category_summary"].items()):
            print(f"    {cat:<25s}  {count:>4d} products")
        print()

    if report["warnings"]:
        print(f"  Warnings ({len(report['warnings'])}):")
        for w in report["warnings"][:10]:
            print(f"    - {w}")
        if len(report["warnings"]) > 10:
            print(f"    ... and {len(report['warnings']) - 10} more")
        print()

    if report["errors"]:
        print(f"  Errors ({len(report['errors'])}):")
        for e in report["errors"][:10]:
            print(f"    - {e}")
        if len(report["errors"]) > 10:
            print(f"    ... and {len(report['errors']) - 10} more")
        print()

    print(f"  Started:  {report['started_at']}")
    print(f"  Completed: {report['completed_at']}")
    print("=" * 60)


if __name__ == "__main__":
    # Default paths
    csv_path = os.path.join(
        PROJECT_ROOT,
        "04-database", "csv", "product_database_filled.csv"
    )
    db_path = None  # Auto-detect

    # Parse command line args
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--csv" and i + 1 < len(args):
            csv_path = args[i + 1]
            i += 2
        elif args[i] == "--db" and i + 1 < len(args):
            db_path = args[i + 1]
            i += 2
        elif args[i] == "--help":
            print("Usage: python migrate_v1_to_v2.py [--csv PATH] [--db PATH]")
            sys.exit(0)
        else:
            i += 1

    # Run migration
    report = migrate(csv_path, db_path)
    print_report(report)

    # Exit code
    if report["errors"] and report["migrated"] == 0:
        sys.exit(1)
    sys.exit(0)
