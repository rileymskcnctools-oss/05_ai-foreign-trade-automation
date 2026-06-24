"""
M5: 客户跟进策略建议器
功能：根据客户评级和信息，AI生成个性化跟进建议。
"""

import json
from datetime import datetime
from typing import Optional

from src.core.database import FTDatabase
from src.core.llm_client import get_llm


ADVICE_PROMPT = """You are a senior B2B sales strategist for a Chinese manual farm tools 
company (shovels, hoes, rakes, pickaxes, garden tools).

Generate personalized follow-up strategy for this client.

Client Profile:
- Company: {company_name}
- Country: {country}
- Grade: {grade} (Score: {grade_score})
- Business Type: {business_type}
- Contact: {contact_person}
- Source: {source}
- Status: {status}
{activity_history}
{product_info}

Provide a follow-up strategy with:
1. Recommended approach (email / WhatsApp / LinkedIn / combination)
2. Key talking points (what to highlight)
3. Product recommendations (which of our products to push)
4. Timing and follow-up schedule
5. Risk assessment

Return JSON:
{{
    "recommended_approach": "email_first",
    "talking_points": ["point1", "point2", "point3"],
    "recommended_products": ["GF-001", "GS-001"],
    "follow_up_schedule": [
        {{"day": 0, "action": "Send initial email", "channel": "email"}},
        {{"day": 7, "action": "WhatsApp follow-up", "channel": "whatsapp"}},
        {{"day": 14, "action": "Call if no response", "channel": "phone"}}
    ],
    "risk_level": "low",
    "risk_notes": "...",
    "email_tips": "...",
    "overall_strategy": "One paragraph strategic recommendation"
}}

Return ONLY the JSON object."""


class ClientAdvisor:
    """客户跟进策略建议器"""

    def __init__(self, db: Optional[FTDatabase] = None):
        self.db = db or FTDatabase()
        self.llm = get_llm(scenario="client_analysis")

    def get_advice(self, client_id: int) -> dict:
        """
        为指定客户生成跟进建议。
        
        Args:
            client_id: 客户ID
            
        Returns:
            跟进策略建议
        """
        # 1. 获取客户信息
        client = self.db.fetchone(
            "SELECT * FROM clients WHERE id = ?", (client_id,)
        )
        if not client:
            return {"error": f"Client {client_id} not found"}

        client = dict(client)

        # 2. 获取联系历史
        activities = self.db.fetchall(
            """SELECT activity_type, direction, subject, status, created_at
               FROM activities WHERE client_id = ?
               ORDER BY created_at DESC LIMIT 10""",
            (client_id,)
        )

        # 3. 获取相关产品信息
        matched_products = self._find_matched_products(client)

        # 4. 构建提示词
        activity_text = ""
        if activities:
            activity_text = "\nRecent Activities:\n" + "\n".join(
                f"- {a['created_at'][:10]}: {a['activity_type']} ({a['direction']}) - {a.get('subject', 'N/A')} [{a.get('status', 'N/A')}]"
                for a in activities
            )

        product_text = ""
        if matched_products:
            product_text = "\nMatched Products:\n" + "\n".join(
                f"- {p['product_code']}: {p['product_name_en']}"
                for p in matched_products
            )

        prompt = ADVICE_PROMPT.format(
            company_name=client.get("company_name", "Unknown"),
            country=client.get("country", "Unknown"),
            grade=client.get("grade", "N/A"),
            grade_score=client.get("grade_score", 0),
            business_type=client.get("business_type", "N/A"),
            contact_person=client.get("contact_person", "N/A"),
            source=client.get("source", "N/A"),
            status=client.get("status", "prospect"),
            activity_history=activity_text,
            product_info=product_text,
        )

        # 5. 调用LLM
        try:
            result = self.llm.generate_json(
                prompt=prompt,
                system_prompt="You are a B2B sales strategist. Return valid JSON only.",
            )
        except Exception as e:
            result = {
                "recommended_approach": "email_first",
                "talking_points": ["Product quality", "Competitive pricing", "Fast delivery"],
                "recommended_products": [],
                "follow_up_schedule": [],
                "risk_level": "medium",
                "risk_notes": f"Unable to generate advice: {str(e)}",
                "overall_strategy": "Manual review needed.",
            }

        # 6. 更新客户分析记录
        client_id = client.get("id")
        if client_id:
            analysis = {
                "client_id": client_id,
                "analysis_type": "update",
                "summary": result.get("overall_strategy", "")[:500],
                "full_analysis": json.dumps(result, ensure_ascii=False),
                "grade_suggested": client.get("grade"),
                "recommendations": json.dumps(result.get("talking_points", []), ensure_ascii=False),
                "created_at": datetime.now().isoformat(),
            }
            columns = ", ".join(analysis.keys())
            placeholders = ", ".join(["?"] * len(analysis))
            self.db.execute(
                f"INSERT INTO client_analyses ({columns}) VALUES ({placeholders})",
                tuple(analysis.values())
            )
            self.db.commit()

        return result

    def _find_matched_products(self, client: dict) -> list[dict]:
        """根据客户信息匹配产品"""
        # 简单匹配：按类别和关键词
        sql = "SELECT product_code, product_name_en, category FROM products WHERE status = 'active'"
        params = []

        # 如果知道客户国家，优先推荐目标市场包含该国的产品
        country = client.get("country")
        if country:
            sql += " AND (target_markets LIKE ? OR target_markets = '')"
            params.append(f"%{country}%")

        sql += " LIMIT 10"
        return self.db.fetchall(sql, tuple(params))

    def get_all_strategies(self) -> list[dict]:
        """获取所有客户的最新策略建议"""
        return self.db.fetchall("""
            SELECT ca.client_id, c.company_name, c.country, c.grade,
                   ca.recommendations, ca.created_at
            FROM client_analyses ca
            JOIN clients c ON ca.client_id = c.id
            WHERE ca.id IN (
                SELECT MAX(id) FROM client_analyses GROUP BY client_id
            )
            ORDER BY ca.created_at DESC
        """)
