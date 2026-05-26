# 国家市场版文案 Prompt

> 用途：为不同目标市场定制产品文案
> 核心原则：同一个产品，不同的市场关注点不同

---

## Prompt 模板

```
你是一个有 10 年经验的 Garden Tools 国际市场专家，熟悉全球各市场的特点。

请为以下产品生成针对 {target_country} 市场的定制化文案。

【产品信息】
- 产品英文名：{product_name_en}
- 产品类别：{category}
- 材质：{material}
- 规格：{length_cm}cm, {weight_kg}kg
- 使用场景：{use_scenario}
- 认证：{certification}

【目标市场：{target_country}】

【市场背景知识】
（以下为 {target_country} 市场的特点，请在文案中体现这些洞察）

{market_info}

【文案规则】
1. 生成以下内容：
   a) 市场版 SEO 标题（2 个）
      - 融入当地常用搜索词
      - 符合当地买家习惯的表达方式
   b) 市场版卖点描述（3 条）
      - 突出该市场最关心的特点
      - 用当地人能共鸣的表达
   c) 市场开发话术（1 段，150-250 词）
      - 针对 {target_country} 进口商/批发商
      - 提及市场相关痛点或趋势
   d) 市场版 FAQ（3 个问答）
      - 该市场买家最常问的问题
2. 语言：英文
3. 要体现你对该市场的了解，不是简单改几个词

【输出格式】
请用 JSON 格式输出：
{
  "product_id": "{product_id}",
  "product_name": "{product_name_en}",
  "target_market": "{target_country}",
  "seo_titles": ["标题1", "标题2"],
  "selling_points": [
    {
      "focus": "该市场关注的维度",
      "text": "卖点文案"
    },
    ...
  ],
  "market_script": "针对该市场的开发话术",
  "faq": [
    {
      "question": "买家常见问题",
      "answer": "你的回答"
    },
    ...
  ]
}
```

---

## 实际使用示例

```
你是一个有 10 年经验的 Garden Tools 国际市场专家，熟悉全球各市场的特点。

请为以下产品生成针对 Nigeria 市场的定制化文案。

【产品信息】
- 产品英文名：Garden Fork
- 产品类别：Digging Tools
- 材质：Carbon Steel + Ash Wood
- 规格：30cm, 0.8kg
- 使用场景：Garden soil turning, compost mixing, farming
- 认证：CE

【目标市场：Nigeria】

【市场背景知识】
- 农业是尼日利亚主要经济支柱，大量人口从事农业
- 土壤类型多样，北部多沙土，南部多黏土和壤土
- 雨季和旱季分明，工具需要耐候性
- 价格敏感度高，但愿意为耐用性买单
- 进口工具主要来自中国和印度
- 批发商集中在拉各斯（Lagos）和卡诺（Kano）
- 偏好坚固耐用的工具，不太关注外观设计
- 常用搜索词：farm fork, digging fork, heavy duty fork, agricultural tools

【文案规则】
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
  "target_market": "Nigeria",
  "seo_titles": [
    "Heavy Duty Farm Fork for Nigerian Agriculture — Carbon Steel 4-Tine Digging Tool",
    "Agricultural Digging Fork for Hard Soil — 30cm Steel Fork with Wooden Handle Nigeria"
  ],
  "selling_points": [
    {
      "focus": "耐用性",
      "text": "HRC 45-50 heat-treated carbon steel tines withstand the tough, compacted laterite soils common across Nigeria's farming regions. Built for daily heavy use in both rainy and dry seasons without bending."
    },
    {
      "focus": "性价比",
      "text": "Factory-direct pricing means you get European-quality durability at a price point that works for the Nigerian market. Our distributors in West Africa report 40% better margin compared to Indian alternatives."
    },
    {
      "focus": "适用性",
      "text": "The 4-tine configuration is versatile enough for turning clay soils in the south, breaking sandy soils in the north, and mixing compost — making it a practical all-in-one tool for diverse Nigerian farming conditions."
    }
  ],
  "market_script": "Hi! We've been supplying garden and farm forks to distributors across West Africa for 8 years, and Nigeria is our fastest-growing market. Our carbon steel garden fork is specifically designed for the heavy soil conditions common in Nigerian farming — HRC 45-50 hardness means it doesn't bend even in compacted laterite. MOQ starts at just 500 pcs, which is perfect for testing the market, and our Lagos-based partners tell us the 30cm size is the most popular. Would you like me to send you a sample and wholesale pricing for the Nigerian market?",
  "faq": [
    {
      "question": "Can this handle the hard soil in northern Nigeria?",
      "answer": "Absolutely. The HRC 45-50 heat-treated steel is specifically designed for tough, compacted soils. Our customers in Kano and Kaduna use it daily for breaking hard ground during the dry season preparation."
    },
    {
      "question": "What is the minimum order and delivery time to Lagos?",
      "answer": "MOQ is 500 pcs. Standard lead time is 25 days production plus shipping. To Lagos port, shipping typically takes 30-35 days. We can also arrange delivery to your Lagos warehouse through our forwarding partner."
    },
    {
      "question": "Do you offer any warranty or after-sales support?",
      "answer": "We offer a 12-month quality guarantee. In practice, our Nigerian distributors report less than 0.5% defect rate. If any quality issue arises, we provide free replacement in the next shipment."
    }
  ]
}
```

