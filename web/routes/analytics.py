"""数据分析路由 — 复用 src/m9_analytics/"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

from web.deps import get_db

router = APIRouter(prefix="/analytics")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"))


@router.get("", response_class=HTMLResponse)
async def analytics_page(request: Request):
    """数据分析页面"""
    db = get_db()
    from src.m9_analytics.product_analytics import ProductAnalytics
    from src.m9_analytics.client_analytics import ClientAnalytics
    from src.m9_analytics.market_analytics import MarketAnalytics
    from src.m9_analytics.dashboard_data import DashboardData

    pa = ProductAnalytics(db)
    ca = ClientAnalytics(db)
    ma = MarketAnalytics(db)
    dashboard = DashboardData(db)

    return templates.TemplateResponse(request, "analytics.html", {
        "request": request, "page": "analytics",
        "product_overview": pa.overview(),
        "category_dist": pa.category_distribution(),
        "color_dist": pa.color_distribution(),
        "seo_coverage": pa.seo_coverage(),
        "client_overview": ca.overview(),
        "country_dist": ca.country_distribution(),
        "score_dist": ca.score_distribution(),
        "market_overview": ma.overview(),
        "pipeline": dashboard.pipeline_summary(),
    })


@router.get("/api/products")
async def api_product_analytics():
    """API: 产品分析数据"""
    db = get_db()
    from src.m9_analytics.product_analytics import ProductAnalytics
    pa = ProductAnalytics(db)
    return {"overview": pa.overview(), "categories": pa.category_distribution(),
            "materials": pa.material_distribution(), "seo": pa.seo_coverage()}


@router.get("/api/clients")
async def api_client_analytics():
    """API: 客户分析数据"""
    db = get_db()
    from src.m9_analytics.client_analytics import ClientAnalytics
    ca = ClientAnalytics(db)
    return {"overview": ca.overview(), "countries": ca.country_distribution(),
            "scores": ca.score_distribution(), "funnel": ca.status_funnel()}
