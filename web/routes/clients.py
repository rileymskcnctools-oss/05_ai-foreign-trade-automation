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
    """API: 删除客户（级联删除所有关联记录）"""
    db = get_db()
    try:
        # 先检查客户是否存在
        client = db.fetchone("SELECT id, company_name FROM clients WHERE id=?", (client_id,))
        if not client:
            return JSONResponse(status_code=404, content={"error": "Client not found"})
        # 级联删除所有关联表
        tables = [
            "activities", "quotations", "orders", "inquiries",
            "client_analyses", "client_tag_map"
        ]
        for table in tables:
            try:
                db.execute(f"DELETE FROM {table} WHERE client_id=?", (client_id,))
            except Exception:
                pass  # 表可能不存在或没有数据
        # 最后删除客户本身
        db.execute("DELETE FROM clients WHERE id=?", (client_id,))
        db.commit()
        return {"success": True, "deleted_id": client_id, "name": client["company_name"]}
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


@router.get("/api/{client_id}/analyses")
async def api_get_client_analyses(client_id: int):
    """API: 获取客户分析记录"""
    db = get_db()
    analyses = db.fetchall(
        "SELECT * FROM client_analyses WHERE client_id=? ORDER BY created_at DESC LIMIT 5",
        (client_id,)
    )
    return {"analyses": analyses}


