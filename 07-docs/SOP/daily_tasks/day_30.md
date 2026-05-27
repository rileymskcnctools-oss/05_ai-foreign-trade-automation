# Day 30 任务：API与LLM调用基础

> 日期：Week 5 / Day 2
> 时间：约2小时
> 目标：了解如何通过API调用AI

---

## 学习任务（40分钟）

### OpenAI兼容API

```python
import requests
url = "https://api.openai.com/v1/chat/completions"
headers = {"Authorization": "Bearer YOUR_KEY", "Content-Type": "application/json"}
payload = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "你是外贸文案助手"},
        {"role": "user", "content": "为Garden Fork写SEO标题"}
    ],
}
response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(result["choices"][0]["message"]["content"])
```

### 项目05的自动化思路

```
Excel产品数据 -> 读取每行 -> 填入Prompt -> 调用API -> 保存JSON
```

---

## 动手任务（50分钟）

### 任务 1：写Prompt组装函数

```python
def build_seo_prompt(product):
    return f"你是外贸SEO专家。为{product.get('product_name_en','N/A')}生成5个SEO标题..."
```

### 任务 2：研究API调用方式

如果有Qwen API Key，测试一次API调用。如果没有，注册阿里云百炼。

---

## 总结（30分钟）

### 今日笔记

---

## 检查清单

- [ ] 了解了API调用方式
- [ ] 组装了Prompt
- [ ] 尝试了API调用（如有Key）
- [ ] 记录了今日笔记

---

## 明天预告

Day 31：pandas + API数据合并
