"""
M7: AI报价邮件生成器
功能：根据报价计算结果，生成专业的报价邮件。
"""

import json
from datetime import datetime, timedelta
from typing import Optional

from src.core.database import FTDatabase
from src.core.llm_client import get_llm
from .calculator import PriceCalculator


QUOTATION_EMAIL_SYSTEM = """You are a professional trade sales representative for a 
Chinese manual farm tools manufacturer.

Your email style:
- Clear, professional, and concise
- Use tables for product pricing
- Include all trade terms (FOB/CIF, payment, lead time)
- Always include MOQ, delivery time, and validity
- Professional greeting and sign-off

Company: [Your Company]
Factory: [Location]
Port: Tianjin, China
Payment: T/T, L/C, Trade Assurance
Lead Time: 20-30 days after deposit
MOQ: 500 pcs per item"""


QUOTATION_EMAIL_PROMPT = """Generate a professional quotation email.

Client: {company_name} ({country})
Contact: {contact_person}

Quotation Items:
{items_table}

Total Amount: USD {total_usd}
Incoterm: {incoterm}
Payment Terms: {payment_terms}
Lead Time: {lead_time} days
Validity: {validity_days} days

Generate a professional quotation email with:
1. Greeting
2. Thank you for inquiry
3. Price table (formatted clearly)
4. Trade terms summary
5. Call to action
6. Professional sign-off

Return JSON:
{{
    "subject": "Quotation for Farm Tools — Ref: {quotation_no}",
    "body": "the full email body with proper formatting",
    "signature": "professional signature"
}}

Return ONLY the JSON."""


class QuotationEmailGenerator:
    """AI报价邮件生成器"""

    def __init__(self, db: Optional[FTDatabase] = None):
        self.db = db or FTDatabase()
        self.llm = get_llm(scenario="quotation")
        self.calculator = PriceCalculator(db)

    def generate_email(
        self,
        client_id: int,
        items: list[dict],
        incoterm: str = "FOB",
        payment_terms: str = "30% T/T deposit, 70% before shipment",
        lead_time: int = 25,
        validity_days: int = 30,
        custom_notes: str = "",
    ) -> dict:
        """
        生成报价邮件。
        
        Args:
            client_id: 客户ID
            items: [{"product_code": "GS-001", "quantity": 1000}, ...]
            incoterm: FOB / CIF / EXW
            payment_terms: 付款条件
            lead_time: 交货期（天）
            validity_days: 报价有效期（天）
            
        Returns:
            {"quotation_no": str, "subject": str, "body": str, ...}
        """
        # 1. 获取客户信息
        client = self.db.fetchone(
            "SELECT * FROM clients WHERE id = ?", (client_id,)
        )
        if not client:
            return {"error": f"Client {client_id} not found"}
        client = dict(client)

        # 2. 计算报价
        market = client.get("country", "")
        batch_result = self.calculator.batch_quote(
            items=items, market=market, incoterm=incoterm
        )

        # 3. 创建报价单记录
        quotation_no = self.db.quotation_create({
            "client_id": client_id,
            "product_code": items[0]["product_code"] if items else "",
            "quantity": sum(i["quantity"] for i in items),
            "unit_price": batch_result["items"][0]["unit_price_usd"] if batch_result["items"] else 0,
            "currency": "USD",
            "incoterm": incoterm,
            "port": "Tianjin",
            "payment_terms": payment_terms,
            "lead_time_days": lead_time,
            "validity_days": validity_days,
            "total_amount": batch_result["total_usd"],
            "status": "draft",
        })

        # 4. 构建价格表格
        items_table = self._build_table(batch_result["items"])

        # 5. 调用LLM生成邮件
        prompt = QUOTATION_EMAIL_PROMPT.format(
            company_name=client.get("company_name", "Unknown"),
            contact_person=client.get("contact_person", "N/A"),
            items_table=items_table,
            total_usd=f"{batch_result['total_usd']:,.2f}",
            incoterm=incoterm,
            payment_terms=payment_terms,
            lead_time=lead_time,
            validity_days=validity_days,
            quotation_no=quotation_no,
        )

        try:
            result = self.llm.generate_json(
                prompt=prompt,
                system_prompt=QUOTATION_EMAIL_SYSTEM,
            )
        except Exception as e:
            result = {
                "subject": f"Quotation {quotation_no} — Farm Tools",
                "body": f"Dear {client.get('contact_person', '')},\n\nPlease find our quotation...",
                "signature": "Best regards",
                "error": str(e),
            }

        # 6. 更新报价单的邮件内容
        self.db.execute(
            """UPDATE quotations SET email_body = ?, status = 'sent', updated_at = ?
               WHERE quotation_no = ?""",
            (result.get("body", ""), datetime.now().isoformat(), quotation_no)
        )
        self.db.commit()

        return {
            "quotation_no": quotation_no,
            "subject": result.get("subject", ""),
            "body": result.get("body", ""),
            "signature": result.get("signature", ""),
            "total_usd": batch_result["total_usd"],
            "total_cbm": batch_result["total_cbm"],
            "items": batch_result["items"],
        }

    def _build_table(self, items: list[dict]) -> str:
        """构建价格表格文本"""
        lines = ["No. | Product | Qty | Unit Price | Total"]
        lines.append("--- | --- | --- | --- | ---")
        for i, item in enumerate(items, 1):
            lines.append(
                f"{i} | {item.get('product_code', '')} {item.get('product_name', '')} | "
                f"{item.get('quantity', 0):,} pcs | "
                f"USD {item.get('unit_price_usd', 0):.2f} | "
                f"USD {item.get('total_usd', 0):,.2f}"
            )
        return "\n".join(lines)

    def get_quotation(self, quotation_no: str) -> Optional[dict]:
        """获取报价单"""
        return self.db.fetchone(
            "SELECT * FROM quotations WHERE quotation_no = ?", (quotation_no,)
        )

    def list_quotations(
        self,
        client_id: Optional[int] = None,
        status: Optional[str] = None,
        limit: int = 20,
    ) -> list[dict]:
        """列出报价单"""
        sql = """SELECT q.*, c.company_name, c.country 
                 FROM quotations q 
                 LEFT JOIN clients c ON q.client_id = c.id 
                 WHERE 1=1"""
        params = []
        if client_id:
            sql += " AND q.client_id = ?"
            params.append(client_id)
        if status:
            sql += " AND q.status = ?"
            params.append(status)
        sql += " ORDER BY q.created_at DESC LIMIT ?"
        params.append(limit)
        return self.db.fetchall(sql, tuple(params))

    def update_status(self, quotation_no: str, status: str) -> bool:
        """更新报价单状态"""
        self.db.execute(
            "UPDATE quotations SET status = ?, updated_at = ? WHERE quotation_no = ?",
            (status, datetime.now().isoformat(), quotation_no)
        )
        self.db.commit()
        return True
