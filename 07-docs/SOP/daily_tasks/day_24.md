# Day 24 任务：Python基础 - 循环与条件

> 日期：Week 4 / Day 3
> 时间：约2小时
> 目标：掌握for循环、if/elif/else

---

## 学习任务（40分钟）

### for循环

```python
for p in products:
    if p["price"] > 10:
        print(f"{p['name']} 是高端产品")
```

### if/elif/else

```python
def price_tier(price):
    if price < 10:
        return "入门级"
    elif price < 15:
        return "中端"
    else:
        return "高端"
```

---

## 动手任务（50分钟）

### 任务 1：价格分级

```python
products = [
    {"name": "Garden Hoe", "price": 8.99},
    {"name": "Garden Spade", "price": 9.99},
    {"name": "Garden Rake", "price": 11.49},
    {"name": "Garden Fork", "price": 12.99},
    {"name": "Round Point Shovel", "price": 15.99},
]

for p in products:
    if p["price"] < 10:
        tier = "入门级"
    elif p["price"] < 15:
        tier = "中端"
    else:
        tier = "高端"
    print(f"{p['name']}: ${p['price']} -> {tier}")
```

### 任务 2：统计各价格带产品数

### 任务 3：写一个完整小程序

遍历产品，输出名称、价格、等级、是否需要视频。

---

## 总结（30分钟）

### 今日笔记

---

## 检查清单

- [ ] 理解了for循环和if/elif/else
- [ ] 完成了价格分级
- [ ] 编写了小程序
- [ ] 记录了今日笔记

---

## 明天预告

Day 25：pandas入门
