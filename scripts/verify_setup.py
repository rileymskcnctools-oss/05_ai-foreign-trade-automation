"""
FT Workspace v2.0 — Quick verification script.

Run this to verify the v2.0 setup is working correctly.

Usage:
    python scripts/verify_setup.py
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


def check(description, condition, detail=""):
    status = "OK" if condition else "FAIL"
    icon = "+" if condition else "x"
    line = f"  [{icon}] {description}"
    if detail and condition:
        line += f"  ({detail})"
    elif detail and not condition:
        line += f"  -- {detail}"
    print(line)
    return condition


def verify():
    print("=" * 60)
    print("  FT Workspace v2.0 — Setup Verification")
    print("=" * 60)
    print()

    all_ok = True

    # 1. Directory structure
    required_dirs = [
        "config", "data", "data/backups", "data/imports/products",
        "src", "src/core", "src/models",
        "src/m1_product_db", "src/m2_marketing", "src/m3_seo",
        "src/m4_market_research", "src/m5_client_analysis",
        "src/m6_outreach", "src/m7_quotation", "src/m8_crm", "src/m9_analytics",
        "src/agents", "src/utils",
        "prompts", "prompts/seo", "prompts/outreach",
        "templates", "templates/catalog",
        "output", "output/catalogs", "output/quotations", "output/reports",
        "assets", "assets/images",
        "ui", "scripts", "tests", "docs",
    ]
    print("Directories:")
    for d in required_dirs:
        exists = os.path.isdir(os.path.join(PROJECT_ROOT, d))
        all_ok &= check(d, exists)

    # 2. Core files
    print("\nCore files:")
    required_files = {
        "data/schema.sql": "Database schema",
        "data/ft_workspace.db": "SQLite database",
        "config/settings.yaml": "Settings",
        "config/.env.example": "Env template",
        "src/core/__init__.py": "Core package",
        "src/core/database.py": "Database module",
        "scripts/migrate_v1_to_v2.py": "Migration script",
        "README.md": "Project README",
        "docs/PROJECT_DOCUMENTATION_v2.md": "Full docs",
    }
    for path, desc in required_files.items():
        exists = os.path.isfile(os.path.join(PROJECT_ROOT, path))
        all_ok &= check(desc, exists, path)

    # 4. Database content
    print("\nDatabase:")
    try:
        from src.core.database import FTDatabase
        from src.m1_product_db.search import search, filter_products, get_categories
        from src.m1_product_db.exporter import export_csv
        from src.m1_product_db.cleaner import find_missing_fields

        db = FTDatabase()

        count = db.product_count()
        all_ok &= check("Products in DB", count == 215, f"{count}")

        sample = db.product_get("GF-001")
        all_ok &= check("Product GF-001 readable", sample is not None)
        if sample:
            all_ok &= check("  Name matches", sample["product_name_en"] == "Garden Fork")

        stats = db.stats_summary()
        all_ok &= check("Stats API works", stats["products"] == 215,
                       f"products={stats['products']}, clients={stats['clients']}")

        # Search test
        results = search("garden fork", db=db, limit=5)
        all_ok &= check("Search works", len(results) >= 3, f"{len(results)} results")

        # Filter test
        heavy = filter_products(db=db, min_weight=1.0, limit=5)
        all_ok &= check("Filter works", len(heavy) > 0, f"{len(heavy)} products >= 1kg")

        # Categories test
        cats = get_categories(db=db)
        all_ok &= check("Categories work", len(cats) == 3, f"{len(cats)} categories")

        # Missing fields test
        missing = find_missing_fields(db=db, fields=["hs_code", "loading_qty_20ft"])
        all_ok &= check("Missing fields check", "hs_code" in missing,
                       f"{len(missing.get('hs_code', []))} products missing HS code")

        # Config test
        from src.core.config import get_config
        cfg = get_config()
        all_ok &= check("Config loads", cfg.get("app.name") == "FT Workspace")
        all_ok &= check("Config DB path", "ft_workspace.db" in cfg.get_db_path())

        db.close()
    except ImportError as e:
        all_ok &= check("Module import", False, str(e))
    except Exception as e:
        all_ok &= check("Database access", False, str(e))

    # 4. Legacy files preserved
    print("\nLegacy (v1.0) files preserved:")
    legacy_files = [
        "04-database/csv/product_database_filled.csv",
        "02-prompts/seo/seo_title_prompt.md",
        "02-prompts/detail_page/alibaba_detail_prompt.md",
        "02-prompts/rfq/rfq_reply_prompt.md",
        "02-prompts/whatsapp/whatsapp_script_prompt.md",
        "08-git/README.md",
        "07-docs/SOP/operation_manual.md",
    ]
    for f in legacy_files:
        exists = os.path.isfile(os.path.join(PROJECT_ROOT, f))
        all_ok &= check(f, exists)

    # 5. Git status
    print("\nGit:")
    git_dir = os.path.join(PROJECT_ROOT, ".git")
    all_ok &= check(".git directory exists", os.path.isdir(git_dir))

    # Summary
    print()
    print("=" * 60)
    if all_ok:
        print("  Result: ALL CHECKS PASSED")
    else:
        print("  Result: SOME CHECKS FAILED — review above")
    print("=" * 60)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(verify())
