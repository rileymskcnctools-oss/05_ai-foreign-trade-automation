# Day 10 任务：DAX入门 - 计算列与度量值

> 日期：Week 2 / Day 3
> 时间：约2小时
> 目标：创建DAX度量值

---

## 学习任务（30分钟）

### 计算列 vs 度量值

| 特性 | 计算列 | 度量值 |
|------|--------|--------|
| 存储 | 存在表中 | 实时计算 |
| 内存 | 占用 | 不占用 |
| 推荐 | 少用 | 多用 |

### 项目04需要的度量值

```dax
Product Count = COUNTROWS(Products)
Avg Price = AVERAGE(Products[price])
Avg Rating = AVERAGE(Products[rating])
Total Reviews = SUM(Products[review_count])
Best Seller Count = CALCULATE([Product Count], Products[is_best_seller]=TRUE)
```

---

## 动手任务（60分钟）

### 任务 1：创建5个基础度量值

```dax
1. Product Count = COUNTROWS(Products)
2. Avg Price = AVERAGE(Products[price])
3. Avg Rating = AVERAGE(Products[rating])
4. Total Reviews = SUM(Products[review_count])
5. Best Seller Count = ...
```

### 任务 2：创建3个高级度量值

```dax
Best Seller Rate = DIVIDE([Best Seller Count], [Product Count])
FBA Ratio = DIVIDE(CALCULATE([Product Count], Products[is_prime]=TRUE), [Product Count])
Has Video Count = CALCULATE([Product Count], Products[has_video]=TRUE)
```

### 任务 3：验证度量值

```
Product Count 应该显示：1000
Avg Price 应该显示：约$82
Avg Rating 应该显示：约4.35
```

---

## 总结（30分钟）

### 今日笔记

1. 创建的度量值清单：

2. 计算列 vs 度量值的理解：

---

## 检查清单

- [ ] 创建了5个基础度量值
- [ ] 创建了3个高级度量值
- [ ] 验证了度量值
- [ ] 记录了今日笔记

---

## 明天预告

Day 11：DAX进阶 - CALCULATE + FILTER
