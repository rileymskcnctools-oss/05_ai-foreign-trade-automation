"""市场研究路由 — 增强版市场研究工作台"""
from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
import os
import json
import io
import re
from datetime import datetime
from typing import Optional

from web.deps import get_db

router = APIRouter(prefix="/market")


# ============================================================
# 报告相关 API
# ============================================================

@router.get("/api/reports")
async def api_list_reports(
    country: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    limit: int = Query(50),
):
    """API: 列出市场报告（支持搜索/筛选）"""
    db = get_db()
    sql = "SELECT id, country, product_category, report_title, summary, confidence, created_at FROM market_reports WHERE 1=1"
    params = []
    if country:
        sql += " AND country LIKE ?"
        params.append(f"%{country}%")
    if keyword:
        sql += " AND (report_title LIKE ? OR summary LIKE ? OR country LIKE ?)"
        params.extend([f"%{keyword}%"] * 3)
    sql += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    reports = db.fetchall(sql, tuple(params))
    return {"reports": reports, "total": len(reports)}


@router.post("/api/generate-report")
async def api_generate_report(request: Request):
    """API: 生成市场研究报告（支持实时网络数据采集）"""
    db = get_db()
    from src.m4_market_research.report_generator import MarketResearchAgent
    data = await request.json()
    agent = MarketResearchAgent(db)
    result = agent.generate_report(
        country=data["country"],
        product_category=data.get("product_category", "Manual Farm Tools"),
        extra_context=data.get("extra_context", ""),
        use_web_research=data.get("use_web_research", True),
    )
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
    # 同时获取该国家的知识点
    knowledge = db.fetchall(
        "SELECT * FROM market_knowledge WHERE country = ? ORDER BY category, created_at DESC",
        (report.get("country", ""),)
    )
    report["knowledge_entries"] = knowledge
    return report


@router.delete("/api/reports/{report_id}")
async def api_delete_report(report_id: int):
    """API: 删除报告"""
    db = get_db()
    if db.report_delete(report_id):
        return {"success": True, "deleted_id": report_id}
    return JSONResponse(status_code=404, content={"error": "Report not found"})


# ============================================================
# 知识库 API
# ============================================================

@router.get("/api/knowledge")
async def api_list_knowledge(
    country: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    limit: int = Query(100),
):
    """API: 列出知识库条目（支持筛选）"""
    db = get_db()
    sql = "SELECT * FROM market_knowledge WHERE 1=1"
    params = []
    if country:
        sql += " AND country LIKE ?"
        params.append(f"%{country}%")
    if category:
        sql += " AND category = ?"
        params.append(category)
    if keyword:
        sql += " AND knowledge LIKE ?"
        params.append(f"%{keyword}%")
    sql += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    items = db.fetchall(sql, tuple(params))
    return {"items": items, "total": len(items)}


@router.get("/api/knowledge/stats")
async def api_knowledge_stats():
    """API: 知识库统计"""
    db = get_db()
    # 按国家统计
    by_country = db.fetchall(
        "SELECT country, COUNT(*) as count FROM market_knowledge GROUP BY country ORDER BY count DESC"
    )
    # 按类别统计
    by_category = db.fetchall(
        "SELECT category, COUNT(*) as count FROM market_knowledge GROUP BY category ORDER BY count DESC"
    )
    # 总数
    total = db.fetchone("SELECT COUNT(*) as c FROM market_knowledge")
    return {
        "total": total["c"],
        "by_country": by_country,
        "by_category": by_category,
    }


# ============================================================
# 市场对比 API
# ============================================================

