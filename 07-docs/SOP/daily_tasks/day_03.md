# Day 3 任务：SQL进阶 - 子查询与CTE

> 日期：Week 1 / Day 3
> 时间：约1.5小时
> 目标：掌握子查询和CTE（WITH语句），改写项目04的复杂查询

---

## 学习任务（30分钟）

### 子查询 vs CTE

```sql
-- 子查询（嵌套，可读性差）
SELECT * FROM products_clean
WHERE price > (SELECT AVG(price) FROM products_clean);

-- CTE（清晰，可复用）
WITH avg_price AS (
    SELECT AVG(price) as mean_price FROM products_clean
)
SELECT p.* FROM products_clean p, avg_price a
WHERE p.price > a.mean_price;
```

### CTE的优势
1. 可读性更好（从上到下读）
2. 可以定义多个CTE，分步计算
3. 面试中展示CTE比子查询更专业

---

## 动手任务（45分钟）

### 任务 1：用CTE改写查询

```sql
-- Q1: 用CTE计算每个品类的平均价格，然后找出价格高于品类均值的产品
WITH category_avg AS (
    SELECT category, AVG(price) as avg_price
    FROM products_clean
    GROUP BY category
)
-- 补全查询


-- Q2: 用CTE + JOIN计算每个品牌在其品类中的排名
```

### 任务 2：写1个嵌套子查询

```sql
-- 找出评论数高于品类平均评论数的产品
```

---

## 总结（15分钟）

### 今日笔记

1. CTE vs 子查询的理解：

2. 完成的查询：

3. 卡壳的地方：

---

## 检查清单

- [ ] 理解了CTE和子查询的区别
- [ ] 用CTE改写了至少1个查询
- [ ] 写了1个嵌套子查询
- [ ] 记录了今日笔记

---

## 明天预告

Day 4：窗口函数入门
