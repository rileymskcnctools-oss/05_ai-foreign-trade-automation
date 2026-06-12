"""
FT Workspace v2.0 — Quick CLI tool (外贸AI工作台命令行总控制器)

【第二周运营官视角】：
这个脚本是整个工作台的“前台营业厅”。你敲击的各种快捷命令（如 stats, search, get）都会由它接收。
在第二周的开发目标中，这里将是扩展 `python ft_cli.py generate GS-001 --type seo` 指令的主战场。
"""

import os
import sys
import json

# ============================================================
# 【项目路径守护伞】
# ============================================================
# 动态获取当前脚本的上一级目录（即项目根目录），并强行加入系统环境变量
# 运营价值：确保在任何安装路径下，脚本都能顺畅使用 `from src.core...` 导入其他核心模块，不会报错“找不到模块”
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# 从第一周和第二周的核心模块中导入数据库、搜索、导出、清洗工具
from src.core.database import FTDatabase
from src.m1_product_db.search import search, filter_products, get_categories
from src.m1_product_db.exporter import export_csv
from src.m1_product_db.cleaner import find_missing_fields


# ============================================================
# 📊 【业务命令指挥中心】：每个函数对应终端的一个具体指令
# ============================================================

def cmd_stats(db):
    """
    【命令一：系统大盘看板】对应：python scripts/ft_cli.py stats
    运营价值：每天一早来看一眼：目前公海库里有多少产品、积压了多少询盘和报价，以及产品分类的分布。
    """
    stats = db.stats_summary()  # 连向第一周的数据库，拉取总盘统计字典
    cats = get_categories(db)   # 从搜索模块获取所有的产品品类及对应数量

    print("FT Workspace v2.0 — System Stats")
    print("=" * 40)
    print(f"  Products:       {stats['products']}")
    print(f"  Clients:        {stats['clients']}")
    print(f"  Activities:     {stats['total_activities']}")
    print(f"  Quotations:     {stats['total_quotations']}")
    print(f"  Inquiries:      {stats['total_inquiries']}")
    print()
    print("Categories:")
    # 动态循环打印品类列表，:<20s 表示左对齐占20个字符空间，:>4d 表右对齐，保证终端排版极其整齐
    for c in cats:
        print(f"  {c['category']:<20s}  {c['product_count']:>4d} products")


def cmd_search(db, query):
    """
    【命令二：模糊查品机】对应：python scripts/ft_cli.py search "关键字"
    运营价值：当海外客户在 WhatsApp 上突然问起某个品类，业务员可以在终端秒查前20个匹配的产品。
    """
    results = search(query, db=db, limit=20) # 模糊搜索关键词，最多吐出20条
    if not results:
        print(f"No products found for '{query}'")
        return

    print(f"Search '{query}' — {len(results)} results:")
    print("-" * 60)
    for r in results:
        # 打印出产品编码、英文名称和所属类目，方便一目了然
        print(f"  {r['product_code']:<10s}  {r['product_name_en']:<35s}  {r['category']}")


def cmd_list(db, category=None, limit=20):
    """
    (仅供阅读/本周停用) 【命令三：分类列表机】对应：python scripts/ft_cli.py list --category "分类名"
    运营价值：按照产品大类（如 Digging Tools）批量盘点产品。
    """
    if category:
        # 如果用户指定了品类，就调用过滤函数
        products = filter_products(db=db, category=category, limit=limit)
        print(f"Category: {category} — {len(products)} products:")
    else:
        # 如果没指定，默认展示全部产品的前20条
        products = db.product_list(limit=limit)
        print(f"All products — showing {len(products)}:")

    print("-" * 60)
    for p in products:
        print(f"  {p['product_code']:<10s}  {p['product_name_en']:<35s}  {p['category']}")


def cmd_get(db, product_code):
    """
    💡【⚡第二周最核心关联函数⚡】：精确查品机 对应：python scripts/ft_cli.py get GF-001
    
    【第二周通关核心点】：
    本周你要做的 `generate` 命令，其核心第一步就是“抄”这个函数的底层：
    必须先通过 `db.product_get(product_code)` 把产品的英文名、材质、参数全部变成 Python 字典，
    大模型（LLM）才能够有原材料去喂出 SEO 标题！
    """
    product = db.product_get(product_code) # 去数据库精准捞出这个产品编码的这一行完整资料
    if not product:
        print(f"Product '{product_code}' not found")
        return

    print(f"Product: {product_code}")
    print("=" * 60)
    # 把数据库里的多达十几个字段循环展示
    for key, value in product.items():
        if value is not None:
            display = str(value)
            # 【细节容错】：万一某个字段的内容巨长（比如描述字段超过80字），在终端截断加省略号，防止刷屏
            if len(display) > 80:
                display = display[:80] + "..."
            print(f"  {key:<25s}: {display}")
        else:
            print(f"  {key:<25s}: (empty)")


