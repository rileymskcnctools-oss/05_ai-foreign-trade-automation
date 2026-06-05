"""
FT Workspace v2.0 — Quick CLI tool

Usage:
    python scripts/ft_cli.py stats
    python scripts/ft_cli.py search "garden fork"
    python scripts/ft_cli.py list --category "Digging Tools"
    python scripts/ft_cli.py get GF-001
    python scripts/ft_cli.py export output/my_export.csv
    python scripts/ft_cli.py missing
"""

import os
import sys
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.core.database import FTDatabase
from src.m1_product_db.search import search, filter_products, get_categories
from src.m1_product_db.exporter import export_csv
from src.m1_product_db.cleaner import find_missing_fields


def cmd_stats(db):
    """Show system statistics."""
    stats = db.stats_summary()
    cats = get_categories(db)

    print("FT Workspace v2.0 — System Stats")
    print("=" * 40)
    print(f"  Products:       {stats['products']}")
    print(f"  Clients:        {stats['clients']}")
    print(f"  Activities:     {stats['total_activities']}")
    print(f"  Quotations:     {stats['total_quotations']}")
    print(f"  Inquiries:      {stats['total_inquiries']}")
    print()
    print("Categories:")
    for c in cats:
        print(f"  {c['category']:<20s}  {c['product_count']:>4d} products")


def cmd_search(db, query):
    """Search products."""
    results = search(query, db=db, limit=20)
    if not results:
        print(f"No products found for '{query}'")
        return

    print(f"Search '{query}' — {len(results)} results:")
    print("-" * 60)
    for r in results:
        print(f"  {r['product_code']:<10s}  {r['product_name_en']:<35s}  {r['category']}")


def cmd_list(db, category=None, limit=20):
    """List products."""
    if category:
        products = filter_products(db=db, category=category, limit=limit)
        print(f"Category: {category} — {len(products)} products:")
    else:
        products = db.product_list(limit=limit)
        print(f"All products — showing {len(products)}:")

    print("-" * 60)
    for p in products:
        print(f"  {p['product_code']:<10s}  {p['product_name_en']:<35s}  {p['category']}")


def cmd_get(db, product_code):
    """Get product details."""
    product = db.product_get(product_code)
    if not product:
        print(f"Product '{product_code}' not found")
        return

    print(f"Product: {product_code}")
    print("=" * 60)
    for key, value in product.items():
        if value is not None:
            display = str(value)
            if len(display) > 80:
                display = display[:80] + "..."
            print(f"  {key:<25s}: {display}")
        else:
            print(f"  {key:<25s}: (empty)")


def cmd_export(db, filepath):
    """Export products to CSV."""
    report = export_csv(filepath, db=db)
    if report["errors"]:
        print(f"Export failed: {report['errors']}")
    else:
        print(f"Exported {report['exported']} products to {report['filepath']}")


def cmd_missing(db):
    """Show missing fields."""
    missing = find_missing_fields(db=db)
    if not missing:
        print("All required fields are filled!")
        return

    print("Missing fields:")
    for field, codes in missing.items():
        print(f"  {field}: {len(codes)} products missing")
        if len(codes) <= 10:
            for c in codes:
                print(f"    - {c}")
        else:
            for c in codes[:5]:
                print(f"    - {c}")
            print(f"    ... and {len(codes) - 5} more")


def print_help():
    print("FT Workspace v2.0 CLI")
    print()
    print("Usage: python scripts/ft_cli.py <command> [args]")
    print()
    print("Commands:")
    print("  stats                        Show system statistics")
    print("  search <query>               Search products")
    print("  list [--category CAT]        List products")
    print("  get <product_code>           Get product details")
    print("  export <filepath>            Export to CSV")
    print("  missing                      Show missing fields")
    print("  help                         Show this help")


def main():
    args = sys.argv[1:]
    if not args or args[0] == "help":
        print_help()
        return

    command = args[0]
    db = FTDatabase()

    try:
        if command == "stats":
            cmd_stats(db)
        elif command == "search":
            query = " ".join(args[1:]) if len(args) > 1 else ""
            if not query:
                print("Usage: ft_cli.py search <query>")
                return
            cmd_search(db, query)
        elif command == "list":
            category = None
            if "--category" in args:
                idx = args.index("--category")
                if idx + 1 < len(args):
                    category = args[idx + 1]
            cmd_list(db, category=category)
        elif command == "get":
            if len(args) < 2:
                print("Usage: ft_cli.py get <product_code>")
                return
            cmd_get(db, args[1])
        elif command == "export":
            if len(args) < 2:
                print("Usage: ft_cli.py export <filepath>")
                return
            cmd_export(db, args[1])
        elif command == "missing":
            cmd_missing(db)
        else:
            print(f"Unknown command: {command}")
            print_help()
    finally:
        db.close()


if __name__ == "__main__":
    main()