---

## 市场知识注入方法

在 `{market_info}` 部分，你可以从市场知识库中复制对应国家的信息：

### 快速市场知识模板

```
【市场知识速查】

🇳🇬 Nigeria（尼日利亚）：
  - 农业大国，价格敏感但愿为耐用买单
  - 土壤：北部沙土，南部黏土/壤土
  - 偏好：坚固耐用 > 外观
  - 认证：无强制要求
  - 渠道：Lagos, Kano 批发市场
  - 竞品：印度廉价工具
  - 搜索词：farm fork, heavy duty, agricultural tools

🇩🇪 Germany（德国）：
  - 高质量要求，注重环保认证
  - 强制认证：CE, GS
  - 偏好：人体工学、品牌、可持续性
  - 渠道：Garden centers, online (Amazon.de)
  - 竞品：Fiskars, Gardena
  - 搜索词：Gartenhacke, Gartengabel, Qualitätswerkzeug
  - 季节：春季（3-5月）为旺季

🇰🇪 Kenya（肯尼亚）：
  - 农业为主，中小型农场多
  - 偏好：多功能、轻便
  - 认证：无强制，KEBS 推荐
  - 渠道：Nairobi, Mombasa
  - 搜索词：farm tools, garden fork Kenya, agricultural equipment
  - 竞品：本地铁匠工具、印度进口

🇧🇷 Brazil（巴西）：
  - 大规模农业 + 城市园艺
  - 偏好：大尺寸、重型工具
  - 认证：INMETRO（部分产品）
  - 渠道：São Paulo, home centers
  - 竞品：Tramontina（本土品牌强势）
  - 搜索词：enxada, garfo de jardim, ferramentas agrícolas

🇿🇦 South Africa（南非）：
  - 成熟市场，质量标准高
  - 偏好：品牌、耐用性
  - 认证：SABS 推荐
  - 渠道：Builders Warehouse, outdoor stores
  - 竞品：Local brands, European imports
  - 搜索词：garden fork, spade, garden tools South Africa
```

---

## 使用技巧

1. **市场知识越具体，输出越好**：花 5 分钟录入市场知识，AI 生成的内容会精准很多
2. **本地搜索词**：每个市场的搜索词不同，要单独提供
3. **竞品对标**：提到当地竞品，AI 会自动调整定位策略
4. **持续积累**：每次使用后，把新的市场洞察加到市场知识库中
