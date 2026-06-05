# 阿里国际站详情页 Prompt

> 用途：生成阿里国际站产品详情页文案
> 结构：Banner → 卖点 → 参数 → 工厂 → FAQ

---

## Prompt 模板

```
你是一个有 10 年经验的阿里国际站详情页设计师，专门做 Garden Tools 品类。
你知道什么样的详情页能提高转化率。

请为以下产品生成一份完整的阿里国际站详情页文案。

【产品信息】
- 产品英文名：${product_name_en}
- 产品编号：${product_id}
- 产品类别：${category}
- 材质：${material}
- 手柄材质：${handle_material}
- 规格：${length_cm}cm, ${weight_kg}kg, ${tine_count}${unit}
- 硬度：${hardness}
- 表面处理：${surface_treatment}
- 使用场景：${use_scenario}
- MOQ：${moq}
- 包装：${packaging_type}
- 交货期：${lead_time_days} 天
- 认证：${certification}
- 核心卖点：${selling_angle}

【工厂信息】
- 工厂经验：${factory_years} 年
- 年产能：${annual_capacity}
- 出口市场：${export_markets}
- 工厂面积：${factory_size}
- 员工数：${employee_count}
- 认证：${factory_certifications}

【详情页结构】
请按以下结构生成内容：

Section 1: Banner / Hero
  - 主标题（10-15 词，突出核心卖点）
  - 副标题（补充说明）
  - 3 个核心标签（如 "Factory Direct" "CE Certified" "MOQ 500"）

Section 2: Product Highlights (5 个卖点)
  - 每个卖点包含：标题 + 2-3 句话描述
  - 配合图标建议（如 ✓ 图标、🏆 图标）

Section 3: Specifications (规格参数表)
  - 用表格列出所有技术参数
  - 格式：参数名 | 参数值

Section 4: Product Applications (使用场景)
  - 3-4 个使用场景描述
  - 每个场景配一个简短说明

Section 5: Why Choose Us (工厂优势)
  - 4 个工厂优势点
  - 用数据说话（年份、产能、认证数量等）

Section 6: Packaging & Shipping (包装与物流)
  - 包装方式描述
  - 装箱信息（每箱数量、外箱尺寸、毛重）
  - 交货期说明

Section 7: FAQ (常见问题)
  - 5 个买家最常问的问题和回答

【规则】
1. 所有内容用英文
2. 面向 B2B 买家（进口商、批发商、零售商）
3. 每个 section 之间用分隔线分隔
4. 图片占位符用 [Image: 描述] 标注
5. 格式：Markdown 格式，方便直接复制到阿里后台

【输出格式】
请直接输出 Markdown 格式的详情页内容，按以上 Section 顺序排列。
```

---

## 实际使用示例

```
你是一个有 10 年经验的阿里国际站详情页设计师...

【产品信息】
- 产品英文名：Garden Fork
- 产品编号：GF-001
- 产品类别：Digging Tools
- 材质：Carbon Steel + Ash Wood
- 手柄材质：Ash Wood
- 规格：30cm, 0.8kg, 4齿
- 硬度：HRC 45-50
- 表面处理：Polished + Lacquered
- 使用场景：Garden soil turning, compost mixing
- MOQ：500
- 包装：Color Box
- 交货期：25 天
- 认证：CE, GS
- 核心卖点：Extra-strong tines, ergonomic handle

【工厂信息】
- 工厂经验：15 年
- 年产能：500,000 pcs
- 出口市场：Europe, Africa, South America
- 工厂面积：10,000 sqm
- 员工数：200+
- 认证：ISO 9001, BSCI, CE, GS

【详情页结构】
（同上）

【输出格式】
（同上）
```

---

## 使用技巧

1. **图片占位符**：用 `[Image: 描述]` 标注需要配图的位置，后期让设计补图
2. **数据化**：工厂优势要用具体数字（"15年经验" 比 "多年经验" 好）
3. **SEO**：详情页中自然融入关键词，有助于阿里搜索排名
4. **移动端适配**：内容分段要短，方便手机端阅读
