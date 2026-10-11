#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FT Workspace — 数据库初始化 / 种子数据脚本 (seed)

作用：把「任何一台电脑上都能复现的可用数据库」一键造出来。

数据库文件 (data/*.db) 已被 .gitignore 排除、不进版本控制，因此换机器时的
标准复现流程是：

    git clone  →  uv sync  →  python scripts/seed_db.py

脚本要做的事：
    1. 按 data/schema.sql 建表（幂等，IF NOT EXISTS）
    2. 导入产品主数据 data/seed/products.csv（215 条，UTF-8）
    3. 灌入业务演示数据（客户 / 市场报告 / 知识库 / 活动 / 报价 / 价格）
    4. 打印各表行数汇总，便于核对

用法：
    python scripts/seed_db.py                  # 幂等：已有数据的表不重复灌
    python scripts/seed_db.py --reset          # 重建表结构 + 重新灌数据（修复结构漂移）
    python scripts/seed_db.py --db <path>      # 指定数据库文件（测试用临时库）
    python scripts/seed_db.py --products-only  # 只灌产品，跳过业务演示数据

数据血缘：
    data/seed/products.csv 由 git 历史恢复而来
    （源文件 04-database/csv/product_database_filled.csv，
      存在于提交 e18efbc 的父提交，在「项目结构重组」时被删除）。
    恢复时做了两件事：GBK → UTF-8；剔除已废弃列 length_cm
    （该列已被 scripts/migrate_length_to_color.py 迁移为 color 列）。
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.database import FTDatabase            # noqa: E402
from src.m1_product_db.importer import import_csv   # noqa: E402

DEFAULT_DB = ROOT / "data" / "ft_workspace.db"
SCHEMA_SQL = ROOT / "data" / "schema.sql"
PRODUCTS_CSV = ROOT / "data" / "seed" / "products.csv"

# 业务表（--reset 时清空）。products 由 import_csv 以 INSERT OR REPLACE 覆盖，无需清空。
BUSINESS_TABLES = [
    "activities",
    "client_analyses",
    "client_tag_mapping",
    "client_tags",
    "clients",
    "content_records",
    "inquiries",
    "market_knowledge",
    "market_reports",
    "orders",
    "outreach_templates",
    "price_records",
    "product_images",
    "products",
    "quotation_items",
    "quotation_versions",
    "quotations",
]

# ============================================================
# 业务演示数据（内容与历史脚本 scripts/inject_test_data.py 一致）
# 注意：activities / quotations 通过 client_id 引用客户，
#       因此必须保证 clients 在 id=1..8 的状态下插入 —— 即需要先 --reset。
# ============================================================

CLIENTS = [
    ("AfroFarm Ltd", "Nigeria", "www.afrofarm.ng", "Chukwuemeka Obi", "chukwuemeka@afrofarm.ng", "+234****5678", "+234****5678", "", "importer", "Hand tools, farm implements", "West Africa", "50000", "A", 85, "alibaba", "Large importer of Chinese hand tools", "customer"),
    ("GreenFields GmbH", "Germany", "www.greenfields.de", "Hans Mueller", "hans@greenfields.de", "+493****3456", "+493****3456", "linkedin.com/in/hansmueller", "distributor", "Garden tools, professional farming", "Europe", "30000", "A", 78, "trade_show", "Premium European distributor", "customer"),
    ("Savanna Supplies", "Kenya", "www.savanna.co.ke", "James Mwangi", "james@savanna.co.ke", "+254****5678", "+254****5678", "", "retailer", "Farm tools, agricultural supplies", "East Africa", "20000", "B", 65, "referral", "Growing retailer in Kenya", "contacted"),
    ("Outback Agri", "Australia", "www.outbackagri.com.au", "Tom Wilson", "tom@outbackagri.com.au", "+614****5678", "+614****5678", "linkedin.com/in/tomwilson", "distributor", "Professional farming tools", "Oceania", "15000", "A", 72, "cold_call", "Interested in premium hoe range", "interested"),
    ("Ferme du Sahel", "Burkina Faso", "", "Ibrahim Compaore", "ibrahim@fermesahel.bf", "+226****3456", "+226****3456", "", "importer", "Basic farm tools", "West Africa", "10000", "C", 45, "website", "Small scale buyer", "quoted"),
    ("Baltic Tools OU", "Estonia", "www.baltictools.ee", "Marti Tamm", "marti@baltictools.ee", "+372****4567", "+372****4567", "linkedin.com/in/martitamm", "distributor", "Hand tools, construction", "Baltic/Nordic", "25000", "B", 60, "linkedin", "Expanding into farm tools", "contacted"),
    ("Zambezi Farm", "Zambia", "", "Grace Phiri", "grace@zambezifarm.zm", "+260****4567", "+260****4567", "", "retailer", "Farm implements, seeds", "Southern Africa", "8000", "D", 30, "referral", "", "lead"),
    ("AgriSolutions SA", "South Africa", "www.agrisolutions.co.za", "Pieter van der Berg", "pieter@agrisolutions.co.za", "+278****4567", "+278****4567", "linkedin.com/in/pvdberg", "distributor", "Professional agricultural tools", "Southern Africa", "40000", "A", 82, "trade_show", "Premium distributor, good volume", "negotiating"),
]

MARKET_REPORTS = [
    ("Nigeria", "Weeding Tools", "Nigeria Weeding Tools Market Report 2026",
     "Nigeria is Africa's largest farm tool market with 200M+ population. Weeding hoes dominate demand.",
     "Full report covering market size, competitive landscape, import regulations, pricing trends...",
     None, "Trade Ministry data, Alibaba trends", 0.75),
    ("Germany", "Cutting Tools", "German Garden Tool Market Analysis",
     "Germany leads European garden tool demand. Strong preference for professional-grade tools.",
     "Full analysis of German market including distribution channels, pricing, competition...",
     None, "Eurostat, Trade shows", 0.82),
    ("Kenya", "Digging Tools", "East Africa Agricultural Tools Demand",
     "Kenya is a gateway to East African market. Growing mechanization drives tool demand.",
     "Comprehensive analysis of East African farm tool market...",
     None, "Kenya Bureau of Statistics", 0.70),
]

MARKET_KNOWLEDGE = [
    ("Nigeria", "Weeding Tools", "Nigeria import duty on hand tools is 5-10%. No phytosanitary cert needed for metal tools.", "Trade Ministry", 1),
    ("Germany", "General", "CE marking mandatory for garden tools in EU market.", "EU Regulation", 1),
    ("Kenya", "Digging Tools", "KEBS certification required for imported hand tools. Process takes 4-6 weeks.", "Import Agent", 0),
    ("Australia", "Cutting Tools", "AS/NZS certification required for cutting tools.", "Trade Commission", 1),
]

ACTIVITIES = [
    (1, "email", "outbound", "Welcome email with catalog", "Sent full catalog", "completed", None, None, "2026-07-01"),
    (1, "whatsapp", "inbound", "Re: Catalog inquiry", "Interested in round head hoe", "completed", None, None, None),
    (1, "email", "outbound", "Quotation RHH-120", "Sent quote for RHH-120", "completed", None, "2026-07-10", None),
    (2, "email", "outbound", "Introduction premium range", "Hans responded positively", "completed", None, None, None),
    (2, "phone", "outbound", "Price negotiation call", "Discussed FOB pricing", "completed", None, "2026-07-08", None),
    (3, "email", "outbound", "Cold outreach Kenya", "Sent initial email", "completed", None, None, None),
    (5, "email", "inbound", "RFQ from Ferme du Sahel", "Looking for 3000pcs hoe", "completed", None, None, None),
    (5, "email", "outbound", "Quotation reply", "Sent CIF pricing", "completed", None, "2026-07-12", None),
    (8, "email", "outbound", "Premium catalog", "Pieter interested", "completed", None, None, None),
    (8, "meeting", "inbound", "Trade show follow-up", "Met at Hannover Messe", "completed", None, "2026-07-05", None),
    (4, "linkedin", "outbound", "Connection request", "Tom connected", "completed", None, None, None),
    (6, "email", "outbound", "Baltic market intro", "Sent catalog to Marti", "completed", None, None, None),
    (2, "email", "outbound", "Follow-up order confirmation", "Hans confirmed 3000pcs", "completed", None, "2026-07-15", None),
    (8, "whatsapp", "outbound", "Delivery timeline update", "Updated production status", "completed", None, "2026-07-20", None),
    (3, "email", "outbound", "Follow up catalog request", "Pending response", "pending", None, None, "2026-07-28"),
    (6, "email", "outbound", "Follow up Baltic tools", "Marti not responded", "pending", None, None, "2026-07-30"),
]

QUOTATIONS = [
    ("QT-2026-001", 1, "RHH-120", 2000, 3.50, "USD", "FOB", "Tianjin", "T/T 30/70", 30, 30, 7000, "", "", "accepted"),
    ("QT-2026-002", 2, "FGH-080", 5000, 4.20, "USD", "FOB", "Tianjin", "L/C at sight", 45, 30, 21000, "", "", "accepted"),
    ("QT-2026-003", 5, "FDH-100", 3000, 3.80, "USD", "CIF", "Ouagadougou", "T/T advance", 35, 15, 11400, "", "", "sent"),
    ("QT-2026-004", 8, "GGT-060", 1500, 8.50, "USD", "FOB", "Tianjin", "L/C at sight", 30, 30, 12750, "", "", "negotiating"),
    ("QT-2026-005", 1, "WCH-050", 3000, 2.80, "USD", "FOB", "Tianjin", "T/T 30/70", 25, 30, 8400, "", "", "sent"),
]

PRICE_RECORDS = [
    ("RHH-120", 2.50, 2.00, "West Africa", "2026-06-01", "Standard round head hoe"),
    ("FGH-080", 3.00, 2.40, "Europe", "2026-06-01", "Flat garden hoe"),
    ("FDH-100", 2.80, 2.20, "West Africa", "2026-06-01", "Flat digging hoe"),
    ("GGT-060", 6.00, 4.80, "Oceania", "2026-06-01", "Premium garden tool"),
    ("WCH-050", 2.00, 1.60, "Global", "2026-06-01", "Weeding hoe basic"),
]


# ============================================================
# 核心步骤
# ============================================================

def ensure_schema(conn: sqlite3.Connection) -> None:
    """按 schema.sql 建表（IF NOT EXISTS，可重复执行）。"""
    if not SCHEMA_SQL.exists():
        raise FileNotFoundError(f"找不到建表脚本: {SCHEMA_SQL}")
    conn.executescript(SCHEMA_SQL.read_text(encoding="utf-8"))
    conn.commit()


def rebuild_schema(conn: sqlite3.Connection) -> None:
    """DROP 全部业务表并按 schema.sql 重建（--reset 使用）。

    与逐表 DELETE 相比，DROP + CREATE 能一并消除「表结构漂移」：
    旧库的 products 表可能仍是 length_cm 时代的结构、缺少 color 列，
    此时仅 DELETE 数据不会修正结构，将导致 /analytics/api/products 等
    接口抛出 "no such column: color"。
    """
    conn.execute("PRAGMA foreign_keys=OFF")
    for table in BUSINESS_TABLES:
        conn.execute(f"DROP TABLE IF EXISTS {table}")
    try:
        conn.execute("DELETE FROM sqlite_sequence")
    except sqlite3.Error:
        pass
    conn.commit()
    ensure_schema(conn)
    conn.execute("PRAGMA foreign_keys=ON")


def seed_products(db: FTDatabase) -> dict:
    """导入产品主数据。import_csv 使用 INSERT OR REPLACE，天然幂等。"""
    if not PRODUCTS_CSV.exists():
        raise FileNotFoundError(f"找不到产品种子数据: {PRODUCTS_CSV}")
    return import_csv(str(PRODUCTS_CSV), encoding="utf-8", db=db)


def seed_business(conn: sqlite3.Connection) -> None:
    """灌入业务演示数据（客户有数据时跳过，保证幂等）。"""
    existing = conn.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
    if existing:
        print(f"  业务数据已存在（clients={existing} 行），跳过。用 --reset 可重建。")
        return

    conn.executemany(
        """INSERT INTO clients
           (company_name,country,website,contact_person,email,phone,whatsapp,linkedin,
            business_type,main_products,market_regions,estimated_volume,grade,grade_score,source,notes,status)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        CLIENTS,
    )
    conn.executemany(
        """INSERT INTO market_reports
           (country,product_category,report_title,summary,full_report,report_file,data_sources,confidence)
           VALUES (?,?,?,?,?,?,?,?)""",
        MARKET_REPORTS,
    )
    conn.executemany(
        "INSERT INTO market_knowledge (country,category,knowledge,source,verified) VALUES (?,?,?,?,?)",
        MARKET_KNOWLEDGE,
    )
    conn.executemany(
        """INSERT INTO activities
           (client_id,activity_type,direction,subject,content,status,scheduled_date,actual_date,follow_up_date)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        ACTIVITIES,
    )
    conn.executemany(
        """INSERT INTO quotations
           (quotation_no,client_id,product_code,quantity,unit_price,currency,incoterm,port,
            payment_terms,lead_time_days,validity_days,total_amount,email_body,quotation_file,status)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        QUOTATIONS,
    )
    conn.executemany(
        """INSERT INTO price_records
           (product_code,base_price_usd,min_price_usd,target_market,effective_date,notes)
           VALUES (?,?,?,?,?,?)""",
        PRICE_RECORDS,
    )
    conn.commit()
    print(f"  业务数据: {len(CLIENTS)} 客户 / {len(MARKET_REPORTS)} 市场报告 / "
          f"{len(MARKET_KNOWLEDGE)} 知识 / {len(ACTIVITIES)} 活动 / "
          f"{len(QUOTATIONS)} 报价 / {len(PRICE_RECORDS)} 价格记录")


def summary(db: FTDatabase) -> None:
    """打印各表行数，便于核对复现结果。"""
    print("\n各表行数：")
    for table in BUSINESS_TABLES:
        try:
            n = db.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  {table:<22} {n:>5}")
        except sqlite3.Error:
            print(f"  {table:<22}   (表不存在)")


def main() -> int:
    parser = argparse.ArgumentParser(description="FT Workspace 数据库初始化 / 种子数据")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="数据库文件路径（默认 data/ft_workspace.db）")
    parser.add_argument("--reset", action="store_true", help="清空全部业务数据后重新灌入")
    parser.add_argument("--products-only", action="store_true", help="只灌产品，跳过业务演示数据")
    args = parser.parse_args()

    db_path = Path(args.db).resolve()
    print("=" * 58)
    print("  FT Workspace — 数据库种子脚本")
    print("=" * 58)
    print(f"  数据库: {db_path}")
    print(f"  模式  : {'RESET 重建' if args.reset else '幂等初始化'}"
          f"{' / 仅产品' if args.products_only else ''}")

    db = FTDatabase(db_path=str(db_path))
    ensure_schema(db.conn)

    if args.reset:
        print("\n[1/3] 重建表结构（DROP + CREATE）...")
        rebuild_schema(db.conn)
        print("  已按 schema.sql 重建")

    print("\n[2/3] 导入产品主数据...")
    report = seed_products(db)
    print(f"  {PRODUCTS_CSV.name}: 共 {report['total_rows']} 行, "
          f"导入 {report['imported']}, 跳过 {report['skipped']}")
    for err in report["errors"][:5]:
        print(f"  ! {err}")
    if report["warnings"]:
        print(f"  ! {len(report['warnings'])} 条警告（前 3 条）：{report['warnings'][:3]}")

    if not args.products_only:
        print("\n[3/3] 灌入业务演示数据...")
        seed_business(db.conn)

    summary(db)
    db.close()
    print("\n完成。数据库已可复现。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
