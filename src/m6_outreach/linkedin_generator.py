"""
M6: AI LinkedIn消息生成器
功能：生成LinkedIn连接请求和InMail消息。
"""

import json
from datetime import datetime
from typing import Optional

from src.core.database import FTDatabase
from src.core.llm_client import get_llm


LINKEDIN_SYSTEM_PROMPT = """You are a B2B LinkedIn outreach specialist for a Chinese 
manual farm tools manufacturer.

LinkedIn message style:
- Professional but personal
- Reference something specific about their profile/company
- Connection request: under 300 characters
- InMail: under 400 words
- Focus on value, not selling
- End with a soft question"""


LINKEDIN_PROMPT = """Generate a LinkedIn outreach message.

Client: {company_name} ({country})
Contact: {contact_person}
Business Type: {business_type}
Message Type: {message_type}
{extra_info}

Generate LinkedIn messages:
Return JSON:
{{
    "connection_request": "short connection request (under 300 chars)",
    "follow_up_message": "longer message after they accept (under 400 words)",
    "inmail_subject": "InMail subject line (if applicable)",
    "inmail_body": "InMail body (if applicable)",
    "personalization_points": ["things to reference about them"]
}}

Return ONLY the JSON."""


class LinkedInGenerator:
    """AI LinkedIn消息生成器"""

    def __init__(self, db: Optional[FTDatabase] = None):
        self.db = db or FTDatabase()
        self.llm = get_llm(scenario="outreach")

    def generate(
        self,
        client_id: int,
        message_type: str = "connection_request",
        custom_instructions: str = "",
    ) -> dict:
        """
        为指定客户生成LinkedIn消息。
        
        Args:
            client_id: 客户ID
            message_type: connection_request / inmail / follow_up
            custom_instructions: 自定义指令
        """
        client = self.db.fetchone(
            "SELECT * FROM clients WHERE id = ?", (client_id,)
        )
        if not client:
            return {"error": f"Client {client_id} not found"}
        client = dict(client)

        prompt = LINKEDIN_PROMPT.format(
            company_name=client.get("company_name", "Unknown"),
            country=client.get("country", "Unknown"),
            contact_person=client.get("contact_person", "N/A"),
            business_type=client.get("business_type", "N/A"),
            message_type=message_type,
            extra_info=f"LinkedIn: {client.get('linkedin', 'N/A')}\n{custom_instructions}",
        )

        try:
            result = self.llm.generate_json(
                prompt=prompt,
                system_prompt=LINKEDIN_SYSTEM_PROMPT,
            )
        except Exception as e:
            result = {
                "connection_request": f"Hi {client.get('contact_person', '')}, I'd love to connect...",
                "follow_up_message": "",
                "inmail_subject": "",
                "inmail_body": "",
                "personalization_points": [],
                "error": str(e),
            }

        # 记录
        self.db.execute(
            """INSERT INTO content_records 
               (product_code, content_type, platform, target_market, content, 
                version, status, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                "",
                "linkedin_outreach",
                "linkedin",
                client.get("country", ""),
                json.dumps(result, ensure_ascii=False),
                1,
                "draft",
                datetime.now().isoformat(),
            )
        )
        self.db.commit()

        return result

    def connection_request(self, client_id: int) -> str:
        """快速生成连接请求"""
        result = self.generate(client_id, message_type="connection_request")
        return result.get("connection_request", "")

    def inmail(self, client_id: int) -> dict:
        """生成InMail消息"""
        return self.generate(client_id, message_type="inmail")
