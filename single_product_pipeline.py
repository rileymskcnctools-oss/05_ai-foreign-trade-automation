"""
FT Workspace - 单产品 AI 内容生成流水线 (v2.0 适配版)
===================================================
运行命令:
  python single_product_pipeline.py GS-001
  python single_product_pipeline.py GS-001 GF-001 GR-001
  python single_product_pipeline.py          (默认跑 GS-001 + GF-001)

工作流:
  1. 定位项目根目录 (当前文件所在目录)
  2. 读取 API Key (.env 或 config/.env)
  3. 从 SQLite 数据库取出产品完整参数
  4. 加载 02-prompts/ 下的 prompt 模板并填充变量
  5. 调用 DeepSeek 生成内容
  6. 保存到 output/{产品编码}/ 目录
"""

import os
import sys
import re
import sqlite3
import requests


# ============================================================
# 1. 项目根目录定位
# ============================================================
def get_project_root():
    """
    当前文件 single_product_pipeline.py 已在项目根目录，
    直接返回 __file__ 所在目录即可。
    """
    return os.path.dirname(os.path.abspath(__file__))


# ============================================================
# 2. 读取 API Key（依次尝试根目录 .env → config/.env）
# ============================================================
def get_api_key():
    """从 .env 文件中读取 DEEPSEEK_API_KEY"""
    root = get_project_root()

    env_paths = [
        os.path.join(root, ".env"),
        os.path.join(root, "config", ".env"),
    ]

    for env_path in env_paths:
        if not os.path.exists(env_path):
            continue
        try:
            # 先用二进制读入，自动判断编码 (UTF-16 / UTF-8)
            with open(env_path, "rb") as f:
                raw = f.read()
            try:
                text = raw.decode("utf-16")
            except UnicodeDecodeError:
                text = raw.decode("utf-8")

            for line in text.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "DEEPSEEK_API_KEY=" in line:
                    key = line.split("DEEPSEEK_API_KEY=", 1)[1].strip().strip('"').strip("'")
                    if key and not key.startswith("sk-your"):
                        return key
        except Exception:
            continue

    return None


# ============================================================
# 3. 从 SQLite 数据库读取产品完整参数
# ============================================================
def get_product(product_id):
    """
    读取 products 表中指定产品编码的【全部字段】，
    返回 dict，key 就是数据库列名。
    """
    root = get_project_root()
    db_path = os.path.join(root, "data", "ft_workspace.db")

    if not os.path.exists(db_path):
        print(f"❌ 数据库不存在: {db_path}")
        return None

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            print(f"❌ 产品编码 [{product_id}] 在数据库中不存在！")
            return None

        return dict(row)

    except Exception as e:
        print(f"❌ 数据库读取失败: {e}")
        return None


# ============================================================
# 4. Prompt 模板映射 & 加载填充
# ============================================================

# 内容类型 → (prompt子目录和文件名, 输出文件名前缀)
PROMPT_MAP = {
    "SEO": {
        "prompt_path": ("02-prompts", "seo", "seo_title_prompt.md"),
        "output_name": "01_SEO_Description.md",
    },
    "Detail": {
        "prompt_path": ("02-prompts", "detail_page", "selling_points_prompt.md"),
        "output_name": "02_Product_Detail.md",
    },
    "RFQ": {
        "prompt_path": ("02-prompts", "rfq", "rfq_reply_prompt.md"),
        "output_name": "03_RFQ_Reply.md",
    },
    "WhatsApp": {
        "prompt_path": ("02-prompts", "whatsapp", "whatsapp_script_prompt.md"),
        "output_name": "04_WhatsApp_Pitch.md",
    },
}


