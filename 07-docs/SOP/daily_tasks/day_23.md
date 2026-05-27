# Day 23 任务：Python基础 - 列表与字典

> 日期：Week 4 / Day 2
> 时间：约2小时
> 目标：掌握列表和字典的使用

---

## 学习任务（40分钟）

### 列表

```python
product_ids = ["GF-001", "GS-001", "GR-001"]
product_ids[0]       # "GF-001"
product_ids[-1]      # "GR-001"
product_ids.append("NEW-001")
len(product_ids)
```

### 字典

```python
product = {
    "id": "GF-001",
    "name": "Garden Fork",
    "price": 12.99,
    "material": "Carbon Steel",
}
product["name"]       # "Garden Fork"
product.get("price", 0)
```

---

## 动手任务（50分钟）

### 任务 1：创建产品字典

```python
product = {
    "product_id": "GR-001",
    "product_name_en": "Garden Rake",
    "category": "Digging Tools",
    "material": "Carbon Steel",
    "weight_kg": 0.9,
    "moq": 300,
}
for key, value in product.items():
    print(f"{key}: {value}")
```

### 任务 2：列表操作

```python
# 1. 创建5个产品的列表
# 2. 计算平均价格
# 3. 找出重量最大的产品
# 4. 筛选MOQ >= 500的产品
# 5. 按价格排序
```

### 任务 3：写一个函数

```python
def calc_total_revenue(price, moq):
    return price * moq
```

---

## 总结（30分钟）

### 今日笔记

---

## 检查清单

- [ ] 创建了产品字典
- [ ] 完成了列表操作
- [ ] 编写了函数
- [ ] 记录了今日笔记

---

## 明天预告

Day 24：Python基础 - 循环与条件
