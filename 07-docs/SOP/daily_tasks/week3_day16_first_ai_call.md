# Day 16: 第一次 AI API 调用

> 日期: Week 3 / Day 16
> 时间: 约 1 小时
> 目标: 成功用 Python 调用 Qwen API, 拿到 AI 返回的第一个 SEO 标题

---

## 学习任务 (20 分钟)

### 前置检查
确认 `config/.env` 中有 QWEN_API_KEY:
```bash
cat config/.env
```
如果没有, 需要先去阿里云 DashScope 平台申请 API Key。

### API 调用三要素回顾
1. **URL (终点站)**: `https://dashscope.aliyuncs.com/compatible-mode/v1`
2. **身份令牌**: `Bearer {api_key}`
3. **数据包裹**: model + messages + temperature

---

## 动手任务 (40 分钟)

### 任务 1: 最简 AI 调用 (复制运行)
创建文件 `03-workflows/python/day16_first_ai_call.py`:

```python
"""
Day 16: 第一次 AI API 调用
目标: 用 Qwen 生成一个 SEO 标题
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.llm_client import LLMClient

# 1. 创建 LLM 客户端 (默认用 Qwen)
client = LLMClient(provider="qwen")

# 2. 写一个简单的 prompt
prompt = """
请为以下产品生成 1 个 SEO 标题:
产品: Garden Fork (园艺叉)
材质: Carbon Steel + Ash Wood
规格: 110cm, 2.8kg
用途: Digging and soil preparation
标题要求: 不超过 128 字符, 包含核心关键词
"""

# 3. 调用 AI
print("正在调用 Qwen API...")
response = client.chat(prompt, max_tokens=200, temperature=0.7)

print("\n=== AI 返回结果 ===")
print(response)
print("\n调用成功!")
```

运行:
```bash
cd /c/Users/Administrator/Desktop/code/05_ai-foreign-trade-automation
python 03-workflows/python/day16_first_ai_call.py
```

### 任务 2: 用 Prompt 模板调用 AI
创建文件 `03-workflows/python/day16_prompt_template_call.py`:

```python
"""
Day 16: 用 Prompt 模板 + 真实数据库数据调用 AI
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.database import FTDatabase
from src.core.llm_client import LLMClient
from src.utils.prompts import load_prompt, fill_prompt, build_product_data

# 1. 从数据库拿产品数据
db = FTDatabase()
product = db.product_get("GF-001")
print(f"产品: {product['product_name_en']}")
print(f"类别: {product['category']}")

# 2. 构建模板数据
data = build_product_data(product)
print(f"模板变量数量: {len(data)}")

# 3. 加载并填充 Prompt 模板
template = load_prompt("seo/alibaba_title")
filled = fill_prompt(template, data)
print(f"\n填充后的 Prompt (前200字符):\n{filled[:200]}...")

# 4. 调用 AI
llm = LLMClient(scenario="seo_content")
print("\n正在调用 AI 生成 SEO 标题...")
response = llm.chat(filled, max_tokens=500, temperature=0.7)

print("\n=== AI 生成的 SEO 标题 ===")
print(response)

db.close()
print("\n完成!")
```

运行:
```bash
python 03-workflows/python/day16_prompt_template_call.py
```

---

## 总结 (10 分钟)

记录以下内容:
1. AI 返回的 SEO 标题是什么?
2. 用 Prompt 模板和直接写 prompt, 输出质量有区别吗?
3. 调用过程中有没有报错? 如果有, 错误是什么, 怎么解决的?

---

## 检查清单
- [ ] `day16_first_ai_call.py` 运行成功, 拿到 AI 返回
- [ ] `day16_prompt_template_call.py` 运行成功, 用真实数据生成标题
- [ ] 理解了 `LLMClient` 的 `provider` 和 `scenario` 参数
- [ ] 记录了 AI 返回的结果

---

## 明天预告
Day 17: 深入理解 Prompt 工程, 学会如何设计更好的 Prompt 模板
