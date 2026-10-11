"""数据分析路由 — 复用 src/m9_analytics/"""
from fastapi import APIRouter

from api.deps import get_db

router = APIRouter(prefix="/analytics")


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
