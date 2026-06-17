"""
FT Workspace v2.0 — Quick CLI tool (外贸AI工作台命令行总控制器)

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
    missing = find_missing_fields(db=db) # 揪出缺失字段的产品清单
    if not missing:
        print("All required fields are filled!")
        return

    print("Missing fields:")
    # 循环告诉运营：比如有 10 个产品缺“产品尺寸”，有 5 个产品缺“包装信息”
    for field, codes in missing.items():
        print(f"  {field}: {len(codes)} products missing")
        # 如果缺的产品少于10个，把产品编码全部打出来；如果太多，就只打前5个，剩下的省略
        if len(codes) <= 10:
            for c in codes:
                print(f"    - {c}")
        else:
            for c in codes[:5]:
                print(f"    - {c}")
            print(f"    ... and {len(codes) - 5} more")


def cmd_generate(db, product_code, content_type="seo"):
    """
    【命令六: AI内容生成器】对应: python scripts/ft_cli.py generate GF-001 --type seo

    数据管道: 数据库产品数据 -> Prompt模板填充 -> AI生成 -> 结果回写数据库

    支持的 content_type:
      - seo: 生成3个阿里国际站SEO标题
      - selling_points: 生成5个产品卖点
      - whatsapp: 生成WhatsApp开发话术
    """
    from src.core.llm_client import LLMClient
    from src.utils.prompts import load_prompt, fill_prompt, build_product_data

    # 第一步: 从数据库获取产品数据
    product = db.product_get(product_code)
    if not product:
        print(f"❌ 产品 {product_code} 不存在")
        return False

    print(f"📦 产品: {product.get('product_name_en', 'Unknown')}")
    print(f"📋 生成类型: {content_type}")

    # 第二步: 根据类型选择对应的 Prompt 模板
    template_map = {
        "seo": "seo/alibaba_title",
        "selling_points": "seo/selling_points",
        "whatsapp": "social/whatsapp",
    }

    if content_type not in template_map:
        print(f"❌ 不支持的类型: {content_type}")
        print(f"   支持的类型: {', '.join(template_map.keys())}")
        return False

    # 第三步: 加载模板并填充产品数据
    try:
        data = build_product_data(product)
        template = load_prompt(template_map[content_type])
        filled = fill_prompt(template, data)
    except Exception as e:
        print(f"❌ 模板加载失败: {e}")
        return False

    # 第四步: 调用 AI 生成内容
    print("🤖 正在调用 AI 生成...")
    try:
        llm = LLMClient(scenario="seo_content")
        response = llm.chat(filled, max_tokens=1000, temperature=0.7)
    except Exception as e:
        print(f"❌ AI 调用失败: {e}")
        return False

    # 第五步: 把 AI 生成的结果保存回数据库
    try:
        if content_type == "seo":
            titles = [line.strip() for line in response.strip().split("\n")
                      if line.strip() and len(line.strip()) > 10]
            titles = titles[:3]
            while len(titles) < 3:
                titles.append("")

            db.execute(
                "UPDATE products SET seo_title_1=?, seo_title_2=?, seo_title_3=?, "
                "updated_at=datetime('now') WHERE product_code=?",
                (titles[0], titles[1], titles[2], product_code)
            )
            print(f"\n✅ 生成完成! 共 {len([t for t in titles if t])} 个标题:")
            for i, t in enumerate(titles, 1):
                if t:
                    print(f"  标题{i}: {t}")

        elif content_type == "selling_points":
            db.execute(
                "UPDATE products SET selling_points=?, updated_at=datetime('now') WHERE product_code=?",
                (response.strip(), product_code)
            )
            print(f"\n✅ 卖点生成完成!")

        elif content_type == "whatsapp":
            db.execute(
                "UPDATE products SET whatsapp_script=?, updated_at=datetime('now') WHERE product_code=?",
                (response.strip(), product_code)
            )
            print(f"\n✅ WhatsApp 话术生成完成!")

        db.commit()
        print(f"💾 已保存到数据库")
        return True

    except Exception as e:
        print(f"❌ 保存失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def cmd_generate_all(db, content_types=None, max_retries=3, limit=None):
    """
    【第5周新增: 批量AI生成器】对应: python scripts/ft_cli.py generate --all

    批量为所有产品生成AI内容，支持:
      - 失败重试（默认3次）
      - 日志记录到 output/generate_log.txt
      - 实时进度显示
      - 生成状态汇总
      - --limit N 限制处理数量（测试用）
    """
    import time
    import datetime
    from src.core.llm_client import LLMClient
    from src.utils.prompts import load_prompt, fill_prompt, build_product_data

    if content_types is None:
        content_types = ["seo", "selling_points", "whatsapp"]

    # 获取所有产品
    products = db.product_list(limit=9999)
    if not products:
        print("❌ 数据库中没有产品")
        return

    # 如果设置了 limit，只取前 N 个产品
    if limit and limit > 0:
        products = products[:limit]

    total = len(products)
    print("=" * 60)
    print("FT Workspace v2.0 — 批量生成")
    print("=" * 60)
    print(f"  产品总数: {total}")
    print(f"  生成类型: {', '.join(content_types)}")
    print(f"  最大重试: {max_retries} 次")
    print()

    # 初始化日志文件
    log_dir = os.path.join(PROJECT_ROOT, "output")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "generate_log.txt")

    # 状态统计
    stats = {"success": 0, "failed": 0, "skipped": 0, "retries": 0}
    start_time = time.time()

    template_map = {
        "seo": "seo/alibaba_title",
        "selling_points": "seo/selling_points",
        "whatsapp": "social/whatsapp",
    }

    def log_msg(msg):
        """写入日志文件"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {msg}\n")

    log_msg(f"========== 批量生成开始 ==========")
    log_msg(f"产品总数: {total}, 生成类型: {content_types}")

    for idx, product in enumerate(products, 1):
        code = product["product_code"]
        name = product.get("product_name_en", "Unknown")
        progress = f"[{idx}/{total}]"

        print(f"\n{progress} {code} — {name}")

        for ctype in content_types:
            if ctype not in template_map:
                continue

            success = False
            for attempt in range(1, max_retries + 1):
                try:
                    # 获取完整产品数据
                    full_product = db.product_get(code)
                    if not full_product:
                        print(f"  ⏭️  {ctype}: 产品不存在，跳过")
                        stats["skipped"] += 1
                        log_msg(f"SKIP {code} {ctype}: 产品不存在")
                        success = True  # 标记为已处理
                        break

                    # 加载模板并填充
                    data = build_product_data(full_product)
                    template = load_prompt(template_map[ctype])
                    filled = fill_prompt(template, data)

                    # 调用 AI
                    llm = LLMClient(scenario="seo_content")
                    response = llm.chat(filled, max_tokens=1000, temperature=0.7)

                    # 保存到数据库
                    if ctype == "seo":
                        titles = [line.strip() for line in response.strip().split("\n")
                                  if line.strip() and len(line.strip()) > 10][:3]
                        while len(titles) < 3:
                            titles.append("")
                        db.execute(
                            "UPDATE products SET seo_title_1=?, seo_title_2=?, seo_title_3=?, "
                            "updated_at=datetime('now') WHERE product_code=?",
                            (titles[0], titles[1], titles[2], code)
                        )
                    elif ctype == "selling_points":
                        db.execute(
                            "UPDATE products SET selling_points=?, updated_at=datetime('now') WHERE product_code=?",
                            (response.strip(), code)
                        )
                    elif ctype == "whatsapp":
                        db.execute(
                            "UPDATE products SET whatsapp_script=?, updated_at=datetime('now') WHERE product_code=?",
                            (response.strip(), code)
                        )

                    db.commit()
                    print(f"  ✅ {ctype} 生成成功")
                    log_msg(f"OK {code} {ctype}")
                    success = True
                    break

                except Exception as e:
                    if attempt < max_retries:
                        print(f"  ⚠️  {ctype} 第{attempt}次失败: {e}，重试中...")
                        log_msg(f"RETRY {code} {ctype} attempt {attempt}: {e}")
                        stats["retries"] += 1
                        time.sleep(2 * attempt)  # 递增等待
                    else:
                        print(f"  ❌ {ctype} 失败（已重试{max_retries}次）: {e}")
                        log_msg(f"FAIL {code} {ctype}: {e}")

            if success:
                stats["success"] += 1
            else:
                stats["failed"] += 1

    # 最终汇总
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)

    print()
    print("=" * 60)
    print("批量生成完成!")
    print("=" * 60)
    print(f"  ✅ 成功: {stats['success']}")
    print(f"  ❌ 失败: {stats['failed']}")
    print(f"  ⏭️  跳过: {stats['skipped']}")
    print(f"  🔄 重试次数: {stats['retries']}")
    print(f"  ⏱️  总耗时: {minutes}分{seconds}秒")
    print(f"  📝 日志文件: {log_path}")

    log_msg(f"========== 批量生成结束 ==========")
    log_msg(f"成功: {stats['success']}, 失败: {stats['failed']}, 跳过: {stats['skipped']}, 重试: {stats['retries']}, 耗时: {minutes}分{seconds}秒")


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
    print("  generate <code> [--type TYPE]  Generate AI content (seo/selling_points/whatsapp)")
    print("  generate all [--type TYPE]     Batch generate for ALL products")
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

        elif command == "generate":
            if len(args) < 2:
                print("Usage: ft_cli.py generate <product_code|all> [--type seo|selling_points|whatsapp]")
                print("       ft_cli.py generate all                    # 批量生成全部产品")
                print("       ft_cli.py generate all --type seo          # 批量只生成SEO")
                return

            # 检查是否是 --all 批量模式
            if args[1] == "all":
                content_types = ["seo", "selling_points", "whatsapp"]
                limit = None
                if "--type" in args:
                    idx = args.index("--type")
                    if idx + 1 < len(args):
                        content_types = [args[idx + 1]]
                if "--limit" in args:
                    idx = args.index("--limit")
                    if idx + 1 < len(args):
                        try:
                            limit = int(args[idx + 1])
                        except ValueError:
                            print("❌ --limit 必须是数字")
                            return
                cmd_generate_all(db, content_types=content_types, limit=limit)
            else:
                product_code = args[1]
                content_type = "seo"
                if "--type" in args:
                    idx = args.index("--type")
                    if idx + 1 < len(args):
                        content_type = args[idx + 1]
                cmd_generate(db, product_code, content_type)
        
        else:
            print(f"Unknown command: {command}")
            print_help()
            
    finally:
        # 【全盘安全铁律】：不管前面的命令是成功运行了，还是直接闪退崩溃了，
        # 处于 `finally` 里面的 `db.close()` 保证百分之百会被执行，随手切断数据库连接，防死锁。
        db.close()


if __name__ == "__main__":
    main()