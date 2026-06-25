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


@router.get("/dashboard/partials/recent-quotations", response_class=HTMLResponse)
async def partial_recent_quotations(request: Request):
    """HTMX: 最近报价局部"""
    db = get_db()
    quotations = db.fetchall(
        """SELECT q.quotation_no, c.company_name, c.country, q.total_amount, q.status, q.created_at
           FROM quotations q LEFT JOIN clients c ON q.client_id = c.id
           ORDER BY q.created_at DESC LIMIT 5"""
    )
    return templates.TemplateResponse(request, "components/recent_quotations.html", {
        "request": request, "quotations": quotations,
    })


@router.get("/dashboard/partials/reminders", response_class=HTMLResponse)
async def partial_reminders(request: Request):
    """HTMX: 跟进提醒局部"""
    db = get_db()
    try:
        from src.m8_crm.reminder import FollowUpReminder
        reminder = FollowUpReminder(db)
        summary = reminder.reminder_summary()
    except Exception:
        summary = []
    return templates.TemplateResponse(request, "components/reminders.html", {
        "request": request, "reminders": summary,
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
