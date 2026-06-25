"""
数据概览路由 — 复用 src/m9_analytics/dashboard_data.py
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

from web.deps import get_db

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"))


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """数据概览页面"""
    db = get_db()
    from src.m9_analytics.dashboard_data import DashboardData
    dashboard = DashboardData(db)
    stats = dashboard.quick_stats()
    home = dashboard.home_data()
    return templates.TemplateResponse(request, "dashboard.html", {
        "request": request, "page": "dashboard", "stats": stats, "home": home,
    })


@router.get("/api/dashboard/stats")
async def dashboard_stats():
    """API: 快速统计数据 (JSON)"""
    db = get_db()
    from src.m9_analytics.dashboard_data import DashboardData
    return DashboardData(db).quick_stats()


@router.get("/api/dashboard/home")
async def dashboard_home():
    """API: 首页仪表盘数据 (JSON)"""
    db = get_db()
    from src.m9_analytics.dashboard_data import DashboardData
    return DashboardData(db).home_data()
