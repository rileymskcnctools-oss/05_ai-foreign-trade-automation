"""
数据概览路由 — 复用 src/m9_analytics/dashboard_data.py
"""
from fastapi import APIRouter

from api.deps import get_db

router = APIRouter()


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
