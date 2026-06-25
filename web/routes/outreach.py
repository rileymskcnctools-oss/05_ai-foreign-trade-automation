"""开发信路由 — 复用 src/m6_outreach/"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os

from web.deps import get_db

router = APIRouter(prefix="/outreach")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"))


@router.get("", response_class=HTMLResponse)
async def outreach_page(request: Request):
    """开发信页面"""
    db = get_db()
    clients = db.fetchall("SELECT id, company_name, country FROM clients ORDER BY company_name")
    return templates.TemplateResponse(request, "outreach.html", {
        "request": request, "page": "outreach", "clients": clients,
    })


@router.post("/api/generate-email")
async def api_generate_email(request: Request):
    """API: 生成邮件开发信"""
    db = get_db()
    from src.m6_outreach.email_generator import EmailGenerator
    data = await request.json()
    gen = EmailGenerator(db)
    result = gen.generate(
        client_id=data["client_id"],
        message_type=data.get("message_type", "cold_intro"),
        custom_instructions=data.get("custom_instructions", ""),
    )
    return result


@router.post("/api/generate-whatsapp")
async def api_generate_whatsapp(request: Request):
    """API: 生成WhatsApp消息"""
    db = get_db()
    from src.m6_outreach.whatsapp_generator import WhatsAppGenerator
    data = await request.json()
    gen = WhatsAppGenerator(db)
    result = gen.generate(client_id=data["client_id"], message_type=data.get("message_type", "cold_intro"))
    return result


@router.post("/api/generate-linkedin")
async def api_generate_linkedin(request: Request):
    """API: 生成LinkedIn消息"""
    db = get_db()
    from src.m6_outreach.linkedin_generator import LinkedInGenerator
    data = await request.json()
    gen = LinkedInGenerator(db)
    result = gen.generate(client_id=data["client_id"])
    return result
