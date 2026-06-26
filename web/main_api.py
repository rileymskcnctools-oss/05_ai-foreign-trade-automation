"""
FT Workspace v4.0 — 纯 API 服务器 (供 Vue 前端调用)
与 web/main.py (HTMX版) 并存，互不影响
"""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# 加载 .env 环境变量（代理、API Key 等）
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(PROJECT_ROOT, "config", ".env"))
except ImportError:
    pass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from web.deps import get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_db()
    print(f"✅ API Server — DB: {db.db_path}, Products: {db.product_count()}")
    yield
    db.close()


app = FastAPI(
    title="FT Workspace API",
    description="Foreign Trade AI Workspace v4.0 — Pure API",
    version="4.0.0",
    lifespan=lifespan,
)

# CORS (允许 Vue 开发服务器跨域)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 注册所有 API 路由 (从现有 routes 导入)
# ============================================================

# Dashboard API
from web.routes.dashboard import (
    dashboard_stats, dashboard_home,
    partial_recent_quotations, partial_reminders,
)
app.add_api_route("/api/dashboard/stats", dashboard_stats, methods=["GET"])
app.add_api_route("/api/dashboard/home", dashboard_home, methods=["GET"])
app.add_api_route("/dashboard/api/dashboard/stats", dashboard_stats, methods=["GET"])
app.add_api_route("/dashboard/api/dashboard/home", dashboard_home, methods=["GET"])

# Products API — 注册所有固定路径 + 通配符
from web.routes.products import (
    api_search, api_categories, api_export_csv,
    api_get_product, api_update_product, api_create_product, api_delete_product,
    api_generate_content,
)
app.add_api_route("/products/api/search", api_search, methods=["GET"])
app.add_api_route("/products/api/categories", api_categories, methods=["GET"])
app.add_api_route("/products/api/export/csv", api_export_csv, methods=["GET"])
app.add_api_route("/products/api/create", api_create_product, methods=["POST"])
app.add_api_route("/products/api/{product_code}", api_get_product, methods=["GET"])
app.add_api_route("/products/api/{product_code}", api_update_product, methods=["PUT"])
app.add_api_route("/products/api/{product_code}", api_delete_product, methods=["DELETE"])
app.add_api_route("/products/api/{product_code}/generate/{content_type}", api_generate_content, methods=["GET"])

# Clients API
from web.routes.clients import (
    api_create_client, api_get_client, api_update_client, api_delete_client,
    api_client_activities, api_log_activity,
    api_reminder_summary, api_export_clients_csv,
    api_get_client_analyses, api_run_client_analysis,
    api_generate_potential_clients, api_search_real_clients, api_batch_insert_clients,
)
# Client list helper
async def _client_list(status: str = "", grade: str = "", country: str = ""):
    from src.m8_crm.client_manager import ClientManager
    db = get_db()
    mgr = ClientManager(db)
    clients = mgr.list_all(
        status=status if status else None,
        grade=grade if grade else None,
        country=country if country else None,
        limit=50,
    )
    return {"clients": clients}
app.add_api_route("/clients/api/list", _client_list, methods=["GET"])
app.add_api_route("/clients/api/create", api_create_client, methods=["POST"])
app.add_api_route("/clients/api/reminders/summary", api_reminder_summary, methods=["GET"])
app.add_api_route("/clients/api/export/csv", api_export_clients_csv, methods=["GET"])
app.add_api_route("/clients/api/generate-potential", api_generate_potential_clients, methods=["POST"])
app.add_api_route("/clients/api/search-real-clients", api_search_real_clients, methods=["POST"])
app.add_api_route("/clients/api/batch-insert", api_batch_insert_clients, methods=["POST"])
app.add_api_route("/clients/api/{client_id}", api_get_client, methods=["GET"])
app.add_api_route("/clients/api/{client_id}", api_update_client, methods=["PUT"])
app.add_api_route("/clients/api/{client_id}", api_delete_client, methods=["DELETE"])
app.add_api_route("/clients/api/{client_id}/activities", api_client_activities, methods=["GET"])
app.add_api_route("/clients/api/{client_id}/activities", api_log_activity, methods=["POST"])
app.add_api_route("/clients/api/{client_id}/analyses", api_get_client_analyses, methods=["GET"])
app.add_api_route("/clients/api/{client_id}/analyze", api_run_client_analysis, methods=["POST"])

# Market API
from web.routes.market import (
    api_generate_report, api_get_report, api_delete_report,
)
app.add_api_route("/market/api/generate-report", api_generate_report, methods=["POST"])
app.add_api_route("/market/api/reports/{report_id}", api_get_report, methods=["GET"])
app.add_api_route("/market/api/reports/{report_id}", api_delete_report, methods=["DELETE"])

# Outreach API
from web.routes.outreach import (
    api_generate_email, api_generate_whatsapp, api_generate_linkedin,
)
app.add_api_route("/outreach/api/generate-email", api_generate_email, methods=["POST"])
app.add_api_route("/outreach/api/generate-whatsapp", api_generate_whatsapp, methods=["POST"])
app.add_api_route("/outreach/api/generate-linkedin", api_generate_linkedin, methods=["POST"])

# Quotation API (new router-based)
from web.routes.quotation import router as quotation_router
app.include_router(quotation_router)

# Reports list helper
async def _report_list():
    db = get_db()
    from src.m4_market_research.report_generator import MarketResearchAgent
    agent = MarketResearchAgent(db)
    reports = agent.list_reports(limit=20)
    return {"reports": reports}
app.add_api_route("/market/api/reports", _report_list, methods=["GET"])

# Sub-category distribution
async def _sub_category_dist():
    db = get_db()
    rows = db.fetchall("SELECT sub_category, COUNT(*) as cnt FROM products WHERE status='active' GROUP BY sub_category ORDER BY cnt DESC")
    return {"sub_categories": [{"name": r["sub_category"], "count": r["cnt"]} for r in rows]}
app.add_api_route("/api/dashboard/sub-categories", _sub_category_dist, methods=["GET"])
# Quotation CRUD handled by router above

# Analytics API
from web.routes.analytics import api_product_analytics, api_client_analytics
app.add_api_route("/analytics/api/products", api_product_analytics, methods=["GET"])
app.add_api_route("/analytics/api/clients", api_client_analytics, methods=["GET"])


# ============================================================
# 静态文件服务 (Vue 构建产物)
# ============================================================
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Vue 构建产物目录
FRONTEND_DIST = os.path.join(PROJECT_ROOT, "frontend", "dist")

# API 路由已在上面注册，这里挂载静态资源
if os.path.exists(FRONTEND_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="vue-assets")

    # SPA fallback: 所有非 API 路径返回 index.html
    @app.get("/{full_path:path}")
    async def spa_fallback(full_path: str):
        # 如果是 API 路径，不处理（已经被上面的路由匹配）
        # 返回 Vue 的 index.html，让 Vue Router 处理前端路由
        index_path = os.path.join(FRONTEND_DIST, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"message": "FT Workspace API v4.0", "docs": "/docs"}
else:
    @app.get("/")
    async def root():
        return {"message": "FT Workspace API v4.0", "docs": "/docs",
                "hint": "Run 'cd frontend && npm run build' to build Vue frontend"}
