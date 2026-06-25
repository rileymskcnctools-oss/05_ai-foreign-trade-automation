"""
FT Workspace v3.0 — FastAPI 应用入口
启动: uvicorn web.main:app --reload --port 8000
"""
import os
import sys

# 项目路径守护伞
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

from web.deps import get_db


# ============================================================
# 应用生命周期
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动/关闭时的钩子"""
    db = get_db()
    print(f"✅ 数据库已连接: {db.db_path}")
    print(f"📦 产品数量: {db.product_count()}")
    yield
    db.close()
    print("🔒 数据库连接已关闭")


# ============================================================
# FastAPI 应用
# ============================================================
app = FastAPI(
    title="FT Workspace",
    description="Foreign Trade AI Workspace v3.0",
    version="3.0.0",
    lifespan=lifespan,
)

# 静态文件
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Jinja2 模板
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)


# ============================================================
# 路由注册
# ============================================================
from web.routes.dashboard import router as dashboard_router
from web.routes.products import router as products_router
from web.routes.clients import router as clients_router
from web.routes.market import router as market_router
from web.routes.outreach import router as outreach_router
from web.routes.quotation import router as quotation_router
from web.routes.analytics import router as analytics_router

app.include_router(dashboard_router)
app.include_router(products_router)
app.include_router(clients_router)
app.include_router(market_router)
app.include_router(outreach_router)
app.include_router(quotation_router)
app.include_router(analytics_router)


@app.get("/")
async def root():
    """首页重定向到数据概览"""
    return RedirectResponse(url="/dashboard")
