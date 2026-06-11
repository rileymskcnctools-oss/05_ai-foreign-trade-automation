"""
FT Workspace - Day 3 数据库实操练习
目标：
1. 查询全部产品
2. 查询指定产品 (如 GS-001)
3. 统计产品数量
"""

import os
# 1. 引入你在 Day 1 和 Day 2 见过的工具
from src.core.config import get_config
from src.core.database import FTDatabase

def main():
    # 2. 自动获取数据库的真实存放路径
    config = get_config()
    db_path = config.get_db_path()
    print(f"📡 正在连接账本，数据库路径为: {db_path}")
    
    # 检查数据库文件是否存在，防止新手找不到文件报错
    if not os.path.exists(db_path):
        print("❌ 错误：未找到数据库文件！请确保你运行脚本的位置在项目根目录，或者 data/ 目录下有 ft_workspace.db")
        return

    # 3. 打开账本（建立数据库连接）
    db = FTDatabase()

    try:
        # ==========================================================
        # 任务 1：查询全部产品
        # 运营场景：我想看看公海里现在总共有哪些货，批量捞出来备用。
        # ==========================================================
        print("\n====== 🚀 任务 1：查询全部产品 ======")
        
        # SQL 语句大白话："SELECT * FROM products" -> 从 products 表里挑选(SELECT) 所有列(*)
        # fetchall 表示“全都要”，把所有符合条件的老底全抽出来
        all_products = db.fetchall("SELECT * FROM products")
        
        print(f"成功捞出 {len(all_products)} 个产品：")
        for prod in all_products:
            # 这时的 prod 是一个干净的字典（Dict），可以直接用大括号的 Key 拿数据
           # 【盲改修复版】：用 .get() 查价格，万一没有 'price'，就返回 '未知'，绝不崩溃！
            product_price = prod.get('price') or prod.get('min_price') or '暂无价格'
            
            print(f"📦 产品编码: {prod.get('product_code', '无编码')} | "
                  f"英文名: {prod.get('product_name_en', '无英文名')} | "
                  f"单价: ${product_price}")
            
            # 【运营调试小外挂】：我们在第一条数据时，把大括号里的所有真相打印出来看看
            if prod == all_products[0]:
                print("\n💡 [运营小贴士] 系统里真实的数据标签长这样，快看看价格到底叫什么：")
                print(prod)
                print("==================================================================\n")


        # ==========================================================
        # 任务 2：查询指定产品 (以 GS-001 为例)
        # 运营场景：海外客户指名道姓要 GS-001 的资料，AI 需要精准把这一款的参数捞出来。
        # ==========================================================
        print("\n====== 🎯 任务 2：查询指定产品 (GS-001) ======")
        
        target_code = "GS-001"
        # SQL 语句大白话：从 products 表里查，但是有个硬性条件(WHERE)——产品编码必须等于问号(?)
        # fetchone 表示“只要一个”，因为编码是唯一的，查到一个就收工
        # 注意：为了防止黑客攻击（SQL注入），变量不能直接拼在字符串里，必须用问号占位，再在后面用括号 (target_code,) 传过去
        single_product = db.fetchone("SELECT * FROM products WHERE product_code = ?", (target_code,))
        
        if single_product:
            print(f"✅ 成功找到该产品！它在系统里的‘原材料字典’长这样：")
            print(single_product) 
            print(f"💡 运营提示：这个大括号格式的数据，今晚就可以直接喂给 DeepSeek 让他写 SEO 文案了！")
        else:
            print(f"❌ 警告：在数据库里没找到编码为 {target_code} 的产品。")


        # ==========================================================
        # 任务 3：统计产品数量
        # 运营场景：老板要听大盘汇报，想知道目前系统里总共录入了多少款产品。
        # ==========================================================
        print("\n====== 📊 任务 3：统计产品数量 ======")
        
        # SQL 语句大白话：COUNT(*) 表示“数一数总共多少行”，as total 是给数出来的结果起个临时名字叫 total
        count_result = db.fetchone("SELECT COUNT(*) as total FROM products")
        
        # 打印结果
        print(f"📈 统计报告：目前中央数据库中，总共管理着 {count_result['total']} 款外贸产品。")

    except Exception as e:
        print(f"💥 运行过程中碰到了钉子（报错）: {e}")
        
    finally:
        # 4. 不管成功还是失败，最后一定要记得合上账本（关闭连接），这是优秀运营的职业操守
        db.close()
        print("\n🔒 账本已安全合上，连接已断开。")

if __name__ == "__main__":
    main()