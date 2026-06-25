"""
FT Workspace v2.0 — Streamlit Web界面
完整版：产品管理 + 市场研究 + 客户CRM + 开发信 + 报价 + 数据分析

启动方式: streamlit run app.py
"""
import os
import sys

# 项目路径守护伞
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
from src.core.database import FTDatabase

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="FT Workspace v2.0",
    page_icon="🔨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 数据库连接
# ============================================================
@st.cache_resource
def get_db():
    return FTDatabase()

db = get_db()

# ============================================================
# 侧边栏导航
# ============================================================
st.sidebar.title("🔨 FT Workspace v2.0")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "导航",
    [
        "📊 数据概览",
        "📦 产品管理",
        "🔍 市场研究",
        "👥 客户CRM",
        "⭐ 客户分析",
        "📧 开发信",
        "💰 报价助手",
        "📈 数据分析",
    ],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.caption("Powered by AI | v2.0")

# ============================================================
# 工具函数
# ============================================================
def get_client_list():
    """获取客户列表"""
    return db.fetchall("SELECT id, company_name, country, grade FROM clients ORDER BY company_name")

def get_product_list():
    """获取产品列表"""
    return db.fetchall(
        "SELECT product_code, product_name_en, category FROM products WHERE status='active' ORDER BY product_code"
    )

# ============================================================
# Page 1: 数据概览 (Dashboard)
# ============================================================
if page == "📊 数据概览":
    st.title("📊 数据概览")
    
    from src.m9_analytics import DashboardData
    dashboard = DashboardData(db)
    stats = dashboard.quick_stats()
    
    # KPI卡片
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("活跃产品", stats["active_products"])
    with c2:
        st.metric("客户总数", stats["total_clients"])
    with c3:
        st.metric("报价单", stats["total_quotations"])
    with c4:
        st.metric("市场报告", stats["market_reports"])
    with c5:
        st.metric("本周活动", stats["weekly_activities"])
    
    st.divider()
    
    # 首页仪表盘
    home = dashboard.home_data()
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📦 产品分布")
        if home["products"]["categories"]:
            cat_df = pd.DataFrame(home["products"]["categories"])
            st.bar_chart(cat_df.set_index("name")["count"])
        else:
            st.info("暂无产品分类数据")
    
    with col_right:
        st.subheader("👥 客户状态")
        if home["clients"]["by_status"]:
            status_df = pd.DataFrame(home["clients"]["by_status"])
            st.bar_chart(status_df.set_index("status")["count"])
        else:
            st.info("暂无客户数据")
    
    st.divider()
    
    # 缺SEO预警（替代库存预警）
    st.subheader("⚠️ SEO内容缺失产品")
    alerts = db.fetchall(
        "SELECT product_code, product_name_en, category FROM products WHERE status='active' AND (seo_title_1 IS NULL OR seo_title_1 = '') ORDER BY product_name_en LIMIT 10"
    )
    if alerts:
        st.dataframe(pd.DataFrame(alerts), use_container_width=True, hide_index=True)
    else:
        st.success("所有产品SEO内容已完善")


# ============================================================
# Page 2: 产品管理
# ============================================================
elif page == "📦 产品管理":
    st.title("📦 产品管理")
    
    search_col, cat_col = st.columns([3, 1])
    with search_col:
        query = st.text_input("搜索产品", placeholder="编码/名称...")
    with cat_col:
        categories = db.fetchall("SELECT DISTINCT category FROM products WHERE category IS NOT NULL ORDER BY category")
        cat_list = [c["category"] for c in categories]
        selected_cat = st.selectbox("分类", ["全部"] + cat_list)
    
    # 查询
    sql = "SELECT product_code, product_name_en, product_name_cn, category, material, length_cm, weight_kg FROM products WHERE 1=1"
    params = []
    if query:
        sql += " AND (product_code LIKE ? OR product_name_en LIKE ?)"
        like = f"%{query}%"
        params.extend([like, like])
    if selected_cat != "全部":
        sql += " AND category = ?"
        params.append(selected_cat)
    sql += " ORDER BY product_code LIMIT 50"
    products = db.fetchall(sql, tuple(params))
    
    st.write(f"**{len(products)} 个产品**")
    
    if products:
        df = pd.DataFrame(products, columns=["编码", "英文名", "中文名", "分类", "材质", "长度cm", "重量kg"])
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # 产品详情
        st.divider()
        st.subheader("产品详情")
        codes = [p["product_code"] for p in products]
        selected = st.selectbox("选择产品", codes)
        
        if selected:
            product = db.fetchone("SELECT * FROM products WHERE product_code = ?", (selected,))
            if product:
                product = dict(product)
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.write(f"**编码:** {product.get('product_code', '')}")
                    st.write(f"**英文名:** {product.get('product_name_en', '')}")
                    st.write(f"**分类:** {product.get('category', '')}")
                    st.write(f"**材质:** {product.get('material', '')}")
                with c2:
                    st.write(f"**长度:** {product.get('length_cm', '')} cm")
                    st.write(f"**重量:** {product.get('weight_kg', '')} kg")
                    st.write(f"**MOQ:** {product.get('moq', '')}")
                    st.write(f"**交期:** {product.get('lead_time_days', '')} 天")
                with c3:
                    st.write(f"**20ft装柜:** {product.get('loading_qty_20ft', '')}")
                    st.write(f"**40ft装柜:** {product.get('loading_qty_40ft', '')}")
                    st.write(f"**40HQ装柜:** {product.get('loading_qty_40hq', '')}")
                    st.write(f"**表面处理:** {product.get('surface_treatment', '')}")
    else:
        st.warning("未找到匹配的产品")


