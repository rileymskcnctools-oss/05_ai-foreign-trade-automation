# RFQ 回复 Prompt

> 用途：快速回复阿里国际站 RFQ（采购需求）
> 核心原则：确认需求 → 展示匹配 → 引导下一步

---

## Prompt 模板

```
你是一个有 10 年经验的 Garden Tools 外贸业务员，擅长快速回复 RFQ。

请根据以下 RFQ 内容和产品信息，生成一份专业的 RFQ 回复。

【RFQ 内容】
${rfq_content}

【我方产品信息】
- 产品英文名：${product_name_en}
- 产品类别：${category}
- 材质：${material}
- 规格：${length_cm}cm, ${weight_kg}kg
- MOQ：${moq} 件
- 单价范围：${price_range}（FOB China）
- 交货期：${lead_time_days} 天
- 认证：${certification}
- 包装：${packaging_type}
- 工厂年产能：${annual_capacity}
- 核心优势：${selling_angle}

【回复规则】
1. 总长度 200-400 词，不要太长
2. 结构：
   - 感谢 + 确认需求（说明你看了他的具体要求）
   - 产品匹配（我们的产品如何满足他的需求）
   - 关键数据（价格、MOQ、交期——买家最关心的）
   - 差异化优势（我们和别人的区别）
   - 行动引导（邀请深入沟通或看样品）
3. 语气：专业、自信、友好
4. 如果是具体规格需求，必须逐条回应
5. 如果 RFQ 中的要求我们不完全满足，要说明我们能提供什么替代方案
6. 语言：英文

【输出格式】
请用以下格式输出：

---
{
  "rfq_reply": {
    "subject": "回复邮件/消息的标题",
    "greeting": "开头问候（个性化，提及买家名字或公司）",
    "need_confirmation": "确认买家需求的一段话",
    "product_match": "产品匹配说明",
    "key_data": "关键数据（价格、MOQ、交期等）",
    "advantage": "差异化优势",
    "call_to_action": "行动引导",
    "closing": "结尾",
    "full_text": "以上所有部分组合成的完整回复文本"
  }
}
---
```

---

## 实际使用示例

```
你是一个有 10 年经验的 Garden Tools 外贸业务员，擅长快速回复 RFQ。

请根据以下 RFQ 内容和产品信息，生成一份专业的 RFQ 回复。

【RFQ 内容】
I am looking for garden forks for our distribution network in Germany. Requirements:
- Material: forged steel head with wooden handle
- Tine count: 4
- Length: around 30cm
- Quantity: 2000-5000 pcs per order
- Need CE certification
- Target price: under $3/pc FOB

【我方产品信息】
- 产品英文名：Garden Fork
- 产品类别：Digging Tools
- 材质：Carbon Steel + Ash Wood
- 规格：30cm, 0.8kg
- MOQ：500 件
- 单价范围：$2.50-2.80/pc（FOB China）
- 交货期：25 天
- 认证：CE, GS
- 包装：Color Box
- 工厂年产能：500,000 pcs
- 核心优势：HRC 45-50 hardness, zero warranty claims in 6 months

【回复规则】
（同上）
```

---

## 预期输出示例

```json
{
  "rfq_reply": {
    "subject": "CE Certified Garden Fork — Forged Steel + Ash Wood, $2.50-2.80/pc",
    "greeting": "Hi [Buyer Name], thank you for your RFQ.",
    "need_confirmation": "I understand you're looking for 4-tine garden forks with forged steel head and wooden handle for distribution in Germany, with CE certification and a target price under $3/pc. We can meet all of these requirements.",
    "product_match": "Our GF-001 garden fork features a forged carbon steel head (HRC 45-50 hardness) with a natural ash wood handle, 30cm working length, 4 tines — exactly matching your specifications. It comes with CE and GS certification, which are the standard requirements for the German market.",
    "key_data": "Price: $2.50-2.80/pc FOB (depending on order quantity). MOQ: 500 pcs. Lead time: 25 days for 2,000 pcs. For your order volume of 2,000-5,000 pcs, we can offer our best tier pricing.",
    "advantage": "What sets us apart: our heat treatment process achieves HRC 45-50 hardness, which has resulted in zero warranty claims from our European distributors over the past 6 months. We also offer custom color box packaging with your branding.",
    "call_to_action": "I'd be happy to send you a sample (free, you cover shipping) so you can evaluate the quality firsthand. Would you like me to prepare a detailed quotation for 2,000 pcs?",
    "closing": "Looking forward to your reply. Best regards, [Your Name]",
    "full_text": "Hi [Buyer Name], thank you for your RFQ. I understand you're looking for 4-tine garden forks with forged steel head and wooden handle for distribution in Germany, with CE certification and a target price under $3/pc. We can meet all of these requirements. Our GF-001 garden fork features a forged carbon steel head (HRC 45-50 hardness) with a natural ash wood handle, 30cm working length, 4 tines — exactly matching your specifications. It comes with CE and GS certification, which are the standard requirements for the German market. Price: $2.50-2.80/pc FOB (depending on order quantity). MOQ: 500 pcs. Lead time: 25 days for 2,000 pcs. For your order volume of 2,000-5,000 pcs, we can offer our best tier pricing. What sets us apart: our heat treatment process achieves HRC 45-50 hardness, which has resulted in zero warranty claims from our European distributors over the past 6 months. We also offer custom color box packaging with your branding. I'd be happy to send you a sample (free, you cover shipping) so you can evaluate the quality firsthand. Would you like me to prepare a detailed quotation for 2,000 pcs? Looking forward to your reply. Best regards, [Your Name]"
  }
}
```

---

## 使用技巧

1. **逐条回应**：RFQ 中的每一条要求都要回应（满足 / 不满足但可替代）
2. **价格策略**：给范围而不是固定价格，保留谈判空间
3. **认证前置**：如果买家提到认证，要在回复中靠前位置确认
4. **样品引导**：用免费样品降低买家的决策门槛
