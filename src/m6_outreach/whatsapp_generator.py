"""
M6: AI WhatsApp消息生成器
功能：根据客户画像生成适合WhatsApp的简短沟通消息。
"""

import json
from datetime import datetime
from typing import Optional

from src.core.database import FTDatabase
from src.core.llm_client import get_llm


WHATSAPP_SYSTEM_PROMPT = """You are a friendly B2B WhatsApp sales specialist for a 
Chinese manual farm tools company.

WhatsApp message style:
- SHORT and conversational (under 100 words)
- Use simple English, easy to read
- Friendly tone with occasional emojis (but not excessive)
- Clear purpose - always have a next step
- Include product photos/catalogs when relevant
- Quick response expected

Products: Manual farm tools, garden tools, agricultural hand tools
MOQ: 500-1000 pcs
Lead time: 20-30 days"""


WHATSAPP_PROMPT = """Generate a WhatsApp message for a potential client.

Client: {company_name} ({country})
Contact: {contact_person}
Business Type: {business_type}
Grade: {grade}
Message Purpose: {message_type}
{custom_instructions}

Generate a short, friendly WhatsApp message.
Return JSON:
{{
    "message": "the WhatsApp message text (under 100 words)",
    "emoji_used": ["list of emojis used"],
    "call_to_action": "what you want them to do next",
    "suggested_reply": "auto-reply suggestion for them"
}}

Return ONLY the JSON."""


class WhatsAppGenerator:
    """AI WhatsApp消息生成器"""

    def __init__(self, db: Optional[FTDatabase] = None):
        self.db = db or FTDatabase()
        self.llm = get_llm(scenario="outreach")

    def generate(
        self,
        client_id: int,
        message_type: str = "cold_intro",
        custom_instructions: str = "",
    ) -> dict:
        """
        为指定客户生成WhatsApp消息。
        
        Args:
            client_id: 客户ID
            message_type: cold_intro / follow_up / promotion / quote_share
            custom_instructions: 自定义指令
        """
        client = self.db.fetchone(
            "SELECT * FROM clients WHERE id = ?", (client_id,)
        )
        if not client:
            return {"error": f"Client {client_id} not found"}
        client = dict(client)

        prompt = WHATSAPP_PROMPT.format(
            company_name=client.get("company_name", "Unknown"),
            country=client.get("country", "Unknown"),
            contact_person=client.get("contact_person", "N/A"),
            business_type=client.get("business_type", "N/A"),
            grade=client.get("grade", "N/A"),
            message_type=message_type,
            custom_instructions=custom_instructions or "",
        )

        try:
            result = self.llm.generate_json(
                prompt=prompt,
                system_prompt=WHATSAPP_SYSTEM_PROMPT,
            )
        except Exception as e:
            result = {
                "message": f"Hi {client.get('contact_person', '')}! We have quality farm tools...",
                "emoji_used": [],
                "call_to_action": "reply",
                "suggested_reply": "Tell me more",
                "error": str(e),
            }

        # 记录到数据库
        self.db.execute(
            """INSERT INTO content_records 
               (product_code, content_type, platform, target_market, content, 
                version, status, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                "",
                "whatsapp_outreach",
                "whatsapp",
                client.get("country", ""),
                result.get("message", ""),
                1,
                "draft",
                datetime.now().isoformat(),
            )
        )
        self.db.commit()

        return result

    def quick_greeting(self, client_id: int) -> str:
        """快速打招呼消息"""
        client = self.db.fetchone(
            "SELECT company_name, contact_person FROM clients WHERE id = ?",
            (client_id,)
        )
        if client:
            return f"Hi {client['contact_person']}! 👋 I'm from [Company]. We specialize in farm tools. Are you interested in our latest catalog? 🌾"
        return "Hi! 👋 We have quality farm tools at competitive prices. Interested?"

    def share_catalog(self, client_id: int) -> dict:
        """分享产品目录消息"""
        return self.generate(
            client_id=client_id,
            message_type="catalog_share",
            custom_instructions="Share our product catalog. Highlight bestsellers for their market.",
        )
