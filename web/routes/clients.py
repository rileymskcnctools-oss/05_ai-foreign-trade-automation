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
    from src.m8_crm.client_manager import ClientManager
    data = await request.json()
    mgr = ClientManager(db)
    success = mgr.update(client_id, data)
    return {"success": success}


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
