# Day 11 任务：DAX进阶 - CALCULATE与FILTER

> 日期：Week 2 / Day 4
> 时间：约2小时
> 目标：掌握CALCULATE函数，创建条件度量值

---

## 学习任务（30分钟）

### CALCULATE - DAX最重要的函数

```dax
CALCULATE(度量值, 筛选条件)

-- 例：$50-100价格带的Best Seller率
MidRange BS Rate = CALCULATE(
    [Best Seller Rate],
    Products[price] >= 50 && Products[price] < 100
)
```

---

## 动手任务（60分钟）

### 任务 1：写3个条件度量值

```dax
-- 1. $50-100价格带的产品数
Mid Range Products = CALCULATE([Product Count], Products[price] >= 50 && Products[price] < 100)

-- 2. 有视频产品的平均评论量
Video Avg Reviews = CALCULATE(AVERAGE(Products[review_count]), Products[has_video] = TRUE)

-- 3. FBA产品的平均价格
FBA Avg Price = CALCULATE([Avg Price], Products[is_prime] = TRUE)
```

### 任务 2：验证条件度量值

```
Mid Range Products: 约202
Video Avg Reviews: 约2559
FBA Avg Price: 约$84
```

---

## 总结（30分钟）

### 今日笔记

1. 创建的条件度量值：

2. CALCULATE的理解：

---

## 检查清单

- [ ] 创建了3个条件度量值
- [ ] 验证了度量值
- [ ] 记录了今日笔记

---

## 明天预告

Day 12：可视化实操 - Page 1 市场总览
