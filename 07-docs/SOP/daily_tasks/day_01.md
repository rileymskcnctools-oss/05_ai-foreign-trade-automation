# Day 1 任务：SQL复习 + 项目04数据验证入门

> 日期：Week 1 / Day 1
> 时间：约2小时
> 目标：复习SQL基础查询，开始验证项目04数据质量

---

## 学习任务（40分钟）

### SQL SELECT / WHERE / GROUP BY 回顾

```sql
-- 基础查询
SELECT product_id, product_name, price, rating
FROM products_clean
WHERE category = 'Carbide Inserts';

-- 聚合查询
SELECT category,
       COUNT(*) as product_count,
       AVG(price) as avg_price,
       AVG(rating) as avg_rating
FROM products_clean
GROUP BY category
ORDER BY avg_price DESC;
```

### 项目04数据概览

| 数据集             | 行数    | 说明                      |
| --------------- | ----- | ----------------------- |
| products.csv    | 1,000 | 产品目录（价格、评分、Listing质量指标） |
| reviews.csv     | 629   | 用户评论（情感、验证、国家数据）        |
| competitors.csv | 787   | 竞品关联数据                  |

---

## 动手任务（50分钟）

### 任务 1：检查项目04清洗后数据

打开项目04文件夹，检查以下文件是否存在且非空：

```
02_data_cleaning/products_clean.csv
02_data_cleaning/reviews_clean.csv
02_data_cleaning/competitors_clean.csv
```

记录检查结果：

```
products_clean.csv: ___ 行, ___ 列
reviews_clean.csv: ___ 行, ___ 列
competitors_clean.csv: ___ 行, ___ 列
```

### 任务 2：写5个SQL查询

```sql
-- Q1: 统计每个品类的产品数
-- Q2: 找出价格最高的5个产品
-- Q3: 计算每个品牌的产品数量和平均评分
-- Q4: 统计FBA vs FBM的产品数量和占比
-- Q5: 按价格区间分组（CASE WHEN），统计每组的Best Seller数量
```

---

## 总结（30分钟）

### 今日笔记

1. 数据检查结果：

2. 完成的SQL查询：

3. 卡壳的地方：

4. 明天的准备：

---

## 检查清单

- [ ] 检查了项目04清洗后数据的完整性
- [ ] 完成了5个SQL查询练习
- [ ] 记录了每个查询的结果
- [ ] 写下了今日笔记

---

## 明天预告

Day 2：SQL进阶 - JOIN

- 关联products表 + competitors表
- 理解INNER JOIN vs LEFT JOIN
- 写3个JOIN查询
