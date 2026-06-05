# WhatsApp 开发话术 Prompt

> 用途：生成面向不同类型客户的 WhatsApp 开发消息
> 核心原则：短、有价值、有行动引导

---

## Prompt 模板

```
你是一个有 10 年经验的 Garden Tools 外贸业务员，擅长用 WhatsApp 开发客户。
你的风格：专业、简洁、像朋友聊天一样自然，不像群发广告。

请为以下产品生成 3 版 WhatsApp 开发话术。

【产品信息】
- 产品英文名：${product_name_en}
- 产品类别：${category}
- 核心卖点：${selling_angle}
- 材质：${material}
- MOQ：${moq} 件
- 交货期：${lead_time_days} 天
- 包装：${packaging_type}

【目标客户】
- 客户类型：${customer_type}（如：wholesaler, retailer, distributor, garden center）
- 目标市场：${target_market}（如：Nigeria, Germany, Brazil）

【话术规则】
1. 每版话术 3-5 句话，不超过 500 字符
2. 结构：
   - 开场：自然的打招呼 + 表明来意（不是 "Dear Sir/Madam"）
   - 价值：一句话说明产品能给他带来什么好处
   - 证据：一个具体的数据或优势支撑
   - 行动：一个低压力的下一步建议（不是 "Please order now"）
3. 3 版话术有不同的开场方式：
   - 版本A：直接介绍产品型
   - 版本B：问题导向型（先问他的需求）
   - 版本C：推荐/案例型（提及其他客户的反馈）
4. 语气：口语化、自然、专业
5. 语言：英文
6. 不要像群发广告！要像一对一的消息

【输出格式】
请用 JSON 格式输出：
{
  "product_id": "${product_id}",
  "product_name": "${product_name_en}",
  "customer_type": "{customer_type}",
  "target_market": "{target_market}",
  "whatsapp_scripts": [
    {
      "version": "A",
      "style": "直接介绍产品型",
      "subject_line": "一句话摘要（用于预览）",
      "message": "完整话术内容"
    },
    {
      "version": "B",
      "style": "问题导向型",
      "subject_line": "一句话摘要",
      "message": "完整话术内容"
    },
    {
      "version": "C",
      "style": "推荐/案例型",
      "subject_line": "一句话摘要",
      "message": "完整话术内容"
    }
  ]
}
```

---

## 实际使用示例

```
你是一个有 10 年经验的 Garden Tools 外贸业务员，擅长用 WhatsApp 开发客户。

请为以下产品生成 3 版 WhatsApp 开发话术。

【产品信息】
- 产品英文名：Garden Fork
- 产品类别：Digging Tools
- 核心卖点：Extra-strong carbon steel tines, ergonomic ash wood handle
- 材质：Carbon Steel + Ash Wood
- MOQ：500 件
- 交货期：25 天
- 包装：Color Box

【目标客户】
- 客户类型：wholesaler
- 目标市场：Nigeria

【话术规则】
（同上）

【输出格式】
（同上）
```

---

## 预期输出示例

```json
{
  "product_id": "GF-001",
  "product_name": "Garden Fork",
  "customer_type": "wholesaler",
  "target_market": "Nigeria",
  "whatsapp_scripts": [
    {
      "version": "A",
      "style": "直接介绍产品型",
      "subject_line": "Heavy-duty garden fork from manufacturer",
      "message": "Hi! I'm from [company name], we manufacture garden tools in China. Our 4-tine garden fork with carbon steel head is one of our top sellers in West Africa — MOQ just 500pcs, 25-day delivery. The ash wood handle and HRC 45-50 hardness make it ideal for tough soil conditions. Would you like me to send you the spec sheet and pricing?"
    },
    {
      "version": "B",
      "style": "问题导向型",
      "subject_line": "Quick question about your garden tool range",
      "message": "Hey! Quick question — are you currently sourcing garden forks for the Nigerian market? We just launched a new model with reinforced carbon steel tines specifically designed for heavy soil, and the feedback from our East African partners has been great. If it fits your range, I'd be happy to share samples. No pressure at all — just thought it might be worth a look."
    },
    {
      "version": "C",
      "style": "推荐/案例型",
      "subject_line": "What our Kenya distributor said about this fork",
      "message": "Hi there! Our distributor in Kenya told us the #1 complaint from their garden fork customers was bent tines after a few months. So we upgraded our steel treatment to HRC 45-50 hardness — same price, much stronger. It's been 6 months and zero warranty claims so far. I thought this might be relevant for your market too. Want me to send details?"
    }
  ]
}
```

---

## 使用技巧

1. **开头要自然**：用 "Hi" / "Hey" 代替 "Dear Sir/Madam"
2. **有具体数据**："HRC 45-50" "500pcs" "25 days" 增加可信度
3. **低压力结尾**：用 "Would you like..." "Want me to..." 代替 "Please order"
4. **版本 C 最有效**：案例型话术通常回复率最高，因为提供了社会证明
