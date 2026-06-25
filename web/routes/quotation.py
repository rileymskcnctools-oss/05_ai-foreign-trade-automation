"""报价路由 — 复用 src/m7_quotation/"""
from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os

from web.deps import get_db

router = APIRouter(prefix="/quotation")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"))


@router.get("", response_class=HTMLResponse)
async def quotation_page(request: Request):
    """报价页面"""
    db = get_db()
    products = db.product_list(limit=200)
    quotations = db.fetchall(
        """SELECT q.quotation_no, c.company_name, c.country, q.total_amount, q.status, q.created_at
           FROM quotations q LEFT JOIN clients c ON q.client_id = c.id
           ORDER BY q.created_at DESC LIMIT 20"""
    )
    return templates.TemplateResponse(request, "quotation.html", {
        "request": request, "page": "quotation", "products": products, "quotations": quotations,
    })


@router.post("/api/calculate")
async def api_calculate(request: Request):
    """API: 计算报价"""
    db = get_db()
    from src.m7_quotation.calculator import PriceCalculator
    data = await request.json()
    calc = PriceCalculator(db)
    result = calc.calculate_price(
        product_code=data["product_code"],
        quantity=data.get("quantity", 1000),
        incoterm=data.get("incoterm", "FOB"),
        margin_pct=data.get("margin_pct", 15),
    )
    return result


@router.post("/api/batch-quote")
async def api_batch_quote(request: Request):
    """API: 批量报价"""
    db = get_db()
    from src.m7_quotation.calculator import PriceCalculator
    data = await request.json()
    calc = PriceCalculator(db)
    result = calc.batch_quote(data["items"])
    return result