@router.get("/api/compare")
async def api_compare_markets(
    countries: str = Query(..., description="逗号分隔的国家列表"),
):
    """API: 多国市场对比"""
    db = get_db()
    country_list = [c.strip() for c in countries.split(",") if c.strip()]
    if not country_list:
        return JSONResponse(status_code=400, content={"error": "请提供至少一个国家"})

    results = []
    for country in country_list:
        # 获取最新报告
        report = db.fetchone(
            "SELECT * FROM market_reports WHERE country LIKE ? ORDER BY created_at DESC LIMIT 1",
            (f"%{country}%",)
        )
        # 获取知识点
        knowledge = db.fetchall(
            "SELECT category, knowledge FROM market_knowledge WHERE country LIKE ? ORDER BY created_at DESC",
            (f"%{country}%",)
        )
        # 按类别整理知识点
        knowledge_by_cat = {}
        for k in knowledge:
            cat = k["category"]
            if cat not in knowledge_by_cat:
                knowledge_by_cat[cat] = []
            knowledge_by_cat[cat].append(k["knowledge"])

        # 获取该国家的客户数
        client_count = db.fetchone(
            "SELECT COUNT(*) as c FROM clients WHERE country LIKE ?",
            (f"%{country}%",)
        )

        results.append({
            "country": country,
            "has_report": report is not None,
            "report_title": report["report_title"] if report else None,
            "summary": report["summary"] if report else "暂无报告",
            "confidence": report["confidence"] if report else None,
            "report_date": report["created_at"] if report else None,
            "knowledge_count": len(knowledge),
            "knowledge": knowledge_by_cat,
            "client_count": client_count["c"] if client_count else 0,
        })

    return {"countries": results, "count": len(results)}


@router.get("/api/compare/available-countries")
async def api_available_countries():
    """API: 获取已有报告或知识的国家列表"""
    db = get_db()
    report_countries = db.fetchall(
        "SELECT DISTINCT country, COUNT(*) as report_count FROM market_reports GROUP BY country ORDER BY country"
    )
    knowledge_countries = db.fetchall(
        "SELECT DISTINCT country, COUNT(*) as knowledge_count FROM market_knowledge GROUP BY country ORDER BY country"
    )
    # 合并
    country_map = {}
    for c in report_countries:
        name = c["country"]
        country_map[name] = {"country": name, "reports": c["report_count"], "knowledge": 0}
    for c in knowledge_countries:
        name = c["country"]
        if name in country_map:
            country_map[name]["knowledge"] = c["knowledge_count"]
        else:
            country_map[name] = {"country": name, "reports": 0, "knowledge": c["knowledge_count"]}
    return {"countries": list(country_map.values())}


# ============================================================
# 统计概览 API
# ============================================================

@router.get("/api/stats")
async def api_market_stats():
    """API: 市场研究模块统计"""
    db = get_db()
    report_count = db.fetchone("SELECT COUNT(*) as c FROM market_reports")
    knowledge_count = db.fetchone("SELECT COUNT(*) as c FROM market_knowledge")
    countries = db.fetchall("SELECT DISTINCT country FROM market_reports")
    categories = db.fetchall("SELECT DISTINCT category FROM market_knowledge")
    return {
        "report_count": report_count["c"],
        "knowledge_count": knowledge_count["c"],
        "country_count": len(countries),
        "countries": [c["country"] for c in countries],
        "categories": [c["category"] for c in categories if c["category"]],
    }


# ============================================================
# 报告导出 API
# ============================================================

