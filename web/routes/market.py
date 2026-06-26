"""市场研究路由 — 复用 src/m4_market_research/"""
from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os

from web.deps import get_db

router = APIRouter(prefix="/market")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"))


@router.get("", response_class=HTMLResponse)
async def market_page(request: Request):
    """市场研究页面"""
    db = get_db()
    from src.m4_market_research.report_generator import MarketResearchAgent
    agent = MarketResearchAgent(db)
    reports = agent.list_reports(limit=20)
    knowledge = agent.get_knowledge(limit=30)
    return templates.TemplateResponse(request, "market.html", {
        "request": request, "page": "market", "reports": reports, "knowledge": knowledge,
    })


@router.post("/api/generate-report")
async def api_generate_report(request: Request):
    """API: 生成市场研究报告"""
    db = get_db()
    from src.m4_market_research.report_generator import MarketResearchAgent
    data = await request.json()
    agent = MarketResearchAgent(db)
    result = agent.generate_report(country=data["country"], extra_context=data.get("extra_context", ""))
    return result


@router.get("/api/reports/{report_id}")
async def api_get_report(report_id: int):
    """API: 获取报告详情"""
    db = get_db()
    from src.m4_market_research.report_generator import MarketResearchAgent
    agent = MarketResearchAgent(db)
    report = agent.get_report(report_id)
    if not report:
        return JSONResponse(status_code=404, content={"error": "Report not found"})
    return report


@router.delete("/api/reports/{report_id}")
async def api_delete_report(report_id: int):
    """API: 删除报告"""
    db = get_db()
    if db.report_delete(report_id):
        return {"success": True, "deleted_id": report_id}
    return JSONResponse(status_code=404, content={"error": "Report not found"})
