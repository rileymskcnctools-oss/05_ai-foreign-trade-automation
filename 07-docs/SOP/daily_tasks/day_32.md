# Day 32 任务：函数编写 - 封装Prompt逻辑

> 日期：Week 5 / Day 4
> 时间：约2小时
> 目标：将6个Prompt模板封装为Python函数

---

## 学习任务（30分钟）

### 为什么封装为函数？

1. 可复用  2. 易维护  3. 可测试  4. 可扩展

---

## 动手任务（60分钟）

### 任务 1：封装6个Prompt函数

创建 `prompts.py`：

```python
def build_seo_title_prompt(product):
    return f"你是外贸SEO专家。为{product.get('product_name_en','N/A')}生成5个SEO标题..."

def build_selling_points_prompt(product):
    return f"你是外贸文案专家。为{product.get('product_name_en','N/A')}生成5条卖点..."

def build_whatsapp_prompt(product): ...
def build_rfq_prompt(product): ...
def build_market_prompt(product, market): ...
def build_alibaba_prompt(product): ...
```

### 任务 2：测试函数

```python
product = {"product_name_en": "Garden Rake", "category": "Digging Tools"}
print(build_seo_title_prompt(product))
```

---

## 总结（30分钟）

### 今日笔记

---

## 检查清单

- [ ] 封装了6个Prompt函数
- [ ] 测试了函数输出
- [ ] 创建了prompts.py
- [ ] 记录了今日笔记

---

## 明天预告

Day 33：数据存储 - JSON输出标准化
