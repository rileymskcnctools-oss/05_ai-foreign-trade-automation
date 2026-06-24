"""
M6: AI邮件开发信生成器
功能：根据客户画像+产品信息，生成个性化邮件开发信。
"""

import json
from datetime import datetime
from typing import Optional

from src.core.database import FTDatabase
from src.core.llm_client import get_llm


EMAIL_SYSTEM_PROMPT = """You are a professional B2B cold email specialist for a Chinese 
manual farm tools manufacturer (shovels, hoes, rakes, pickaxes, garden tools).

Your style:
- Professional but warm, not pushy
- Short paragraphs (3-4 sentences max)
- Clear value proposition
- Specific product references
- Professional signature

Company: [Your Company Name]
Products: Manual farm tools, garden tools, agricultural hand tools
Factory: [Location]
Certifications: ISO 9001, CE, SGS
MOQ: Usually 500-1000 pcs
Lead time: 20-30 days
Payment: T/T, L/C, Trade Assurance

Write in English. Always end with a clear call-to-action."""


EMAIL_PROMPT = """Generate a personalized cold outreach email.

Client Info:
- Company: {company_name}
- Country: {country}
- Contact: {contact_person}
- Business Type: {business_type}
- Current Products: {main_products}
- Grade: {grade}
{activity_context}

Message Type: {message_type}
{custom_instructions}

Generate:
1. Subject line (compelling, under 60 chars)
2. Email body (200-300 words, professional)
3. P.S. line (one extra hook)

Return JSON:
{{
    "subject": "...",
    "body": "...",
    "ps_line": "...",
    "tone": "professional/friendly/urgent",
    "cta": "what call-to-action was used"
}}

Return ONLY the JSON."""


class EmailGenerator:
    """AI邮件开发信生成器"""

    def __init__(self, db: Optional[FTDatabase] = None):
        self.db = db or FTDatabase()
        self.llm = get_llm(scenario="outreach")

    def generate(
        self,
        client_id: int,
        message_type: str = "cold_intro",
        custom_instructions: str = "",
        product_codes: Optional[list[str]] = None,
    ) -> dict:
        """
        为指定客户生成邮件开发信。
        
        Args:
            client_id: 客户ID
            message_type: cold_intro / follow_up / re_engage / promotion
            custom_instructions: 自定义指令
            product_codes: 指定推荐的产品编码
            
        Returns:
            {"subject": str, "body": str, "ps_line": str, ...}
        """
        # 1. 获取客户信息
        client = self.db.fetchone(
            "SELECT * FROM clients WHERE id = ?", (client_id,)
        )
        if not client:
            return {"error": f"Client {client_id} not found"}
        client = dict(client)

        # 2. 获取活动历史
        activities = self.db.fetchall(
            """SELECT activity_type, direction, subject, status, created_at
               FROM activities WHERE client_id = ?
               ORDER BY created_at DESC LIMIT 5""",
            (client_id,)
        )

        # 3. 构建活动上下文
        activity_context = ""
        if activities:
            activity_context = "\nRecent interactions:\n" + "\n".join(
                f"- {a['created_at'][:10]}: {a['activity_type']} ({a['direction']}) - {a.get('subject', 'N/A')}"
                for a in activities
            )

        # 4. 构建提示词
        prompt = EMAIL_PROMPT.format(
            company_name=client.get("company_name", "Unknown"),
            country=client.get("country", "Unknown"),
            contact_person=client.get("contact_person", "N/A"),
            business_type=client.get("business_type", "N/A"),
            main_products=client.get("main_products", "N/A"),
            grade=client.get("grade", "N/A"),
            activity_context=activity_context,
            message_type=message_type,
            custom_instructions=custom_instructions or "No special instructions.",
        )

        # 5. 调用LLM
        try:
            result = self.llm.generate_json(
                prompt=prompt,
                system_prompt=EMAIL_SYSTEM_PROMPT,
            )
        except Exception as e:
            result = {
                "subject": f"Farm Tools Inquiry - {client.get('company_name', '')}",
                "body": f"Dear {client.get('contact_person', 'Sir/Madam')},\n\n...",
                "ps_line": "Looking forward to your reply.",
                "tone": "professional",
                "cta": "inquiry_reply",
                "error": str(e),
            }

        # 6. 记录到数据库
        content_text = f"Subject: {result.get('subject', '')}\n\n{result.get('body', '')}"
        self.db.execute(
            """INSERT INTO content_records 
               (product_code, content_type, platform, target_market, content, 
                version, status, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                product_codes[0] if product_codes else "",
                "email_outreach",
                "email",
                client.get("country", ""),
                content_text,
                1,
                "draft",
                datetime.now().isoformat(),
            )
        )
        self.db.commit()

        return result

    def follow_up(
        self,
        client_id: int,
        last_activity_summary: str = "",
    ) -> dict:
        """生成跟进邮件"""
        return self.generate(
            client_id=client_id,
            message_type="follow_up",
            custom_instructions=f"Previous interaction summary: {last_activity_summary}" if last_activity_summary else "",
        )

    def re_engage(self, client_id: int) -> dict:
        """生成重新激活邮件"""
        return self.generate(
            client_id=client_id,
            message_type="re_engage",
            custom_instructions="Client has been inactive for a while. Make it compelling but not pushy.",
        )
