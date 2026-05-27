# Day 33 任务：数据存储 - JSON输出标准化

> 日期：Week 5 / Day 5
> 时间：约2小时
> 目标：定义JSON Schema，确保输出格式一致

---

## 学习任务（30分钟）

### JSON操作

```python
import json
data = {"name": "Garden Rake", "price": 11.49}
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

---

## 动手任务（60分钟）

### 任务 1：定义输出结构

```python
def create_empty_output(product_id, product_name):
    return {
        "product_id": product_id,
        "product_name": product_name,
        "generated_at": "",
        "seo_titles": [],
        "selling_points": [],
        "whatsapp_scripts": {},
        "rfq_reply": "",
        "alibaba_detail": "",
        "market_versions": {},
    }
```

### 任务 2：读取项目05已有输出

```python
import json
with open(r"C:\Users\Administrator\Desktop\code\05_AI-外贸自动化系统\05-输出结果\GR-001\seo_titles.json", "r", encoding="utf-8") as f:
    data = json.load(f)
```

### 任务 3：写保存函数

```python
def save_product_output(output, base_dir):
    product_id = output["product_id"]
    product_dir = os.path.join(base_dir, product_id)
    os.makedirs(product_dir, exist_ok=True)
    with open(os.path.join(product_dir, "output.json"), "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
```

---

## 总结（30分钟）

### 今日笔记

---

## 检查清单

- [ ] 定义了标准JSON结构
- [ ] 读取了已有输出
- [ ] 编写了保存函数
- [ ] 记录了今日笔记

---

## 明天预告

Day 34：项目05推进 - 写自动化脚本v1
