"""
客户CRM路由 — 复用 src/m8_crm/
"""
from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os

from web.deps import get_db

router = APIRouter(prefix="/clients")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"))


@router.get("", response_class=HTMLResponse)
async def clients_page(
    request: Request,
    status: str = Query("", description="状态筛选"),
    grade: str = Query("", description="评级筛选"),
    country: str = Query("", description="国家筛选"),
):
    """客户列表页面"""
    db = get_db()
    from src.m8_crm.client_manager import ClientManager
    mgr = ClientManager(db)
    clients = mgr.list_all(
        status=status if status else None,
        grade=grade if grade else None,
        country=country if country else None,
        limit=50,
    )
    pipeline = mgr.pipeline_stats()
    return templates.TemplateResponse(request, "clients.html", {
        "request": request, "page": "clients", "clients": clients,
        "pipeline": pipeline, "filters": {"status": status, "grade": grade, "country": country},
    })


@router.post("/api/create")
async def api_create_client(request: Request):
    """API: 创建新客户"""
    db = get_db()
    from src.m8_crm.client_manager import ClientManager
    data = await request.json()
    mgr = ClientManager(db)
    client_id = mgr.create(data)
    return {"success": True, "client_id": client_id}


@router.get("/api/{client_id}")
async def api_get_client(client_id: int):
    """API: 获取客户详情"""
    db = get_db()
    from src.m8_crm.client_manager import ClientManager
    mgr = ClientManager(db)
    client = mgr.get(client_id)
    if not client:
        return JSONResponse(status_code=404, content={"error": "Client not found"})
    return client


@router.put("/api/{client_id}")
async def api_update_client(client_id: int, request: Request):
    """API: 更新客户信息"""
    db = get_db()
    data = await request.json()
    data.pop("id", None)
    if not data:
        return JSONResponse(status_code=400, content={"error": "No fields to update"})
    set_clause = ", ".join(f"{k}=?" for k in data.keys())
    sql = f"UPDATE clients SET {set_clause}, updated_at=datetime('now') WHERE id=?"
    params = list(data.values()) + [client_id]
    try:
        cursor = db.execute(sql, tuple(params))
        db.commit()
        if cursor.rowcount == 0:
            return JSONResponse(status_code=404, content={"error": "Client not found"})
        return {"success": True, "updated_fields": list(data.keys())}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.delete("/api/{client_id}")
async def api_delete_client(client_id: int):
    """API: 删除客户"""
    db = get_db()
    try:
        # 先删关联的跟进记录
        db.execute("DELETE FROM activities WHERE client_id=?", (client_id,))
        cursor = db.execute("DELETE FROM clients WHERE id=?", (client_id,))
        db.commit()
        if cursor.rowcount == 0:
            return JSONResponse(status_code=404, content={"error": "Client not found"})
        return {"success": True, "deleted_id": client_id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@router.get("/api/{client_id}/activities")
async def api_client_activities(client_id: int, limit: int = Query(20)):
    """API: 获取客户跟进记录"""
    db = get_db()
    from src.m8_crm.activity_tracker import ActivityTracker
    tracker = ActivityTracker(db)
    activities = tracker.timeline(client_id, limit=limit)
    return {"activities": activities}


@router.post("/api/{client_id}/activities")
async def api_log_activity(client_id: int, request: Request):
    """API: 新增跟进记录"""
    db = get_db()
    from src.m8_crm.activity_tracker import ActivityTracker
    data = await request.json()
    tracker = ActivityTracker(db)
    activity_id = tracker.log(
        client_id=client_id,
        activity_type=data.get("activity_type", "email"),
        direction=data.get("direction", "outbound"),
        subject=data.get("subject", ""),
        content=data.get("content", ""),
        follow_up_date=data.get("follow_up_date"),
    )
    return {"success": True, "activity_id": activity_id}


@router.get("/api/reminders/summary")
async def api_reminder_summary():
    """API: 跟进提醒汇总"""
    db = get_db()
    from src.m8_crm.reminder import FollowUpReminder
    return FollowUpReminder(db).reminder_summary()


@router.get("/api/export/csv")
async def api_export_clients_csv():
    """API: 导出客户数据为 CSV"""
    import csv
    import io
    from fastapi.responses import StreamingResponse

    db = get_db()
    clients = db.fetchall("SELECT * FROM clients ORDER BY company_name")

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "company_name", "country", "contact_person",
                     "email", "whatsapp", "status", "grade", "source"])
    for c in clients:
        writer.writerow([
            c.get("id", ""),
            c.get("company_name", ""),
            c.get("country", ""),
            c.get("contact_person", ""),
            c.get("email", ""),
            c.get("whatsapp", ""),
            c.get("status", ""),
            c.get("grade", ""),
            c.get("source", ""),
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=clients_export.csv"},
    )


@router.post("/api/generate-potential")
async def api_generate_potential_clients(request: Request):
    """API: AI生成潜在客户画像"""
    import json as _json
    body = await request.json()
    target_market = body.get("target_market", "Africa")
    count = body.get("count", 5)

    # 加载提示词模板
    from src.utils.prompts import load_prompt, fill_prompt
    template = load_prompt("outreach/generate_potential_client")
    prompt = fill_prompt(template, {
        "target_market": target_market,
        "count": str(count),
    })

    # 调用AI生成
    try:
        from src.core.llm_client import LLMClient
        llm = LLMClient(scenario="outreach")
        result_text = llm.chat(prompt, temperature=0.8, max_tokens=4000)

        # 尝试解析JSON
        # 先找到JSON块
        if "```json" in result_text:
            json_str = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            json_str = result_text.split("```")[1].split("```")[0].strip()
        else:
            json_str = result_text.strip()

        result = _json.loads(json_str)
        clients = result.get("clients", [])
        return {"success": True, "clients": clients, "count": len(clients)}
    except _json.JSONDecodeError as e:
        return {"success": False, "error": f"AI返回格式错误: {str(e)}", "raw": result_text[:500]}
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@router.post("/api/batch-insert")
async def api_batch_insert_clients(request: Request):
    """API: 批量插入AI生成的潜在客户"""
    body = await request.json()
    clients = body.get("clients", [])
    if not clients:
        return JSONResponse(status_code=400, content={"error": "No clients provided"})

    db = get_db()
    inserted = []
    errors = []
    for c in clients:
        try:
            cid = db.client_create(c)
            inserted.append({"id": cid, "company_name": c.get("company_name", "")})
        except Exception as e:
            errors.append({"company_name": c.get("company_name", ""), "error": str(e)})
    return {"success": True, "inserted": len(inserted), "errors": errors, "details": inserted}
