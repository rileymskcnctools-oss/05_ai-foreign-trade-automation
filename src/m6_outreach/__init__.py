# m6_outreach package
"""
M6: AI开发信Agent (Outreach Agent)
根据客户画像自动生成个性化开发信（邮件/WhatsApp/LinkedIn）。

组件:
    - email_generator: 邮件开发信
    - whatsapp_generator: WhatsApp消息
    - linkedin_generator: LinkedIn连接消息
    - template_manager: 模板管理
"""
from .email_generator import EmailGenerator
from .whatsapp_generator import WhatsAppGenerator
from .linkedin_generator import LinkedInGenerator
from .template_manager import TemplateManager

__all__ = ["EmailGenerator", "WhatsAppGenerator", "LinkedInGenerator", "TemplateManager"]
