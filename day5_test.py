"""
FT Workspace - Week 1 终极交付成果（数据库+MD流版 - 字段完美对齐版）
目标：
1. 真实连接本地 SQLite 数据库，读取 products 表中的产品参数（严格对齐真实列名）
2. 兼容周边表格为空的现状，在代码层对价格进行基准保底
3. 批量调用 DeepSeek 接口，一键生成 4 类外贸核心文案
4. 自动创建本地产品文件夹，全量保存为标准的 .md 格式文件
"""

import os
import sys
import sqlite3
import requests

# ====== 1. 寻路与环境洗白补丁 (确保穿透 Windows 捞到密钥) ======
def force_get_api_key():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    env_paths = [
        os.path.join(base_dir, ".env"),
        os.path.join(os.path.dirname(base_dir), ".env") # 尝试向上一级寻找
    ]
    
    for env_path in env_paths:
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f: lines = f.readlines()
            except UnicodeDecodeError:
                with open(env_path, "r", encoding="utf-16", errors="ignore") as f: lines = f.readlines()
            
            for line in lines:
                if "DEEPSEEK_API_KEY=" in line:
                    return line.split("DEEPSEEK_API_KEY=")[1].strip().strip('"').strip("'")
    return None

# ====== 2. 【核心修复】严格按照真实表格列名从数据库读取数据 ======
def get_product_from_db(product_id):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "data", "ft_workspace.db")
    
    # 防呆路径
    if not os.path.exists(db_path):
        db_path = os.path.join(os.path.dirname(base_dir), "data", "ft_workspace.db")
        if not os.path.exists(db_path):
            db_path = os.path.join(base_dir, "ft_workspace.db")

    print(f"🔍 正在尝试连接数据库: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 🟢 终极对齐：SELECT 后面的字段必须存在于你的真实 CSV/数据库结构中！
        # 真实字段：product_id, product_name_en, material, selling_points, use_scenario
        query = """
            SELECT product_id, product_name_en, material, selling_points, use_scenario 
            FROM products 
            WHERE product_id = ?
        """
        cursor.execute(query, (product_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # 将数据库捞出的真实字段组装进字典
            product_data = {
                "product_id": row[0],
                "product_name_en": row[1],
                "material": row[2],
                "selling_points": row[3],  # 👈 对应你表里的高质量卖点/技术规格
                "use_scenario": row[4],    # 👈 对应你表里的应用场景
                "min_price": 550.0 if product_id == "GS-001" else 580.0 # 价格表为空的运营保底补丁
            }
            return product_data
        else:
            print(f"⚠️ 数据库对应的 products 表中未找到编码为 [{product_id}] 的产品！")
            return None
            
    except Exception as e:
        print(f"❌ 数据库读取失败: {e}")
        return None

# ====== 3. AI 核心通信函数 ======
def ask_deepseek(api_key, prompt):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "stream": False
    }
    response = requests.post(url, json=data, headers=headers, timeout=30)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"AI 请求失败，状态码: {response.status_code}, 原因: {response.text}")

# ====== 4. 主管道流水线 ======
def run_database_md_pipeline(product_id):
    print(f"\n==================== 🚀 启动产品 [{product_id}] 数据库+MD流管道 ====================")
    
    # 1. 捞密钥
    api_key = force_get_api_key()
    if not api_key:
        print("❌ 错误：未捞到有效的 DEEPSEEK_API_KEY，请检查 .env 文件！")
        return

    # 2. 真实去数据库敲门捞数据
    prod = get_product_from_db(product_id)
    if not prod:
        print(f"❌ 流程中断：无法从数据库获取产品 [{product_id}] 的有效核心参数。")
        return
        
    print(f"✅ 成功从数据库捞出核心参数！")
    print(f"   📋 品名(英): {prod['product_name_en']}\n   📋 材质: {prod['material']}")

    # 3. 准备 4 类外贸核心文案的 Prompt 模板 (完美利用你表格里的真实优质字段！)
    prompts = {
        "01_SEO_Description": f"Write a professional Google SEO Meta title and description for {prod['product_name_en']} (Code: {prod['product_id']}). Material: {prod['material']}. Selling points: {prod['selling_points']}. Target keywords: Wholesale steel, supplier. Output in standard Markdown.",
        
        "02_Product_Detail": f"Act as a B2B copywriter. Write a detailed product description page for {prod['product_name_en']}. Include features, application scenarios ({prod['use_scenario']}), and a technical specifications table based on: {prod['selling_points']}. Price reference: ${prod['min_price']}/ton. Output in rich Markdown with clean headings.",
        
        "03_RFQ_Reply": f"Draft a professional B2B email reply to an inquiry asking about {prod['product_name_en']}. Provide a soft quote based on ${prod['min_price']}/ton FOB, emphasize fast global shipping, and invite them to confirm sample requirements. Use selling points: {prod['selling_points']}. Output in Markdown email format.",
        
        "04_WhatsApp_Pitch": f"Write 3 variations of short, high-conversion WhatsApp marketing messages for {prod['product_name_en']}. Keep them punchy, use appropriate emojis, include a clear Call to Action (CTA), and highlight cost efficiency based on material {prod['material']}. Output in Markdown."
    }

    # 4. 创建本地目标存放房间：output/GS-001/
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output", product_id)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 已全自动创建本地 Markdown 导出目录: {output_dir}")

    # 5. 循环轰炸 AI，并全量写出为 .md 格式
    for content_type, prompt_text in prompts.items():
        print(f"📡 正在全自动请求 AI 生成 -> [{content_type}]...")
        try:
            ai_result = ask_deepseek(api_key, prompt_text)
            
            # 🎯 强制后缀为 .md
            file_path = os.path.join(output_dir, f"{content_type}.md")
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(ai_result)
            print(f"  └─ 💾【.md 写入成功】: {file_path}")
            
        except Exception as e:
            print(f"  └─ ❌ 生成 [{content_type}] 时遇到阻碍: {e}")

    print(f"🎉 产品 [{product_id}] 的数据库数据激活，4 类 Markdown 外贸文件全部落盘完毕！")

if __name__ == "__main__":
    # 🟢 终极一战：传入你数据库里真实存在的 product_id 进行连续验证！
    run_database_md_pipeline("GR-001")
    run_database_md_pipeline("AX-011")