# 📄 文件路径：03-workflows/python/day05_content_generator.py
import os
import sys
import time
import traceback
import argparse
from datetime import datetime
import pandas as pd
from day05_ai_client import call_ai_agent

# 统一维护项目根路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_PATH = os.path.join(PROJECT_ROOT, '04-database', 'csv', 'product_database_filled.csv')

# ======================================================================
# 📦 模块一：数据库核心底层加载中心
# ======================================================================
def load_products_dataframe():
    """多编码鲁棒性加载 CSV 数据库"""
    if not os.path.exists(CSV_PATH):
        return None
    for enc in ('utf-8-sig', 'utf-8', 'gbk', 'latin1'):
        try:
            df = pd.read_csv(CSV_PATH, encoding=enc)
            df.columns = df.columns.str.strip()
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"⚠️ 读取异常 ({enc}): {e}")
    return None

def get_garden_tools_data(product_id: str) -> dict:
    """提取单个产品的参数字典并完成基础清洗"""
    df = load_products_dataframe()
    if df is None:
        print("⚠️ 未找到数据库文件，启动兜底应急测试数据包...")
        return {
            'product_name_en': 'Heavy Duty Garden Rake with Carbon Steel Tines',
            'product_id': product_id, 'category': 'Garden Hand Tools',
            'material': 'High Carbon Steel', 'hardness': '45-48 HRC',
            'use_scenario': 'Soil loosening, agricultural cultivation',
            'selling_angle': 'Military-grade hardness steel tines',
            'factory_years': '15', 'annual_capacity': '2,000,000 pcs',
            'target_markets': 'North America, Western Europe, Australia'
        }
    
    first_col = df.columns[0]
    df[first_col] = df[first_col].astype(str).str.strip()
    product_row = df[df[first_col] == str(product_id).strip()]
    
    if product_row.empty:
        print(f"❌ 数据库中未找到产品编码: {product_id}")
        return None
        
    raw_dict = product_row.iloc[0].to_dict()
    return {k.strip(): ("Premium Standard" if pd.isna(v) or str(v).lower() == 'nan' or str(v).strip() == '' else str(v).strip()) for k, v in raw_dict.items()}


# ======================================================================
# 🛠️ 模块二：核心变量爆破替换引擎
# ======================================================================
def inject_variables_to_template(template_text: str, p_data: dict) -> str:
    """防冲突自适应变量爆破引擎，支持各种大小写和驼峰格式占位符"""
    final_prompt = template_text
    replace_count = 0
    
    def to_camel(s: str) -> str:
        parts = s.split('_')
        return parts[0] + ''.join(p.title() for p in parts[1:]) if len(parts) > 1 else s

    for key, value in p_data.items():
        candidates = set()
        k = key.strip()
        # 搜集各种可能在模板里出现的格式：${product_id}, ${productId}, $product_id ...
        for wrapper in [f"${{{k}}}", f"${{{k.lower()}}}", f"${{{to_camel(k)}}}", f"${k}", f"${k.lower()}", f"${to_camel(k)}"]:
            candidates.add(wrapper)
        for ph in candidates:
            if ph in final_prompt:
                final_prompt = final_prompt.replace(ph, str(value))
                replace_count += 1
                
    return final_prompt, replace_count


# ======================================================================
# 🚀 模块三：多内容矩阵自动化一键生成车间
# ======================================================================
def generate_single_product_pipeline(product_id: str):
    """【Week 1 终极任务】一键读取参数，组合4套模板，批量生产全套 AI 外贸资料包"""
    print(f"\n========================================================")
    print(f"🚀 启动产品 [{product_id}] 全套出海内容自动化流水线...")
    print(f"========================================================")
    
    # 1. 抓取结构化数据
    p_data = get_garden_tools_data(product_id)
    if not p_data:
        print(f"❌ 获取产品数据失败，流程终止。")
        return
        
    # 2. 定义 4 类文案的配置矩阵（模板文件名 -> 期望输出的文件名）
    tasks_matrix = {
        "seo_title_template.txt": "seo_copywriting.md",
        "alibaba_detail_template.txt": "alibaba_details_final.md",
        "rfq_reply_template.txt": "rfq_response.md",
        "whatsapp_script_template.txt": "whatsapp_outreach.md"
    }
    
    # 准备输出目录和错误日志文件
    output_dir = os.path.join(PROJECT_ROOT, '05-output', product_id)
    os.makedirs(output_dir, exist_ok=True)
    errors_path = os.path.join(output_dir, 'process_errors.txt')
    
    success_count = 0
    
    # 3. 遍历任务矩阵，挨个处理
    for template_name, output_filename in tasks_matrix.items():
        template_path = os.path.join(PROJECT_ROOT, '03-workflows', 'python', 'prompt_templates', template_name)
        final_output_path = os.path.join(output_dir, output_filename)
        
        print(f"\n📂 正在处理文案维度: [{output_filename}]")
        
        # 检查对应的模板是否存在
        if not os.path.exists(template_path):
            print(f"   ⚠️ 提示：未在路径下发现模板 {template_name}，跳过此项生产。")
            continue
            
        # 读取模板
        with open(template_path, 'r', encoding='utf-8-sig') as f:
            template_text = f.read()
            
        # 参数卡位爆破
        final_prompt, replaced = inject_variables_to_template(template_text, p_data)
        print(f"   🔁 数据注入完成，精准替换了 {replaced} 个模板参数占位符。")
        
        # 调用大模型生成（带错误重试机制机制）
        print(f"   📡 正在向 Hermes 模型提交定制 Prompt ...")
        actual_ai_text = None
        max_attempts = 3
        
        for attempt in range(1, max_attempts + 1):
            try:
                # 针对不同性质的文案提供超时安全边界
                actual_ai_text = call_ai_agent(final_prompt, timeout_seconds=180)
                break
            except Exception as e:
                msg = f"[{datetime.now().isoformat()}] [{output_filename}] 失败尝试 {attempt}：{e}\n{traceback.format_exc()}\n"
                with open(errors_path, 'a', encoding='utf-8') as ef:
                    ef.write(msg)
                print(f"   ⏳ 遇到波动，正在进行第 {attempt} 次重试...")
                time.sleep(3 * attempt)
                
        if actual_ai_text is None:
            print(f"   ❌ 该单项内容调用 AI 失败，详情请看错误日志。")
            continue
            
        # 结果文件安全落盘
        with open(final_output_path, 'w', encoding='utf-8-sig') as f:
            f.write(actual_ai_text)
            
        print(f"   ✅ 生成成功！已安全写入文件：05-output/{product_id}/{output_filename}")
        success_count += 1
        time.sleep(1) # 在不同大任务间加入平滑延迟，防止频繁请求触发限流
        
    print(f"\n========================================================")
    print(f"🎉 【流水线作业完毕】产品 [{product_id}] 的自动化加工圆满结束！")
    print(f"📦 成功产出: {success_count}/{len(tasks_matrix)} 个高质量内容资产包。")
    print(f"📁 结果均保存在：05-output/{product_id}/")
    print(f"========================================================")


# ======================================================================
# 🎮 中央指挥调度台
# ======================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='外贸全自动化内容生成管线 - 单品一键全包版')
    parser.add_argument('product_id', nargs='?', default='GS-001', help='GF-001 或 GF-002')
    args = parser.parse_args()
    
    # 启动一键跑通管线
    generate_single_product_pipeline(args.product_id)