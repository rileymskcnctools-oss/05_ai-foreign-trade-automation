"""
FT Workspace v2.0 — Streamlit Web界面
第7周：产品搜索 + AI内容生成完整工作台

启动方式: streamlit run app.py
"""
import os
import sys

# 项目路径守护伞
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from src.core.database import FTDatabase

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="FT Workspace v2.0",
    page_icon="🔨",
    layout="wide",
)

# ============================================================
# 数据库连接（使用缓存，避免每次刷新都重连）
# ============================================================
@st.cache_resource
def get_db():
    """获取数据库连接，Streamlit会缓存这个连接"""
    return FTDatabase()

db = get_db()

# ============================================================
# AI生成函数（复用CLI的逻辑）
# ============================================================
def generate_ai_content(product_code, content_type):
    """
    调用AI生成内容并保存到数据库
    返回: (success: bool, message: str)
    """
    import traceback
    from src.core.llm_client import LLMClient
    from src.utils.prompts import load_prompt, fill_prompt, build_product_data

    # 1. 获取产品数据
    product = db.product_get(product_code)
    if not product:
        return False, f"产品 {product_code} 不存在"

    # 2. 选择Prompt模板
    template_map = {
        "seo": "seo/alibaba_title",
        "selling_points": "seo/selling_points",
        "whatsapp": "social/whatsapp",
    }

    if content_type not in template_map:
        return False, f"不支持的类型: {content_type}"

    # 3. 加载模板并填充数据
    try:
        data = build_product_data(product)
        template = load_prompt(template_map[content_type])
        filled = fill_prompt(template, data)
    except Exception as e:
        tb = traceback.format_exc()
        return False, f"模板加载失败: {e}\n\n{tb}"

    # 4. 调用AI
    try:
        llm = LLMClient(scenario="seo_content")
        response = llm.chat(filled, max_tokens=1000, temperature=0.7)
    except Exception as e:
        tb = traceback.format_exc()
        return False, f"AI调用失败: {e}\n\n{tb}"

    # 5. 保存到数据库
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
            count = len([t for t in titles if t])
            return True, f"生成了 {count} 个SEO标题"

        elif content_type == "selling_points":
            db.execute(
                "UPDATE products SET selling_points=?, updated_at=datetime('now') WHERE product_code=?",
                (response.strip(), product_code)
            )
            return True, "卖点生成完成"

        elif content_type == "whatsapp":
            db.execute(
                "UPDATE products SET whatsapp_script=?, updated_at=datetime('now') WHERE product_code=?",
                (response.strip(), product_code)
            )
            return True, "WhatsApp话术生成完成"

        db.commit()
        return True, "保存成功"

    except Exception as e:
        return False, f"保存失败: {e}"


# ============================================================
# 侧边栏：搜索和筛选
# ============================================================
st.sidebar.title("🔍 产品搜索")

# 搜索框
search_query = st.sidebar.text_input("输入关键词", placeholder="如: shovel, hoe, rake...")

# 分类筛选
categories = db.execute("SELECT DISTINCT category FROM products WHERE category IS NOT NULL ORDER BY category").fetchall()
category_list = [c[0] for c in categories]
selected_category = st.sidebar.selectbox("产品分类", ["全部"] + category_list)

# ============================================================
# 主页面：标题
# ============================================================
st.title("🔨 Foreign Trade AI Workspace v2.0")
st.markdown("手动农具外贸AI工作台 — 产品数据库 + AI内容生成")

# ============================================================
# 查询产品列表
# ============================================================
def get_products(query=None, category=None, limit=50):
    """根据搜索词和分类查询产品"""
    sql = "SELECT product_code, product_name_en, category, material, length_cm, weight_kg FROM products WHERE 1=1"
    params = []

    if query:
        sql += " AND (product_code LIKE ? OR product_name_en LIKE ? OR product_name_cn LIKE ?)"
        like = f"%{query}%"
        params.extend([like, like, like])

    if category and category != "全部":
        sql += " AND category = ?"
        params.append(category)

    sql += f" ORDER BY product_code LIMIT {limit}"
    return db.execute(sql, params).fetchall()


# ============================================================
# 搜索结果展示
# ============================================================
products = get_products(
    query=search_query if search_query else None,
    category=selected_category
)

# 统计信息
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("搜索结果", f"{len(products)} 个产品")
with col2:
    total = db.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    st.metric("产品总数", f"{total} 个")
with col3:
    generated = db.execute("SELECT COUNT(*) FROM products WHERE seo_title_1 IS NOT NULL AND seo_title_1 != ''").fetchone()[0]
    st.metric("已生成SEO", f"{generated} 个")

st.divider()

# ============================================================
# 产品列表表格
# ============================================================
if not products:
    st.warning("没有找到匹配的产品，请尝试其他关键词")
