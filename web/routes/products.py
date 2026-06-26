"""
产品管理路由 — 复用 src/m1_product_db/
"""
from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import os
import csv
import io

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


# === 固定路径 API (必须在通配符 /api/{product_code} 之前) ===

@router.get("/api/search")
async def api_search(q: str = Query(""), limit: int = Query(20)):
    """API: 产品搜索 (JSON)"""
    db = get_db()
    from src.m1_product_db.search import search
    results = search(q, db=db, limit=limit) if q else db.product_list(limit=limit)
    return {"results": results, "count": len(results)}


@router.get("/api/categories")
async def api_categories():
    """API: 获取所有分类 (JSON)"""
    db = get_db()
    from src.m1_product_db.search import get_categories
    return get_categories(db)


@router.get("/api/export/csv")
async def api_export_csv():
    """API: 导出产品数据为 CSV"""
    db = get_db()
    products = db.product_list(limit=9999)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["product_code", "product_name_en", "product_name_cn",
                     "category", "material", "color", "weight_kg", "handle_type"])
    for p in products:
        writer.writerow([
            p.get("product_code", ""),
            p.get("product_name_en", ""),
            p.get("product_name_cn", ""),
            p.get("category", ""),
            p.get("material", ""),
            p.get("color", ""),
            p.get("weight_kg", ""),
            p.get("handle_type", ""),
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=products_export.csv"},
    )


# === 通配符 API (必须在固定路径之后) ===

@router.get("/api/{product_code}")
async def api_get_product(product_code: str):
    """API: 获取单个产品详情 (JSON)"""
    db = get_db()
    product = db.product_get(product_code)
    if not product:
        return JSONResponse(status_code=404, content={"error": "Product not found"})
    return product


@router.put("/api/{product_code}")
async def api_update_product(product_code: str, request: Request):
    """API: 更新产品信息"""
    db = get_db()
    data = await request.json()
    # 不允许修改主键
    data.pop("product_code", None)
    data.pop("id", None)
    if not data:
        return JSONResponse(status_code=400, content={"error": "No fields to update"})
    set_clause = ", ".join(f"{k}=?" for k in data.keys())
    sql = f"UPDATE products SET {set_clause}, updated_at=datetime('now') WHERE product_code=?"
    params = list(data.values()) + [product_code]
    try:
        cursor = db.execute(sql, tuple(params))
        db.commit()
        if cursor.rowcount == 0:
            return JSONResponse(status_code=404, content={"error": "Product not found"})
        return {"success": True, "updated_fields": list(data.keys())}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.post("/api/create")
async def api_create_product(request: Request):
    """API: 新增产品"""
    db = get_db()
    data = await request.json()
    if not data.get("product_code"):
        return JSONResponse(status_code=400, content={"error": "product_code is required"})
    if not data.get("product_name_en"):
        return JSONResponse(status_code=400, content={"error": "product_name_en is required"})
    if not data.get("category"):
        return JSONResponse(status_code=400, content={"error": "category is required"})
    # 检查是否已存在
    existing = db.fetchone("SELECT product_code FROM products WHERE product_code=?", (data["product_code"],))
    if existing:
        return JSONResponse(status_code=409, content={"error": f"产品编码 {data['product_code']} 已存在"})
    try:
        data.setdefault("status", "active")
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        sql = f"INSERT INTO products ({columns}) VALUES ({placeholders})"
        db.execute(sql, tuple(data.values()))
        db.commit()
        return {"success": True, "product_code": data["product_code"]}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.delete("/api/{product_code}")
async def api_delete_product(product_code: str):
    """API: 删除产品"""
    db = get_db()
    if db.product_delete(product_code):
        return {"success": True, "deleted": product_code}
    return JSONResponse(status_code=404, content={"error": "Product not found"})


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
