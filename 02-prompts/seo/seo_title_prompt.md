# SEO 标题生成 Prompt

> 用途：为阿里国际站产品生成 SEO 优化标题
> 规则：128 字符以内，关键词前置，自然可读

---

## Prompt 模板

```
你是一个有 10 年经验的阿里国际站 SEO 专家，专门做 Garden Tools / Farm Tools 品类。

请为以下产品生成 5 个 SEO 标题。

【产品信息】
- 产品英文名：${product_name_en}
- 产品类别：${category} / ${sub_category}
- 材质：${material}
- 核心规格：${specifications}（如：${tine_count}齿, ${length_cm}cm, ${weight_kg}kg）
- 表面处理：${surface_treatment}
- 使用场景：${use_scenario}

【目标关键词】
${target_keywords}

【标题规则】
1. 每个标题不超过 128 个字符
2. 最重要的关键词放在标题最前面
3. 标题要包含：核心关键词 + 材质/规格 + 使用场景/优势
4. 5 个标题要有不同侧重点：
   - 标题1：侧重核心大词（搜索量最大的词）
   - 标题2：侧重材质优势
   - 标题3：侧重使用场景
   - 标题4：侧重规格参数
   - 标题5：长尾精准词
5. 不要用 "Hot Sale""Best Price" 等无意义词
6. 语言：英文

【输出格式】
请用 JSON 格式输出：
{
  "product_id": "${product_id}",
  "product_name": "${product_name_en}",
  "seo_titles": [
    {
      "variant": 1,
      "focus": "核心大词",
      "title": "标题文字"
    },
    {
      "variant": 2,
      "focus": "材质优势",
      "title": "标题文字"
    },
    ...
  ]
}
```

---

## 实际使用示例

把 `{大括号}` 替换成实际数据后：

```
你是一个有 10 年经验的阿里国际站 SEO 专家，专门做 Garden Tools / Farm Tools 品类。

请为以下产品生成 5 个 SEO 标题。

【产品信息】
- 产品英文名：Garden Fork
- 产品类别：Digging Tools / Forks
- 材质：Carbon Steel + Ash Wood
- 核心规格：4齿, 30cm, 0.8kg
- 表面处理：Polished + Lacquered
- 使用场景：Garden soil turning, compost mixing

【目标关键词】
garden fork, digging fork, steel fork

【标题规则】
1. 每个标题不超过 128 个字符
2. 最重要的关键词放在标题最前面
3. 标题要包含：核心关键词 + 材质/规格 + 使用场景/优势
4. 5 个标题要有不同侧重点：
   - 标题1：侧重核心大词
   - 标题2：侧重材质优势
   - 标题3：侧重使用场景
   - 标题4：侧重规格参数
   - 标题5：长尾精准词
5. 不要用 "Hot Sale""Best Price" 等无意义词
6. 语言：英文

【输出格式】
请用 JSON 格式输出：
{
  "product_id": "GF-001",
  "product_name": "Garden Fork",
  "seo_titles": [
    ...
  ]
}
```

---

## 预期输出示例

```json
{
  "product_id": "GF-001",
  "product_name": "Garden Fork",
  "seo_titles": [
    {
      "variant": 1,
      "focus": "核心大词",
      "title": "Garden Fork Heavy Duty Digging Fork with 4 Steel Tines for Garden Soil Cultivation"
    },
    {
      "variant": 2,
      "focus": "材质优势",
      "title": "Carbon Steel Garden Fork with Ash Wood Handle, Rust Resistant Digging Fork for Farming"
    },
    {
      "variant": 3,
      "focus": "使用场景",
      "title": "4-Tine Garden Fork for Soil Turning Compost Mixing Lawn Aeration with Ergonomic Handle"
    },
    {
      "variant": 4,
      "focus": "规格参数",
      "title": "30cm 4-Tine Steel Garden Fork 0.8kg Lightweight Digging Tool with Polished Finish"
    },
    {
      "variant": 5,
      "focus": "长尾精准词",
      "title": "Heavy Duty Carbon Steel Garden Digging Fork 4 Tines Hardwood Handle for Professional Gardeners"
    }
  ]
}
```

---

## 使用技巧

1. **关键词选择**：把搜索量最大的词放在最前面
2. **规格数据**：有具体数字的标题点击率更高（"30cm" 比 "long" 好）
3. **避免重复**：5 个标题的关键词排列不要完全一样
4. **检查长度**：生成后用字符计数工具检查是否超过 128