@router.get("/api/reports/{report_id}/export")
async def api_export_report(report_id: int, format: str = Query("pdf")):
    """API: 导出报告（pdf 或 txt 格式）"""
    db = get_db()
    from src.m4_market_research.report_generator import MarketResearchAgent
    agent = MarketResearchAgent(db)
    report = agent.get_report(report_id)
    if not report:
        return JSONResponse(status_code=404, content={"error": "Report not found"})

    # 获取知识点
    knowledge = db.fetchall(
        "SELECT category, knowledge FROM market_knowledge WHERE country = ? ORDER BY category",
        (report.get("country", ""),)
    )

    country = report.get("country", "unknown")
    title = report.get("report_title", "Market Report")
    full_report = report.get("full_report", "")
    summary = report.get("summary", "")
    confidence = report.get("confidence", "-")
    created = report.get("created_at", "-")[:10]
    category = report.get("product_category", "-")

    if format == "pdf":
        # 生成 PDF（fpdf2 + SimHei 中文字体）
        try:
            from fpdf import FPDF

            # 字体路径
            font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "simhei.ttf")

            class ReportPDF(FPDF):
                def header(self):
                    self.set_font("SimHei", "", 9)
                    self.set_text_color(150, 150, 150)
                    self.cell(0, 10, f"FT Workspace - {title[:40]}", align="L")
                    self.ln(12)
                    self.set_draw_color(220, 220, 220)
                    self.line(15, self.get_y(), 195, self.get_y())
                    self.ln(5)

                def footer(self):
                    self.set_y(-15)
                    self.set_font("SimHei", "", 8)
                    self.set_text_color(150, 150, 150)
                    self.cell(0, 10, f"- {self.page_no()} -", align="C")

                def write_line(self, size, style, color, text, align="L"):
                    """写一行中文文字，自动换行"""
                    self.set_font("SimHei", style, size)
                    self.set_text_color(*color)
                    self.multi_cell(0, size * 0.45, text, align=align)

                def write_list_item(self, size, color, text):
                    """写一个列表项"""
                    self.set_font("SimHei", "", size)
                    self.set_text_color(*color)
                    x = self.get_x()
                    self.cell(8, size * 0.45, "  > ")
                    self.multi_cell(0, size * 0.45, text)

            pdf = ReportPDF()
            pdf.set_auto_page_break(auto=True, margin=20)
            pdf.add_font("SimHei", "", font_path, uni=True)
            pdf.add_page()

            # 封面
            pdf.ln(40)
            pdf.write_line(22, "", (26, 60, 110), title, align="C")
            pdf.ln(8)
            # 分隔线
            pdf.set_draw_color(26, 60, 110)
            pdf.set_line_width(0.8)
            pdf.line(60, pdf.get_y(), 150, pdf.get_y())
            pdf.set_line_width(0.2)
            pdf.ln(12)
            for info in [f"目标国家: {country}", f"产品类别: {category}", f"报告日期: {created}", f"置信度: {confidence}"]:
                pdf.write_line(11, "", (100, 100, 100), info, align="C")
                pdf.ln(2)

            # 摘要页
            pdf.add_page()
            pdf.write_line(14, "", (26, 60, 110), "报告摘要")
            pdf.ln(3)
            pdf.set_draw_color(26, 60, 110)
            pdf.line(15, pdf.get_y(), 80, pdf.get_y())
            pdf.ln(5)
            # 摘要框
            pdf.set_fill_color(235, 245, 255)
            pdf.set_draw_color(200, 220, 240)
            y_start = pdf.get_y()
            pdf.set_font("SimHei", "", 11)
            pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(180, 6, summary, fill=True)
            pdf.ln(10)

            # 正文
            pdf.write_line(16, "", (26, 60, 110), "报告正文")
            pdf.set_draw_color(26, 60, 110)
            pdf.line(15, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(6)

            # 逐行解析 Markdown 渲染
            import re as _re
            for line in full_report.split("\n"):
                stripped = line.strip()
                if not stripped:
                    pdf.ln(3)
                    continue

                # 清理 markdown 标记
                clean = _re.sub(r'\*\*(.+?)\*\*', r'\1', stripped)
                clean = _re.sub(r'\*(.+?)\*', r'\1', clean)
                clean = _re.sub(r'`(.+?)`', r'\1', clean)

                if clean.startswith("#### "):
                    pdf.ln(3)
                    pdf.write_line(10, "", (60, 60, 60), clean[5:])
                    pdf.ln(2)
                elif clean.startswith("### "):
                    pdf.ln(4)
                    pdf.write_line(11, "", (45, 55, 72), clean[4:])
                    pdf.set_draw_color(200, 210, 225)
                    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
                    pdf.ln(3)
                elif clean.startswith("## "):
                    pdf.ln(5)
                    pdf.write_line(13, "", (26, 60, 110), clean[3:])
                    pdf.set_draw_color(26, 60, 110)
                    pdf.line(15, pdf.get_y(), 100, pdf.get_y())
                    pdf.ln(4)
                elif clean.startswith("# "):
                    pdf.ln(6)
                    pdf.write_line(15, "", (26, 60, 110), clean[2:])
                    pdf.ln(4)
                elif clean.startswith("- ") or clean.startswith("* "):
                    pdf.write_list_item(10, (60, 60, 60), clean[2:])
                    pdf.ln(1)
                else:
                    pdf.write_line(10, "", (50, 50, 50), clean)
                    pdf.ln(1)

            # 知识点
            if knowledge:
                pdf.add_page()
                pdf.write_line(14, "", (26, 60, 110), f"知识库 ({len(knowledge)} 条)")
                pdf.set_draw_color(26, 60, 110)
                pdf.line(15, pdf.get_y(), 195, pdf.get_y())
                pdf.ln(6)

                cat_labels = {
                    "agriculture": "农业", "import": "进口", "competitor": "竞品",
                    "pricing": "定价", "distribution": "分销",
                }
                current_cat = None
                for k in knowledge:
                    cat = k["category"]
                    if cat != current_cat:
                        current_cat = cat
                        pdf.ln(3)
                        pdf.write_line(11, "", (45, 55, 72), cat_labels.get(cat, cat))
                        pdf.ln(2)
                    pdf.write_list_item(9, (80, 80, 80), k["knowledge"])
                    pdf.ln(1)

            # 结尾
            pdf.ln(15)
            pdf.write_line(8, "", (180, 180, 180), f"FT Workspace v4.0 | {datetime.now().strftime('%Y-%m-%d %H:%M')}", align="C")

            pdf_bytes = pdf.output()
            filename = f"market_report_{country}_{datetime.now().strftime('%Y%m%d')}.pdf"
            return StreamingResponse(
                io.BytesIO(bytes(pdf_bytes)),
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
        except Exception as e:
            import traceback
            return JSONResponse(status_code=500, content={"error": f"PDF generation failed: {str(e)}", "trace": traceback.format_exc()})

    elif format == "md":
        # Markdown 格式（推荐）
        cat_labels = {
            "agriculture": "🌾 农业", "import": "🚢 进口", "competitor": "🏢 竞品",
            "pricing": "💰 定价", "distribution": "📦 分销",
        }
        md_content = f"""# {title}

> **目标国家:** {country} | **产品类别:** {category} | **报告日期:** {created} | **置信度:** {confidence}

---

## 📝 报告摘要

{summary}

---

{full_report}

---

## 🧠 知识库 ({len(knowledge)} 条)

"""
        current_cat = None
        for k in knowledge:
            cat = k["category"]
            if cat != current_cat:
                current_cat = cat
                md_content += f"\n### {cat_labels.get(cat, cat)}\n\n"
            md_content += f"- {k['knowledge']}\n"

        md_content += f"\n---\n\n*Generated by FT Workspace v4.0 · {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
        filename = f"market_report_{country}_{datetime.now().strftime('%Y%m%d')}.md"
        return StreamingResponse(
            io.BytesIO(md_content.encode("utf-8")),
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    else:
        # TXT 格式
        content = f"""{'='*60}
  {title}
{'='*60}

Country: {country}
Category: {category}
Date: {created}
Confidence: {confidence}

{'='*60}
  FULL REPORT
{'='*60}

{full_report}

{'='*60}
  SUMMARY
{'='*60}

{summary}

{'='*60}
  KNOWLEDGE BASE ({len(knowledge)} entries)
{'='*60}
"""
        current_cat = None
        for k in knowledge:
            if k["category"] != current_cat:
                current_cat = k["category"]
                content += f"\n--- {current_cat.upper()} ---\n"
            content += f"  * {k['knowledge']}\n"

        content += f"\n{'='*60}\n  Generated by FT Workspace v4.0\n{'='*60}\n"
        filename = f"market_report_{country}_{datetime.now().strftime('%Y%m%d')}.txt"
        return StreamingResponse(
            io.BytesIO(content.encode("utf-8")),
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