def cmd_export(db, filepath):
    """
    (仅供阅读/本周停用) 【命令四：海关独立站一键交货】对应：python scripts/ft_cli.py export 路径.csv
    运营价值：把系统里的爆款产品一键导出为标准的 CSV 表格，直接拿去上传 Shopify 独立站，或者发给大包商。
    """
    report = export_csv(filepath, db=db)
    if report["errors"]:
        print(f"Export failed: {report['errors']}")
    else:
        print(f"Exported {report['exported']} products to {report['filepath']}")


def cmd_missing(db):
    """
    【命令五：数据漏斗清洗器】对应：python scripts/ft_cli.py missing
    
    【第二周运营大白话】：
    这个函数太牛了，它是自动化运营的“纪检委”。它能帮你扫出哪些产品还没有填写核心字段。
    在第二周的业务流里，AI 生成完 SEO 标题后会保存数据库。你可以通过运行这个命令，
    一眼看清还有多少产品的 `seo_title` 字段是（empty）漏填状态。
    """
    missing = find_missing_fields(db=db)
    if not missing:
        print("All required fields are filled!")
        return

    print("Missing Fields Report:")
    print("=" * 50)
    for field, codes in sorted(missing.items(), key=lambda x: -len(x[1])):
        print(f"  {field:25s} {len(codes):>4d} products missing")
        if len(codes) <= 5:
            for c in codes:
                print(f"    - {c}")
        else:
            for c in codes[:3]:
                print(f"    - {c}")
            print(f"    ... and {len(codes) - 3} more")


def print_help():
    """
    【终端说明书】
    当员工在终端胡乱输入，或者输入 help 时，系统吐出这个规范的菜单向导。
    """
    print("FT Workspace v2.0 CLI")
    print()
    print("Usage: python scripts/ft_cli.py <command> [args]")
    print()
    print("Commands:")
    print("  stats                       Show system statistics")
    print("  search <query>               Search products")
    print("  list [--category CAT]        List products")
    print("  get <product_code>           Get product details")
    print("  export <filepath>            Export to CSV")
    print("  missing                      Show missing fields")
    print("  help                         Show this help")


# ============================================================
# 🧭 【终端总线路由器】（程序入口）
# ============================================================
def main():
    # sys.argv 用于捕捉你在黑窗口敲下的所有单词。
    # 比如敲了 `python ft_cli.py search fork`，那么 args 就是 ['search', 'fork']
    args = sys.argv[1:]
    
    # 兜底：如果直接运行脚本啥也没敲，或者敲了 help，就打印说明书
    if not args or args[0] == "help":
        print_help()
        return

    command = args[0] # 第一个单词是我们的核心“遥控按钮”（command）
    db = FTDatabase() # 瞬间启动第一周的数据库连接

    try:
        # ============================================================
        # 🎛️ 路由分发大闸开关
        # ============================================================
        if command == "stats":
            cmd_stats(db)
            
        elif command == "search":
            # 把 search 后面所有的参数拼成一句话作为搜索词
            query = " ".join(args[1:]) if len(args) > 1 else ""
            if not query:
                print("Usage: ft_cli.py search <query>")
                return
            cmd_search(db, query)
            
        elif command == "list":
            # 精准抓取命令行里有没有传递 `--category` 过滤选项
            category = None
            if "--category" in args:
                idx = args.index("--category")
                if idx + 1 < len(args):
                    category = args[idx + 1] # 拿到分类名
            cmd_list(db, category=category)
            
        elif command == "get":
            if len(args) < 2:
                print("Usage: ft_cli.py get <product_code>")
                return
            cmd_get(db, args[1]) # 执行精确查品
            
        elif command == "export":
            if len(args) < 2:
                print("Usage: ft_cli.py export <filepath>")
                return
            cmd_export(db, args[1])
            
        elif command == "missing":
            cmd_missing(db)
            
        else:
            # 💡 第二周的项目任务：你需要在下面追加一个 `elif command == "generate":` 分支！
            print(f"Unknown command: {command}")
            print_help()
            
    finally:
        # 【全盘安全铁律】：不管前面的命令是成功运行了，还是直接闪退崩溃了，
        # 处于 `finally` 里面的 `db.close()` 保证百分之百会被执行，随手切断数据库连接，防死锁。
        db.close()


if __name__ == "__main__":
    main()