def load_prompt(content_type, product_data):
    """
    1. 从 02-prompts/ 加载 markdown 模板文件
    2. 提取 ``` 代码块内的纯 prompt 文本（跳过顶部说明）
    3. 将 ${key} 格式的占位符替换为产品实际数据
    返回填充好的 prompt 字符串
    """
    root = get_project_root()
    info = PROMPT_MAP[content_type]
    prompt_path = os.path.join(root, *info["prompt_path"])

    if not os.path.exists(prompt_path):
        print(f"  ⚠️  Prompt 文件不存在: {prompt_path}")
        return None

    with open(prompt_path, "r", encoding="utf-8") as f:
        raw = f.read()

    # --- 提取 ``` 代码块里的纯 prompt ---
    # 文件结构: 顶部是说明，然后 ``` 包裹着真正的 prompt 模板
    code_block = None
    if "```" in raw:
        parts = raw.split("```")
        if len(parts) >= 3:
            code_block = parts[1].strip()
            # 去掉可能的语言标记 (如 ```text 或 ```prompt)
            first_line, _, rest = code_block.partition("\n")
            if first_line.strip().lower() in ("text", "prompt", "md", ""):
                code_block = rest.strip()

    template = code_block if code_block else raw

    # --- 准备填充数据 ---
    data = dict(product_data)

    # 补充 prompt 需要但数据库里没有的字段 (提供合理默认值)
    fill_defaults = {
        "specifications": _build_specs_str(data),
        "unit": "tines" if data.get("tine_count") else "",
        "price_range": "USD 2.5 - 5.0 (FOB Tianjin)",
        "rfq_content": "(请将此行替换为买家 RFQ 原文)",
        "customer_type": "wholesaler",
        "target_market": data.get("target_markets") or "Global",
        "target_country": data.get("target_markets") or "Global",
        "market_info": "(请从 04-database/output/market_knowledge.md 补充)",
        "annual_capacity": "500,000 pcs/year",
        "factory_years": "15",
        "export_markets": data.get("target_markets") or "Global",
        "factory_size": "10,000 sqm",
        "employee_count": "200+",
        "factory_certifications": data.get("certification") or "ISO 9001, BSCI",
    }
    for k, v in fill_defaults.items():
        if k not in data or not data[k]:
            data[k] = v

    # --- 替换 ${key} 占位符 ---
    filled = template
    for key, value in data.items():
        placeholder = "${" + key + "}"
        if placeholder in filled:
            filled = filled.replace(placeholder, str(value) if value is not None else "")

    # 处理残留的未匹配 ${...} 标记（替换为空，避免提示词里留乱码）
    filled = re.sub(r'\$\{[^}]+\}', '', filled)

    return filled


def _build_specs_str(data):
    """拼接产品规格字符串，如 '23cm, 0.8kg, 14tines'"""
    parts = []
    if data.get("length_cm"):
        parts.append(f"{data['length_cm']}cm")
    if data.get("weight_kg"):
        parts.append(f"{data['weight_kg']}kg")
    if data.get("tine_count"):
        parts.append(f"{int(data['tine_count'])}tines")
    if data.get("head_width_cm"):
        parts.append(f"head {data['head_width_cm']}cm")
    return ", ".join(parts) if parts else "Contact for specs"


# ============================================================
# 5. AI 核心通信 (DeepSeek API)
# ============================================================
def ask_ai(api_key, prompt, model="deepseek-chat"):
    """调用 DeepSeek Chat API，返回生成的文本"""
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "stream": False,
    }

    response = requests.post(url, json=payload, headers=headers, timeout=60)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(
            f"AI 请求失败 [HTTP {response.status_code}]: {response.text[:300]}"
        )


# ============================================================
# 6. 主流水线
# ============================================================
def run_pipeline(product_id):
    """为单个产品生成全套 AI 营销内容"""
    print(f"\n{'=' * 55}")
    print(f"🚀  启动产品 [{product_id}] AI 内容生成流水线")
    print(f"{'=' * 55}")

    # Step 1: API Key
    api_key = get_api_key()
    if not api_key:
        print("❌ 未找到有效的 DEEPSEEK_API_KEY！")
        print("   请检查项目根目录 .env 或 config/.env")
        return

    # Step 2: 产品数据
    product = get_product(product_id)
    if not product:
        return
    print(f"✅ 产品数据已加载: {product.get('product_name_en', product_id)}")
    print(f"   类别: {product.get('category', '-')} | 材质: {product.get('material', '-')}")

    # Step 3: 创建输出目录
    root = get_project_root()
    output_dir = os.path.join(root, "output", product_id)
    os.makedirs(output_dir, exist_ok=True)

    # Step 4: 逐个内容类型生成
    results = {}
    for content_type, info in PROMPT_MAP.items():
        print(f"\n📡 [{content_type}] 加载模板 → {info['prompt_path'][-1]} ...")

        try:
            prompt = load_prompt(content_type, product)
            if not prompt:
                results[content_type] = False
                continue

            result = ask_ai(api_key, prompt)

            filepath = os.path.join(output_dir, info["output_name"])
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(result)

            # 显示生成内容的前 80 个字符作为预览
            preview = result[:80].replace("\n", " ").strip()
            print(f"  ✅ 已保存: {filepath}")
            print(f"     预览: {preview}...")
            results[content_type] = True

        except Exception as e:
            print(f"  ❌ 失败: {e}")
            results[content_type] = False

    # Step 5: 汇总报告
    success_count = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"\n{'=' * 55}")
    print(f"🎉  产品 [{product_id}] 流水线完成: {success_count}/{total} 类内容生成成功")
    print(f"📂  输出目录: {output_dir}")

    if success_count < total:
        failed = [k for k, v in results.items() if not v]
        print(f"⚠️  失败项: {', '.join(failed)}")

    print(f"{'=' * 55}")
    return results


# ============================================================
# 入口: 支持命令行传参或默认测试
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 指定产品编码: python single_product_pipeline.py GS-001 GF-001
        for pid in sys.argv[1:]:
            run_pipeline(pid.strip())
    else:
        # 默认跑两个代表性产品 (花园铁锹 + 花园叉)
        run_pipeline("GS-001")
        run_pipeline("GF-001")
