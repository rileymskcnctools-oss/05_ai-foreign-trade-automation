# Day 4 任务：窗口函数入门

> 日期：Week 1 / Day 4
> 时间：约2小时
> 目标：掌握SQL窗口函数，用于排名、累计计算等分析

---

## 学习任务（40分钟）

### 常用窗口函数

```sql
-- ROW_NUMBER(): 给每行分配唯一序号
SELECT product_name, price,
       ROW_NUMBER() OVER (ORDER BY price DESC) as price_rank
FROM products_clean;

-- RANK(): 相同值相同排名，跳号
SELECT brand, avg_rating,
       RANK() OVER (ORDER BY avg_rating DESC) as rating_rank
FROM brand_stats;

-- NTILE(4): 四分位分组
SELECT product_name, price,
       NTILE(4) OVER (ORDER BY price) as price_quartile
FROM products_clean;
```

---

## 动手任务（50分钟）

### 任务 1：窗口函数练习

```sql
-- Q1: 每个品类中价格最高的3个产品（ROW_NUMBER + PARTITION BY）
SELECT * FROM (
    SELECT product_name, category, price,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) as rn
    FROM products_clean
) WHERE rn <= 3;

-- Q2: 品牌按平均评分排名

-- Q3: 把产品按价格分成4个等级，统计每个等级的产品数
```

---

## 总结（30分钟）

### 今日笔记

1. 掌握的窗口函数：

2. PARTITION BY 的理解：

3. 完成的查询：

---

## 检查清单

- [ ] 理解了ROW_NUMBER(), RANK(), NTILE()
- [ ] 完成了3个窗口函数查询
- [ ] 记录了今日笔记

---

## 明天预告

Day 5：项目04 - SQL结果导出
