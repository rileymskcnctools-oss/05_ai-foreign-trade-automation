"""
产品管理路由 — 复用 src/m1_product_db/
"""
from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os

from web.deps import get_db

router = APIRouter(prefix="/products")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"))


@router.get("", response_class=HTMLResponse)
async def products_page(
    request: Request,
    q: str = Query("", description="搜索关键词"),
    category: str = Query("", description="分类筛选"),
    page: int = Query(1, ge=1),
):
    """产品管理页面"""
    db = get_db()
    from src.m1_product_db.search import get_categories, search, filter_products
    
    categories = get_categories(db)
    if q:
        products = search(q, db=db, limit=50)
    elif category:
        products = filter_products(category=category, db=db, limit=50)
    else:
        products = db.product_list(limit=50, offset=(page - 1) * 50)
    
    return templates.TemplateResponse(request, "products.html", {
        "request": request, "page": "products", "products": products,
        "categories": categories, "query": q, "selected_category": category, "current_page": page,
    })


@router.get("/partials/table", response_class=HTMLResponse)
async def products_table_partial(
    request: Request,
    q: str = Query("", description="搜索关键词"),
    category: str = Query("", description="分类筛选"),
    page: int = Query(1, ge=1),
):
    """HTMX: 返回产品表格局部 HTML (不包含 base.html)"""
    db = get_db()
    from src.m1_product_db.search import get_categories, search, filter_products

    categories = get_categories(db)
    if q:
        products = search(q, db=db, limit=50)
    elif category:
        products = filter_products(category=category, db=db, limit=50)
    else:
        products = db.product_list(limit=50, offset=(page - 1) * 50)

    return templates.TemplateResponse(request, "components/product_table.html", {
        "request": request, "products": products, "categories": categories,
    })


@router.get("/api/search")
async def api_search(q: str = Query(""), limit: int = Query(20)):
    """API: 产品搜索 (JSON)"""
    db = get_db()
    from src.m1_product_db.search import search
    results = search(q, db=db, limit=limit) if q else db.product_list(limit=limit)
    return {"results": results, "count": len(results)}


@router.get("/api/{product_code}")
async def api_get_product(product_code: str):
    """API: 获取单个产品详情 (JSON)"""
    db = get_db()
    product = db.product_get(product_code)
    if not product:
        return JSONResponse(status_code=404, content={"error": "Product not found"})
    return product


@router.get("/api/categories")
async def api_categories():
    """API: 获取所有分类 (JSON)"""
    db = get_db()
    from src.m1_product_db.search import get_categories
    return get_categories(db)


@router.get("/api/{product_code}/generate/{content_type}")
async def api_generate_content(product_code: str, content_type: str):
    """API: 生成产品内容 (SEO/selling_points/whatsapp/alibaba)"""
    db = get_db()
    from src.m3_seo.content_generator import (
        generate_seo_titles, generate_selling_points,
        generate_whatsapp_script, generate_alibaba_detail,
    )
    generators = {
        "seo": lambda: generate_seo_titles(product_code, count=3, save=True, db=db),
        "selling_points": lambda: generate_selling_points(product_code, save=True, db=db),
        "whatsapp": lambda: generate_whatsapp_script(product_code, save=True, db=db),
        "alibaba": lambda: generate_alibaba_detail(product_code, save=True, db=db),
    }
    if content_type not in generators:
        return JSONResponse(status_code=400, content={"error": f"Unknown type: {content_type}"})
    try:
        result = generators[content_type]()
        return {"success": True, "result": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