# ============================================================
# Page 3: 市场研究 (M4)
# ============================================================
elif page == "🔍 市场研究":
    st.title("🔍 市场研究 Agent")
    st.caption("AI自动生成目标市场研究报告")
    
    tab1, tab2, tab3 = st.tabs(["生成报告", "历史报告", "市场知识库"])
    
    with tab1:
        st.subheader("生成新报告")
        
        col1, col2 = st.columns(2)
        with col1:
            report_country = st.text_input("目标国家", placeholder="如: Nigeria, Kenya, Germany...")
            report_type = st.selectbox("报告类型", [
                "country_profile",
                "competitor_analysis", 
                "demand_analysis",
                "trade_policy",
            ])
        with col2:
            custom_focus = st.text_area("关注重点（可选）", placeholder="如: 关注农具进口政策、竞品价格区间...")
            product_code = st.text_input("关联产品编码（可选）")
        
        if st.button("🚀 生成市场报告", use_container_width=True):
            if not report_country:
                st.error("请输入目标国家")
            else:
                with st.spinner(f"正在生成 {report_country} 市场研究报告..."):
                    try:
                        from src.m4_market_research import MarketResearchAgent
                        agent = MarketResearchAgent(db)
                        extra = f"报告类型: {report_type}"
                        if custom_focus:
                            extra += f"; 关注重点: {custom_focus}"
                        if product_code:
                            extra += f"; 关联产品: {product_code}"
                        result = agent.generate_report(
                            country=report_country,
                            extra_context=extra,
                        )
                        if "error" in result:
                            st.error(f"生成失败: {result['error']}")
                        else:
                            st.success("✅ 报告生成成功！")
                            st.json(result)
                    except Exception as e:
                        st.error(f"错误: {e}")
    
    with tab2:
        st.subheader("历史报告")
        reports = db.fetchall(
            "SELECT id, country, product_category, report_title, confidence, created_at FROM market_reports ORDER BY created_at DESC LIMIT 20"
        )
        if reports:
            df = pd.DataFrame(reports, columns=["ID", "国家", "类型", "标题", "评分", "日期"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            report_id = st.selectbox("查看报告", [r["id"] for r in reports])
            if st.button("加载报告"):
                rpt = db.fetchone("SELECT * FROM market_reports WHERE id = ?", (report_id,))
                if rpt:
                    rpt = dict(rpt)
                    st.markdown(f"### {rpt.get('report_title', 'Untitled')}")
                    st.write(f"**国家:** {rpt.get('country', '')} | **评分:** {rpt.get('confidence', '')}")
                    if rpt.get("summary"):
                        st.markdown("**摘要:**")
                        st.write(rpt["summary"])
                    if rpt.get("full_report"):
                        st.markdown("**详细报告:**")
                        st.write(rpt["full_report"])
        else:
            st.info("暂无历史报告")
    
    with tab3:
        st.subheader("市场知识库")
        knowledge = db.fetchall(
            "SELECT country, category, knowledge, created_at FROM market_knowledge ORDER BY created_at DESC LIMIT 30"
        )
        if knowledge:
            df = pd.DataFrame(knowledge, columns=["国家", "分类", "知识点", "日期"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("知识库暂无内容，生成报告后会自动提取知识点")


# ============================================================
# Page 4: 客户CRM (M8)
# ============================================================
elif page == "👥 客户CRM":
    st.title("👥 客户CRM")
    
    tab1, tab2, tab3, tab4 = st.tabs(["客户列表", "新建客户", "跟进记录", "提醒"])
    
    with tab1:
        st.subheader("客户列表")
        
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            status_filter = st.selectbox("状态", ["全部", "lead", "contacted", "interested", "quoted", "negotiating", "customer", "lost"])
        with filter_col2:
            grade_filter = st.selectbox("评级", ["全部", "A", "B", "C", "D"])
        with filter_col3:
            country_filter = st.text_input("国家筛选")
        
        sql = "SELECT id, company_name, contact_person, country, grade, status, email, whatsapp FROM clients WHERE 1=1"
        params = []
        if status_filter != "全部":
            sql += " AND status = ?"
            params.append(status_filter)
        if grade_filter != "全部":
            sql += " AND grade = ?"
            params.append(grade_filter)
        if country_filter:
            sql += " AND country LIKE ?"
            params.append(f"%{country_filter}%")
        sql += " ORDER BY company_name LIMIT 50"
        
        clients = db.fetchall(sql, tuple(params))
        if clients:
            df = pd.DataFrame(clients, columns=["ID", "公司", "联系人", "国家", "评级", "状态", "邮箱", "WhatsApp"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("暂无客户数据")
    
    with tab2:
        st.subheader("新建客户")
        with st.form("new_client"):
            c1, c2 = st.columns(2)
            with c1:
                company = st.text_input("公司名称 *")
                contact = st.text_input("联系人")
                email = st.text_input("邮箱")
                whatsapp = st.text_input("WhatsApp")
            with c2:
                country = st.text_input("国家")
                business_type = st.text_input("业务类型")
                main_products = st.text_input("主营产品")
                grade = st.selectbox("评级", ["", "A", "B", "C", "D"])
            
            if st.form_submit_button("💾 保存客户"):
                if not company:
                    st.error("请输入公司名称")
                else:
                    from src.m8_crm import ClientManager
                    mgr = ClientManager(db)
                    cid = mgr.create({
                        "company_name": company,
                        "contact_person": contact,
                        "email": email,
                        "whatsapp": whatsapp,
                        "country": country,
                        "business_type": business_type,
                        "main_products": main_products,
                        "grade": grade or None,
                    })
                    st.success(f"✅ 客户创建成功！ID: {cid}")
    
    with tab3:
        st.subheader("跟进记录")
        clients_list = get_client_list()
        if clients_list:
            client_map = {f"{c['company_name']} ({c['country']})": c['id'] for c in clients_list}
            selected_client = st.selectbox("选择客户", list(client_map.keys()))
            
            if selected_client:
                client_id = client_map[selected_client]
                activities = db.fetchall(
                    """SELECT activity_type, direction, subject, content, status, follow_up_date, created_at
                       FROM activities WHERE client_id = ? ORDER BY created_at DESC LIMIT 10""",
                    (client_id,)
                )
                if activities:
                    df = pd.DataFrame(activities, columns=["类型", "方向", "主题", "内容", "状态", "跟进日期", "日期"])
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("暂无跟进记录")
                
                # 新建跟进
                st.markdown("**新增跟进**")
                with st.form("new_activity"):
                    act_type = st.selectbox("活动类型", ["email", "whatsapp", "phone", "meeting"])
                    direction = st.selectbox("方向", ["outbound", "inbound"])
                    subject = st.text_input("主题")
                    content = st.text_area("内容")
                    follow_up = st.date_input("下次跟进日期")
                    
                    if st.form_submit_button("📝 记录跟进"):
                        from src.m8_crm import ActivityTracker
                        tracker = ActivityTracker(db)
                        aid = tracker.log(
                            client_id=client_id,
                            activity_type=act_type,
                            direction=direction,
                            subject=subject,
                            content=content,
                            follow_up_date=follow_up.isoformat(),
                        )
                        st.success(f"✅ 跟进记录已保存！ID: {aid}")
    
    with tab4:
        st.subheader("跟进提醒")
        from src.m8_crm import FollowUpReminder
        reminder = FollowUpReminder(db)
        summary = reminder.reminder_summary()
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("逾期跟进", summary["overdue_count"], delta=None)
        with c2:
            st.metric("3天内待跟进", len(summary["upcoming_3_days"]))
        with c3:
            st.metric("30天无活动", summary["stale_clients_count"])
        
        if summary["overdue_clients"]:
            st.warning("⚠️ 逾期未跟进客户")
            st.dataframe(pd.DataFrame(summary["overdue_clients"]), use_container_width=True, hide_index=True)
        
        if summary["upcoming_3_days"]:
            st.info("📅 近3天待跟进")
            st.dataframe(pd.DataFrame(summary["upcoming_3_days"]), use_container_width=True, hide_index=True)


# ============================================================
# Page 5: 客户分析 (M5)
# ============================================================
elif page == "⭐ 客户分析":
    st.title("⭐ 客户分析 Agent")
    st.caption("AI评级 + 跟进策略")
    
    tab1, tab2 = st.tabs(["客户评级", "批量分析"])
    
    with tab1:
        clients_list = get_client_list()
        if clients_list:
            client_map = {f"{c['company_name']} ({c['country']}) [{c['grade'] or 'N/A'}]": c['id'] for c in clients_list}
            selected = st.selectbox("选择客户", list(client_map.keys()))
            
            if st.button("🔍 生成评级分析", use_container_width=True):
                cid = client_map[selected]
                with st.spinner("正在分析客户..."):
                    try:
                        from src.m5_client_analysis import ClientGrader, ClientAdvisor
                        
                        grader = ClientGrader(db)
                        grade_result = grader.grade_client(cid)
                        
                        advisor = ClientAdvisor(db)
                        strategy = advisor.get_advice(cid)
                        
                        st.success("✅ 分析完成")
                        
                        st.json(grade_result)
                        
                        st.divider()
                        st.subheader("📋 跟进策略")
                        st.json(strategy)
                        
                    except Exception as e:
                        st.error(f"错误: {e}")
        else:
            st.info("暂无客户数据，请先在CRM中添加客户")
    
    with tab2:
        st.subheader("批量评级")
        if st.button("🔄 批量评级所有客户"):
            with st.spinner("正在批量评级..."):
                try:
                    from src.m5_client_analysis import ClientGrader
                    grader = ClientGrader(db)
                    results = grader.batch_grade()
                    st.success(f"✅ 已完成 {len(results)} 个客户评级")
                    if results:
                        st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
                except Exception as e:
                    st.error(f"错误: {e}")


# ============================================================
# Page 6: 开发信 (M6)
# ============================================================
elif page == "📧 开发信":
    st.title("📧 AI开发信 Agent")
    st.caption("根据客户画像生成个性化开发信")
    
    tab1, tab2, tab3 = st.tabs(["邮件", "WhatsApp", "LinkedIn"])
    
    with tab1:
        st.subheader("邮件开发信")
        clients_list = get_client_list()
        if clients_list:
            client_map = {f"{c['company_name']} ({c['country']})": c['id'] for c in clients_list}
            selected = st.selectbox("选择客户", list(client_map.keys()))
            
            col1, col2 = st.columns(2)
            with col1:
                msg_type = st.selectbox("邮件类型", ["cold_intro", "follow_up", "re_engage", "promotion"])
            with col2:
                custom = st.text_input("自定义指令")
            
            if st.button("✉️ 生成邮件", use_container_width=True):
                cid = client_map[selected]
                with st.spinner("正在生成邮件..."):
                    try:
                        from src.m6_outreach import EmailGenerator
                        gen = EmailGenerator(db)
                        result = gen.generate(cid, message_type=msg_type, custom_instructions=custom)
                        
                        st.success("✅ 邮件生成成功")
                        
                        st.markdown(f"**主题:** {result.get('subject', '')}")
                        st.text_area("邮件正文", result.get('body', ''), height=300)
                        st.info(f"P.S. {result.get('ps_line', '')}")
                    except Exception as e:
                        st.error(f"错误: {e}")
    
    with tab2:
        st.subheader("WhatsApp消息")
        clients_list = get_client_list()
        if clients_list:
            client_map = {f"{c['company_name']} ({c['country']})": c['id'] for c in clients_list}
            selected = st.selectbox("选择客户", list(client_map.keys()), key="wa_client")
            
            msg_type = st.selectbox("消息类型", ["cold_intro", "follow_up", "catalog_share"], key="wa_type")
            
            if st.button("📱 生成WhatsApp消息", use_container_width=True):
                cid = client_map[selected]
                with st.spinner("正在生成消息..."):
                    try:
                        from src.m6_outreach import WhatsAppGenerator
                        gen = WhatsAppGenerator(db)
                        result = gen.generate(cid, message_type=msg_type)
                        
                        st.success("✅ 消息生成成功")
                        st.text_area("消息内容", result.get('message', ''), height=150)
                    except Exception as e:
                        st.error(f"错误: {e}")
    
    with tab3:
        st.subheader("LinkedIn消息")
        clients_list = get_client_list()
        if clients_list:
            client_map = {f"{c['company_name']} ({c['country']})": c['id'] for c in clients_list}
            selected = st.selectbox("选择客户", list(client_map.keys()), key="li_client")
            
            if st.button("🔗 生成LinkedIn消息", use_container_width=True):
                cid = client_map[selected]
                with st.spinner("正在生成消息..."):
                    try:
                        from src.m6_outreach import LinkedInGenerator
                        gen = LinkedInGenerator(db)
                        result = gen.generate(cid)
                        
                        st.success("✅ 消息生成成功")
                        st.markdown("**连接请求:**")
                        st.info(result.get('connection_request', ''))
                        st.markdown("**后续消息:**")
                        st.text_area("Follow-up", result.get('follow_up_message', ''), height=200)
                    except Exception as e:
                        st.error(f"错误: {e}")


# ============================================================
# Page 7: 报价助手 (M7)
# ============================================================
elif page == "💰 报价助手":
    st.title("💰 报价助手")
    st.caption("价格计算 + 装柜量 + 报价邮件生成")
    
    tab1, tab2, tab3 = st.tabs(["单品报价", "批量报价", "报价记录"])
    
    with tab1:
        st.subheader("单品报价")
        
        product_list = get_product_list()
        if product_list:
            product_map = {f"{p['product_code']} - {p['product_name_en']}": p['product_code'] for p in product_list}
            selected = st.selectbox("选择产品", list(product_map.keys()))
            
            c1, c2, c3 = st.columns(3)
            with c1:
                quantity = st.number_input("数量", value=1000, min_value=1)
            with c2:
                incoterm = st.selectbox("贸易术语", ["FOB", "CIF", "EXW"])
            with c3:
                margin = st.slider("利润率 %", 0, 50, 15)
            
            if st.button("🧮 计算报价", use_container_width=True):
                from src.m7_quotation import PriceCalculator
                calc = PriceCalculator(db)
                result = calc.calculate_price(
                    product_code=product_map[selected],
                    quantity=quantity,
                    incoterm=incoterm,
                    margin_pct=margin,
                )
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success("✅ 报价计算完成")
                    
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.metric("单价", f"${result['unit_price_usd']:.2f}")
                    with c2:
                        st.metric("总价", f"${result['total_usd']:,.2f}")
                    with c3:
                        st.metric("总重量", f"{result['total_weight_kg']:,.1f} kg")
                    with c4:
                        st.metric("总体积", f"{result['total_cbm']:.3f} CBM")
                    
                    st.divider()
                    st.markdown("**装柜量:**")
                    loading = result.get("loading", {})
                    for ct, info in loading.items():
                        if isinstance(info, dict):
                            st.write(f"- {ct}: 每柜 {info.get('per_container', 0)} 件, 需 {info.get('containers_needed', 0)} 个柜")
    
    with tab2:
        st.subheader("批量报价")
        st.info("在下方逐行添加产品，然后一键计算")
        
        product_list = get_product_list()
        if product_list:
            product_map = {f"{p['product_code']} - {p['product_name_en']}": p['product_code'] for p in product_list}
            
            if "batch_items" not in st.session_state:
                st.session_state.batch_items = []
            
            with st.form("add_item"):
                item_product = st.selectbox("产品", list(product_map.keys()), key="batch_prod")
                item_qty = st.number_input("数量", value=1000, min_value=1, key="batch_qty")
                
                if st.form_submit_button("➕ 添加"):
                    st.session_state.batch_items.append({
                        "product_code": product_map[item_product],
                        "quantity": item_qty,
                    })
                    st.rerun()
            
            if st.session_state.batch_items:
                st.dataframe(pd.DataFrame(st.session_state.batch_items), use_container_width=True, hide_index=True)
                
                if st.button("🧮 计算批量报价", use_container_width=True):
                    from src.m7_quotation import PriceCalculator
                    calc = PriceCalculator(db)
                    result = calc.batch_quote(st.session_state.batch_items)
                    
                    st.metric("批量报价总额", f"${result['total_usd']:,.2f}")
                    st.dataframe(pd.DataFrame(result["items"]), use_container_width=True, hide_index=True)
                
                if st.button("🗑️ 清空列表"):
                    st.session_state.batch_items = []
                    st.rerun()
    
    with tab3:
        st.subheader("报价记录")
        quotations = db.fetchall(
            """SELECT q.quotation_no, c.company_name, c.country, q.total_amount, q.status, q.created_at
               FROM quotations q LEFT JOIN clients c ON q.client_id = c.id
               ORDER BY q.created_at DESC LIMIT 20"""
        )
        if quotations:
            df = pd.DataFrame(quotations, columns=["报价号", "客户", "国家", "金额", "状态", "日期"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("暂无报价记录")


# ============================================================
# Page 8: 数据分析 (M9)
# ============================================================
elif page == "📈 数据分析":
    st.title("📈 数据分析")
    
    from src.m9_analytics import DashboardData, ProductAnalytics, ClientAnalytics, MarketAnalytics
    
    tab1, tab2, tab3, tab4 = st.tabs(["产品分析", "客户分析", "市场分析", "销售漏斗"])
    
    with tab1:
        pa = ProductAnalytics(db)
        
        overview = pa.overview()
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("总产品数", overview["total_products"])
        with c2:
            st.metric("平均长度", f"{overview['avg_length_cm']} cm")
        with c3:
            st.metric("分类数", len(overview["categories"]))
        
        st.subheader("分类分布")
        cat_data = pa.category_distribution()
        if cat_data:
            st.dataframe(pd.DataFrame(cat_data), use_container_width=True, hide_index=True)
        
        st.subheader("长度区间分布")
        length_dist = pa.length_distribution()
        if length_dist:
            st.bar_chart(pd.DataFrame(length_dist).set_index("range")["count"])
        
        st.subheader("材质分布")
        mat_data = pa.material_distribution()
        if mat_data:
            st.dataframe(pd.DataFrame(mat_data), use_container_width=True, hide_index=True)
        
        st.subheader("SEO覆盖率")
        seo = pa.seo_coverage()
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("SEO标题", f"{seo['with_seo_titles']}/{seo['total']}")
        with c2:
            st.metric("卖点文案", f"{seo['with_selling_points']}/{seo['total']}")
        with c3:
            st.metric("WhatsApp文案", f"{seo['with_whatsapp_script']}/{seo['total']}")
        with c4:
            st.metric("SEO覆盖率", f"{seo['seo_pct']}%")
    
    with tab2:
        ca = ClientAnalytics(db)
        
        overview = ca.overview()
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("总客户数", overview["total_clients"])
        with c2:
            st.metric("平均评分", overview["avg_score"])
        
        st.subheader("国家分布")
        countries = ca.country_distribution()
        if countries:
            st.dataframe(pd.DataFrame(countries), use_container_width=True, hide_index=True)
        
        st.subheader("评分分布")
        score_dist = ca.score_distribution()
        if score_dist:
            st.bar_chart(pd.DataFrame(score_dist).set_index("range")["count"])
    
    with tab3:
        ma = MarketAnalytics(db)
        
        overview = ma.overview()
        st.metric("市场报告总数", overview["total_reports"])
        
        if overview["by_country"]:
            st.subheader("国家报告分布")
            st.dataframe(pd.DataFrame(overview["by_country"]), use_container_width=True, hide_index=True)
        
        st.subheader("竞争格局")
        competitive = ma.competitive_landscape()
        if competitive:
            st.dataframe(pd.DataFrame(competitive), use_container_width=True, hide_index=True)
    
    with tab4:
        st.subheader("销售漏斗")
        dashboard = DashboardData(db)
        pipeline = dashboard.pipeline_summary()
        
        if pipeline["funnel"]:
            funnel_df = pd.DataFrame(pipeline["funnel"])
            st.dataframe(funnel_df, use_container_width=True, hide_index=True)
        
        if pipeline["quotations"]:
            st.subheader("报价统计")
            q = pipeline["quotations"]
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("总报价", q.get("total", 0))
            with c2:
                st.metric("已接受", q.get("accepted", 0))
            with c3:
                st.metric("已拒绝", q.get("rejected", 0))
