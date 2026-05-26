# 五点描述 / 产品卖点 Prompt

> 用途：生成 B2B 买家角度的产品卖点
> 核心原则：Feature（特点）→ Benefit（好处）的转换

---

## Prompt 模板

```
你是一个有 10 年经验的 Garden Tools 产品开发专家，同时也是 B2B 销售文案高手。

请为以下产品生成 5 个核心卖点。

【产品信息】
- 产品英文名：{product_name_en}
- 产品类别：{category}
- 材质：{material}
- 手柄材质：{handle_material}
- 规格：{length_cm}cm, {weight_kg}kg, {tine_count}{unit}
- 硬度：{hardness}
- 表面处理：{surface_treatment}
- 使用场景：{use_scenario}
- 核心卖点方向：{selling_angle}

【B2B 买家关注点参考】
- 批发商：价格竞争力、MOQ、交期、包装、复购率
- 零售商：产品外观、展示性、利润空间、消费者卖点
- 终端用户：耐用性、手感、功能、性价比

【卖点规则】
1. 每个卖点用 "Feature → Benefit" 结构写
   - Feature（是什么）：产品有什么特点
   - Benefit（对买家有什么好处）：这个特点能给买家/用户带来什么价值
2. 格式：每条 2-3 句话
   - 第一句：Feature（简洁描述特点）
   - 第二句：Benefit（转换成买家语言的价值）
   - 可选第三句：数据/证据支撑
3. 5 个卖点覆盖不同维度：
   - 卖点1：材质与耐用性
   - 卖点2：人体工学与使用体验
   - 卖点3：工艺与质量
   - 卖点4：适用场景与多功能
   - 卖点5：包装与商业价值（MOQ/交期/认证）
4. 语言：英文
5. 面向 B2B 买家（进口商、批发商、零售商），不是终端消费者

【输出格式】
请用 JSON 格式输出：
{
  "product_id": "{product_id}",
  "product_name": "{product_name_en}",
  "selling_points": [
    {
      "dimension": "材质与耐用性",
      "feature": "特点描述",
      "benefit": "买家价值",
      "full_text": "完整的卖点文案（2-3句话）"
    },
    ...
  ],
  "short_summary": "一句话总结产品核心优势（15词以内）"
}
```

---

## 实际使用示例

```
你是一个有 10 年经验的 Garden Tools 产品开发专家，同时也是 B2B 销售文案高手。

请为以下产品生成 5 个核心卖点。

【产品信息】
- 产品英文名：Garden Fork
- 产品类别：Digging Tools
- 材质：Carbon Steel + Ash Wood
- 手柄材质：Ash Wood
- 规格：30cm, 0.8kg, 4齿
- 硬度：HRC 45-50
- 表面处理：Polished + Lacquered
- 使用场景：Garden soil turning, compost mixing
- 核心卖点方向：Extra-strong tines, ergonomic handle

【卖点规则】
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
  "selling_points": [
    {
      "dimension": "材质与耐用性",
      "feature": "High-carbon steel tines with HRC 45-50 hardness",
      "benefit": "Withstands heavy-duty soil penetration and rocky conditions without bending, reducing replacement costs for distributors",
      "full_text": "Forged from high-carbon steel with HRC 45-50 heat treatment hardness, the tines penetrate hard soil and handle rocky conditions without bending or breaking. This means fewer warranty claims and higher repeat orders from your customers."
    },
    {
      "dimension": "人体工学与使用体验",
      "feature": "Ergonomic ash wood handle, 0.8kg lightweight design",
      "benefit": "Reduces user fatigue during extended work sessions, making it ideal for professional gardeners and farmers",
      "full_text": "The naturally curved ash wood handle provides a comfortable, non-slip grip that reduces hand fatigue. At just 0.8kg, users can work longer without strain — a key selling point for end consumers that drives repeat purchases."
    },
    {
      "dimension": "工艺与质量",
      "feature": "Polished and lacquered surface treatment",
      "benefit": "Double-layer rust protection extends product life in humid climates, reducing after-sales issues",
      "full_text": "Each fork head undergoes a dual treatment process — precision polishing followed by lacquer coating — creating a two-layer barrier against rust and corrosion. This is especially valued in tropical and coastal markets, reducing warranty returns by up to 60%."
    },
    {
      "dimension": "适用场景与多功能",
      "feature": "4-tine design, 30cm working length",
      "benefit": "Versatile for soil turning, compost mixing, and lawn aeration — one tool for multiple tasks",
      "full_text": "The optimized 4-tine configuration with 30cm working length handles multiple tasks: turning garden soil, mixing compost, aerating lawns, and breaking up clay. Retailers benefit from a single SKU that serves diverse customer needs."
    },
    {
      "dimension": "包装与商业价值",
      "feature": "Color box packaging, MOQ 500pcs, 25-day lead time",
      "benefit": "Shelf-ready packaging reduces retailer prep time, flexible MOQ supports new market testing",
      "full_text": "Comes in full-color printed retail packaging — ready to display without additional prep. With an MOQ of just 500 units and a 25-day production lead time, you can test new markets with low risk and replenish quickly during peak season."
    }
  ],
  "short_summary": "Heavy-duty carbon steel fork with ergonomic ash handle for professional-grade garden work."
}
```

---

## 使用技巧

1. **数据支撑**：有具体数字的卖点更有说服力（"HRC 45-50" 比 "very hard" 好）
2. **买家语言**：说买家关心的事，不是工厂关心的事
   - ❌ "我们采用先进的热处理工艺"
   - ✅ "热处理硬度 HRC 45-50，减少 60% 售后问题"
3. **维度覆盖**：确保 5 个卖点不重复，覆盖不同关注点