@router.post("/api/{client_id}/analyze")
async def api_run_client_analysis(client_id: int):
    """API: 运行 AI 客户背调分析"""
    import json as _json
    db = get_db()
    db.conn.rollback()  # 释放可能的残留锁

    # 获取客户信息
    client = db.fetchone("SELECT * FROM clients WHERE id=?", (client_id,))
    if not client:
        return JSONResponse(status_code=404, content={"success": False, "error": "客户不存在"})

    # 构建客户信息摘要
    client_info = f"""
公司名: {client.get('company_name', '')}
国家: {client.get('country', '')}
联系人: {client.get('contact_person', '')}
邮箱: {client.get('email', '')}
WhatsApp: {client.get('whatsapp', '')}
LinkedIn: {client.get('linkedin', '')}
网站: {client.get('website', '')}
业务类型: {client.get('business_type', '')}
主营产品: {client.get('main_products', '')}
目标市场: {client.get('market_regions', '')}
预估体量: {client.get('estimated_volume', '')}
来源: {client.get('source', '')}
当前状态: {client.get('status', '')}
当前评级: {client.get('grade', '')}
备注: {client.get('notes', '')}
""".strip()

    # 获取跟进记录
    activities = db.fetchall(
        "SELECT activity_type, direction, subject, content, created_at FROM activities WHERE client_id=? ORDER BY created_at DESC LIMIT 10",
        (client_id,)
    )
    activity_summary = ""
    if activities:
        activity_summary = "\n\n跟进记录:\n"
        for a in activities:
            activity_summary += f"- [{a.get('created_at', '')}] {a.get('activity_type', '')} ({a.get('direction', '')}): {a.get('subject', '')} - {a.get('content', '')[:200]}\n"

    # 尝试网页抓取
    website_content = ""
    website = client.get('website', '')
    if website:
        try:
            import urllib.request
            import re
            url = website if website.startswith('http') else f'https://{website}'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
            resp = urllib.request.urlopen(req, timeout=10)
            html = resp.read().decode('utf-8', errors='ignore')[:8000]
            # 提取文本
            text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()[:3000]
            if text:
                website_content = f"\n\n官网内容摘录:\n{text}"
        except Exception as e:
            website_content = f"\n\n(官网抓取失败: {str(e)[:100]})"

    # 构建分析 prompt
    prompt = f"""你是一位资深的外贸客户分析师。请根据以下客户信息，进行专业的客户背调分析。

客户信息:
{client_info}
{activity_summary}
{website_content}

请从以下维度分析:

1. **公司概况**: 根据已有信息推断公司规模、业务范围、市场定位
2. **采购潜力**: 分析该客户的采购需求、体量、频率
3. **竞争分析**: 该客户可能的供应商选择标准、价格敏感度
4. **沟通策略**: 针对该客户的最佳沟通方式、注意事项
5. **风险评估**: 付款风险、合作风险
6. **建议评级**: A/B/C/D 及理由

请用中文回答，格式清晰。如果信息不足，请明确标注"信息不足，建议补充"。"""

    try:
        from src.core.llm_client import LLMClient
        llm = LLMClient()
        analysis_text = llm.chat(prompt, temperature=0.3, max_tokens=2000)

        # 提取建议评级
        grade_suggested = ""
        for g in ['A', 'B', 'C', 'D']:
            if f'建议评级.*{g}' in analysis_text or f'评级.*{g}' in analysis_text:
                grade_suggested = g
                break
        if not grade_suggested:
            for g in ['A', 'B', 'C', 'D']:
                if f'{g}级' in analysis_text or f'评级{g}' in analysis_text:
                    grade_suggested = g
                    break

        # 提取建议部分
        recommendations = ""
        if '建议' in analysis_text:
            parts = analysis_text.split('建议')
            if len(parts) > 1:
                recommendations = '建议' + parts[1][:500]

        # 保存到数据库
        db.execute(
            """INSERT INTO client_analyses (client_id, analysis_type, summary, full_analysis, grade_suggested, recommendations)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (client_id, 'background_check', analysis_text[:2000], analysis_text, grade_suggested, recommendations)
        )
        db.commit()

        return {
            "success": True,
            "analysis": {
                "summary": analysis_text,
                "grade_suggested": grade_suggested,
                "recommendations": recommendations,
                "created_at": "刚刚",
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


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

    # 获取已有客户名单用于去重
    from src.core.database import FTDatabase
    db_ro = FTDatabase()
    existing_rows = db_ro.fetchall("SELECT company_name, country FROM clients")
    db_ro.close()
    existing_list = [f"- {r['company_name']} ({r.get('country', '')})" for r in existing_rows]
    existing_str = "\n".join(existing_list) if existing_list else "(CRM is empty - no existing clients)"

    prompt = fill_prompt(template, {
        "target_market": target_market,
        "count": str(count),
        "existing_clients": existing_str,
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


@router.post("/api/search-real-clients")
async def api_search_real_clients(request: Request):
    """API: 搜索真实客户 — 先尝试网页搜索，失败则用AI知识库直接分析"""
    import json as _json
    body = await request.json()
    query = body.get("query", "").strip()
    country = body.get("country", "").strip()
    max_results = min(body.get("max_results", 8), 15)
    market = body.get("market", "default")
    mode = body.get("mode", "auto")  # auto / web_search / ai_direct

    if not query and not country:
        return JSONResponse(status_code=400, content={"error": "请提供搜索关键词或目标国家"})

    if not query:
        query = f"agricultural hand tools importer {country}"

    raw_results = []
    search_error = None

    # ── Step 1: 尝试网页搜索 ──
    if mode in ("auto", "web_search"):
        try:
            from src.m8_crm.browser_searcher import BrowserSearcher
            import os
            proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
            searcher = BrowserSearcher(proxy=proxy, headless=True)
            raw_results = searcher.search(query=query, max_results=max_results)
        except Exception as e:
            search_error = str(e)
            if mode == "web_search":
                return JSONResponse(status_code=500, content={
                    "success": False, "error": f"网页搜索失败: {search_error}"
                })

    # ── Step 2: AI 分析（有搜索结果则分析结果，无结果则用AI知识库） ──
    try:
        from src.utils.prompts import load_prompt, fill_prompt
        from src.core.llm_client import LLMClient

        # 获取已有客户名单用于去重
        from src.core.database import FTDatabase
        db_ro = FTDatabase()
        existing_rows = db_ro.fetchall("SELECT company_name, country FROM clients")
        db_ro.close()
        existing_list = [f"- {r['company_name']} ({r.get('country', '')})" for r in existing_rows]
        existing_str = "\n".join(existing_list) if existing_list else "(CRM is empty)"

        if raw_results:
            # 有搜索结果 → 用 analyze_real_company 模板分析
            template = load_prompt("outreach/analyze_real_company")
            companies_text = ""
            for i, r in enumerate(raw_results, 1):
                companies_text += f"\n### Company {i}\n"
                companies_text += f"- Name: {r.get('name', 'Unknown')}\n"
                companies_text += f"- URL: {r.get('url', 'N/A')}\n"
                companies_text += f"- Domain: {r.get('domain', 'N/A')}\n"
                if r.get("snippet"):
                    companies_text += f"- Search snippet: {r['snippet'][:300]}\n"
                if r.get("emails"):
                    companies_text += f"- Emails found: {', '.join(r['emails'][:5])}\n"
                if r.get("emails_from_search"):
                    companies_text += f"- Emails (search): {', '.join(r['emails_from_search'])}\n"
                if r.get("phones"):
                    companies_text += f"- Phones found: {', '.join(r['phones'][:5])}\n"
                if r.get("whatsapp"):
                    companies_text += f"- WhatsApp: {', '.join(r['whatsapp'])}\n"
                if r.get("linkedin"):
                    companies_text += f"- LinkedIn: {', '.join(r['linkedin'])}\n"
                if r.get("page_title"):
                    companies_text += f"- Page title: {r['page_title']}\n"
                if r.get("raw_text_snippet"):
                    companies_text += f"- Page text excerpt: {r['raw_text_snippet'][:500]}\n"

            prompt = fill_prompt(template, {
                "search_query": query,
                "companies_data": companies_text,
            })
        else:
            # 无搜索结果 → 用 AI 知识库直接找真实公司
            template = load_prompt("outreach/generate_potential_client")
            prompt = fill_prompt(template, {
                "target_market": country or market,
                "count": str(max_results),
                "existing_clients": existing_str,
            })

        llm = LLMClient(scenario="outreach")
        result_text = llm.chat(prompt, temperature=0.3, max_tokens=4000)

        # 解析JSON
        if "```json" in result_text:
            json_str = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            json_str = result_text.split("```")[1].split("```")[0].strip()
        else:
            json_str = result_text.strip()

        result = _json.loads(json_str)
        clients = result.get("clients", [])

        return {
            "success": True,
            "clients": clients,
            "raw": raw_results,
            "count": len(clients),
            "search_query": query,
            "mode_used": "web_search+ai" if raw_results else "ai_direct",
            "search_error": search_error,
        }

    except _json.JSONDecodeError as e:
        return {
            "success": True, "clients": [], "raw": raw_results, "count": 0,
            "warning": f"AI返回格式错误: {str(e)}",
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "success": False, "error": f"AI分析失败: {str(e)}"
        })


@router.post("/api/batch-insert")
async def api_batch_insert_clients(request: Request):
    """API: 批量插入AI生成的潜在客户"""
    body = await request.json()
    clients = body.get("clients", [])
    if not clients:
        return JSONResponse(status_code=400, content={"error": "No clients provided"})

    # 用独立连接避免锁冲突
    from src.core.database import FTDatabase
    db = FTDatabase()
    valid_cols = {c['name'] for c in db.fetchall('PRAGMA table_info(clients)')}
    valid_cols.discard('id')
    valid_cols.discard('created_at')
    valid_cols.discard('updated_at')

    inserted = []
    errors = []
    skipped = []
    for c in clients:
        try:
            # 去重检查：同名客户不重复插入
            name = c.get("company_name", "").strip()
            if name:
                existing = db.fetchall(
                    "SELECT id FROM clients WHERE company_name = ?", (name,)
                )
                if existing:
                    skipped.append(name)
                    continue

            filtered = {k: v for k, v in c.items() if k in valid_cols}
            cid = db.client_create(filtered)
            inserted.append({"id": cid, "company_name": c.get("company_name", "")})
        except Exception as e:
            errors.append({"company_name": c.get("company_name", ""), "error": str(e)})
    db.close()
    return {"success": True, "inserted": len(inserted), "skipped": len(skipped),
            "skipped_names": skipped, "errors": errors, "details": inserted}