else:
    # 用 DataFrame 展示产品列表
    import pandas as pd
    df = pd.DataFrame(products, columns=["产品编码", "英文名称", "分类", "材质", "长度(cm)", "重量(kg)"])
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    # ============================================================
    # 产品详情卡片
    # ============================================================
    st.subheader("📋 产品详情")

    # 让用户选择要查看的产品
    product_codes = [p[0] for p in products]
    selected_code = st.selectbox("选择产品查看详情", product_codes)

    if selected_code:
        # 获取完整产品数据
        product = db.execute(
            "SELECT * FROM products WHERE product_code = ?",
            (selected_code,)
        ).fetchone()

        if product:
            # 把数据库行转成字典（方便取值）
            col_names = [c[1] for c in db.execute("PRAGMA table_info(products)").fetchall()]
            prod_dict = dict(zip([c[1] for c in db.execute("PRAGMA table_info(products)").fetchall()], product))

            # 左右两栏布局
            left, right = st.columns([1, 1])

            with left:
                st.markdown("### 基本信息")
                st.write(f"**产品编码:** {prod_dict.get('product_code', '')}")
                st.write(f"**英文名称:** {prod_dict.get('product_name_en', '')}")
                st.write(f"**中文名称:** {prod_dict.get('product_name_cn', '')}")
                st.write(f"**分类:** {prod_dict.get('category', '')}")
                st.write(f"**子分类:** {prod_dict.get('sub_category', '')}")

                st.markdown("### 产品参数")
                st.write(f"**材质:** {prod_dict.get('material', '')}")
                st.write(f"**手柄材质:** {prod_dict.get('handle_material', '')}")
                st.write(f"**长度:** {prod_dict.get('length_cm', '')} cm")
                st.write(f"**重量:** {prod_dict.get('weight_kg', '')} kg")
                st.write(f"**头部宽度:** {prod_dict.get('head_width_cm', '')} cm")
                st.write(f"**硬度:** {prod_dict.get('hardness', '')}")
                st.write(f"**表面处理:** {prod_dict.get('surface_treatment', '')}")

            with right:
                st.markdown("### 包装与物流")
                st.write(f"**最小起订量:** {prod_dict.get('moq', '')}")
                st.write(f"**包装方式:** {prod_dict.get('packaging_type', '')}")
                st.write(f"**每箱数量:** {prod_dict.get('qty_per_carton', '')}")
                st.write(f"**箱规:** {prod_dict.get('carton_size_cm', '')}")
                st.write(f"**每箱毛重:** {prod_dict.get('gw_per_carton_kg', '')} kg")
                st.write(f"**交货期:** {prod_dict.get('lead_time_days', '')} 天")
                st.write(f"**认证:** {prod_dict.get('certification', '')}")

                st.markdown("### 装柜数量")
                st.write(f"**20ft:** {prod_dict.get('loading_qty_20ft', '')}")
                st.write(f"**40ft:** {prod_dict.get('loading_qty_40ft', '')}")
                st.write(f"**40HQ:** {prod_dict.get('loading_qty_40hq', '')}")

            st.divider()

            # ============================================================
            # 第7周新增：AI生成功能区
            # ============================================================
            st.subheader("🤖 AI内容生成")

            # 三个生成按钮并排
            gen_col1, gen_col2, gen_col3 = st.columns(3)

            with gen_col1:
                if st.button("📝 生成SEO标题", key="btn_seo", use_container_width=True):
                    with st.spinner("正在调用AI生成SEO标题..."):
                        success, msg = generate_ai_content(selected_code, "seo")
                    if success:
                        st.success(f"✅ {msg}")
                        st.rerun()  # 刷新页面显示新内容
                    else:
                        st.error(f"❌ {msg}")

            with gen_col2:
                if st.button("💡 生成卖点", key="btn_selling", use_container_width=True):
                    with st.spinner("正在调用AI生成卖点..."):
                        success, msg = generate_ai_content(selected_code, "selling_points")
                    if success:
                        st.success(f"✅ {msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

            with gen_col3:
                if st.button("📱 生成WhatsApp话术", key="btn_whatsapp", use_container_width=True):
                    with st.spinner("正在调用AI生成WhatsApp话术..."):
                        success, msg = generate_ai_content(selected_code, "whatsapp")
                    if success:
                        st.success(f"✅ {msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

            st.divider()

            # ============================================================
            # AI生成内容展示（已有内容显示，没有则提示）
            # ============================================================
            st.subheader("📄 AI生成结果")

            # SEO标题
            seo1 = prod_dict.get('seo_title_1', '')
            seo2 = prod_dict.get('seo_title_2', '')
            seo3 = prod_dict.get('seo_title_3', '')

            st.markdown("#### 📝 SEO标题（阿里国际站）")
            if seo1 or seo2 or seo3:
                if seo1:
                    st.info(f"**标题1:** {seo1}")
                if seo2:
                    st.info(f"**标题2:** {seo2}")
                if seo3:
                    st.info(f"**标题3:** {seo3}")
            else:
                st.warning("尚未生成，请点击上方「生成SEO标题」按钮")

            # 卖点
            selling = prod_dict.get('selling_points', '')
            st.markdown("#### 💡 产品卖点")
            if selling:
                st.text_area("卖点内容", selling, height=150, disabled=True, key="selling")
            else:
                st.warning("尚未生成，请点击上方「生成卖点」按钮")

            # WhatsApp话术
            whatsapp = prod_dict.get('whatsapp_script', '')
            st.markdown("#### 📱 WhatsApp话术")
            if whatsapp:
                st.text_area("话术内容", whatsapp, height=150, disabled=True, key="whatsapp")
            else:
                st.warning("尚未生成，请点击上方「生成WhatsApp话术」按钮")

            # 目标关键词和使用场景
            st.divider()
            st.subheader("🎯 市场信息")
            col_a, col_b = st.columns(2)
            with col_a:
                keywords = prod_dict.get('target_keywords', '')
                if keywords:
                    st.write(f"**目标关键词:** {keywords}")
                markets = prod_dict.get('target_markets', '')
                if markets:
                    st.write(f"**目标市场:** {markets}")
            with col_b:
                scenario = prod_dict.get('use_scenario', '')
                if scenario:
                    st.write(f"**使用场景:** {scenario}")
                angle = prod_dict.get('selling_angle', '')
                if angle:
                    st.write(f"**卖点角度:** {angle}")
