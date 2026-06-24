"""
M6: 模板管理器
功能：管理邮件/消息模板，支持预设模板和自定义模板。
"""

from datetime import datetime
from typing import Optional

from src.core.database import FTDatabase


class TemplateManager:
    """消息模板管理器"""

    # 预设邮件模板
    DEFAULT_EMAIL_TEMPLATES = [
        {
            "name": "cold_intro",
            "channel": "email",
            "subject_line": "Farm Tools Direct from Factory — ISO Certified",
            "template_body": """Dear {contact_person},

I noticed {company_name} works in {business_type} in {country}. We are a Chinese manufacturer specializing in manual farm tools — shovels, hoes, rakes, pickaxes, and garden tools.

Why work with us:
• Factory-direct pricing (no middleman)
• ISO 9001 & CE certified
• 20-30 day lead time
• MOQ from 500 pcs

I'd love to share our latest catalog. Would you be open to a quick chat?

Best regards""",
        },
        {
            "name": "follow_up",
            "channel": "email",
            "subject_line": "Following Up — Farm Tools for {company_name}",
            "template_body": """Hi {contact_person},

I reached out last week about our farm tools. I understand you're busy, so I'll keep this short.

We just launched a new heavy-duty shovel line that's selling well in {country}. I think it could be a great fit for your customers.

Would you like me to send over some specs and pricing?

Best regards""",
        },
        {
            "name": "promotion",
            "channel": "email",
            "subject_line": "Special Offer — 10% Off First Order",
            "template_body": """Dear {contact_person},

Great news! We're offering 10% off your first order of any farm tools.

Products included:
• Round Point Shovels
• Flat Garden Hoes
• Bow Rakes
• Forged Pickaxes

Offer valid until {deadline}. Interested?

Best regards""",
        },
    ]

    DEFAULT_WHATSAPP_TEMPLATES = [
        {
            "name": "quick_intro",
            "channel": "whatsapp",
            "subject_line": "",
            "template_body": "Hi {contact_person}! 👋 I'm from a farm tools factory in China. We supply shovels, hoes, rakes & pickaxes. Interested in our catalog? 🌾",
        },
        {
            "name": "catalog_share",
            "channel": "whatsapp",
            "subject_line": "",
            "template_body": "Hi {contact_person}! 📋 Here's our latest farm tools catalog. We have 50+ models with ISO certification. Which products interest you most? 🛠️",
        },
    ]

    def __init__(self, db: Optional[FTDatabase] = None):
        self.db = db or FTDatabase()

    def init_default_templates(self) -> int:
        """初始化预设模板"""
        existing = self.db.fetchall(
            "SELECT name, channel FROM outreach_templates"
        )
        existing_keys = {(t["name"], t["channel"]) for t in existing}

        count = 0
        for tpl in self.DEFAULT_EMAIL_TEMPLATES + self.DEFAULT_WHATSAPP_TEMPLATES:
            if (tpl["name"], tpl["channel"]) not in existing_keys:
                self.create(tpl)
                count += 1
        return count

    def create(self, data: dict) -> int:
        """创建模板"""
        now = datetime.now().isoformat()
        data.setdefault("created_at", now)
        data.setdefault("updated_at", now)

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        cursor = self.db.execute(
            f"INSERT INTO outreach_templates ({columns}) VALUES ({placeholders})",
            tuple(data.values())
        )
        self.db.commit()
        return cursor.lastrowid

    def get(self, template_id: int) -> Optional[dict]:
        """获取模板"""
        return self.db.fetchone(
            "SELECT * FROM outreach_templates WHERE id = ?", (template_id,)
        )

    def list_all(
        self,
        channel: Optional[str] = None,
    ) -> list[dict]:
        """列出模板"""
        sql = "SELECT * FROM outreach_templates WHERE 1=1"
        params = []
        if channel:
            sql += " AND channel = ?"
            params.append(channel)
        sql += " ORDER BY name"
        return self.db.fetchall(sql, tuple(params))

    def update(self, template_id: int, data: dict) -> bool:
        """更新模板"""
        data["updated_at"] = datetime.now().isoformat()
        sets = ", ".join(f"{k} = ?" for k in data.keys())
        params = list(data.values()) + [template_id]
        self.db.execute(
            f"UPDATE outreach_templates SET {sets} WHERE id = ?", tuple(params)
        )
        self.db.commit()
        return True

    def delete(self, template_id: int) -> bool:
        """删除模板"""
        self.db.execute("DELETE FROM outreach_templates WHERE id = ?", (template_id,))
        self.db.commit()
        return True

    def render(self, template_id: int, variables: dict) -> str:
        """
        渲染模板，替换变量占位符。
        
        Args:
            template_id: 模板ID
            variables: 变量字典，如 {"contact_person": "John", "company_name": "ABC Co"}
        """
        tpl = self.get(template_id)
        if not tpl:
            return ""
        content = tpl["template_body"]
        for key, value in variables.items():
            content = content.replace(f"{{{key}}}", str(value))
        return content
