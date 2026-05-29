# Day 2 任务：SQL进阶 - JOIN连接

> 日期：Week 1 / Day 2
> 时间：约2小时
> 目标：掌握JOIN操作，关联产品数据和竞品数据

---

## 学习任务（40分钟）

### JOIN 类型回顾

```sql
-- INNER JOIN：只返回两表都有匹配的行
SELECT p.product_name, p.price, c.competitor_name, c.competitor_price
FROM products_clean p
INNER JOIN competitors_clean c ON p.asin = c.product_asin;

-- LEFT JOIN：返回左表所有行，右表无匹配则为NULL
SELECT p.product_name, p.price, c.competitor_name
FROM products_clean p
LEFT JOIN competitors_clean c ON p.asin = c.product_asin;
```

### 项目04中的应用

| JOIN类型              | 业务问题               |
| ------------------- | ------------------ |
| INNER JOIN          | 哪些产品同时出现在产品表和竞品表中？ |
| LEFT JOIN           | 所有产品中，哪些没有被竞品关联？   |
| LEFT JOIN + IS NULL | 找出没有竞品关联的孤儿产品      |

---

## 动手任务（50分钟）

### 任务 1：写3个JOIN查询

```sql
-- Q1 (INNER JOIN): 关联产品表和竞品表，计算竞品价格差距
-- Q2 (LEFT JOIN): 所有产品+竞品关联（无竞品的显示NULL）
-- Q3 (LEFT JOIN + IS NULL): 找出没有竞品关联的产品，统计数量
```

### 任务 2：分析竞品价格差距

```sql
-- 计算我方产品与竞品的平均价格差距，按品类分组
```

---

## 总结（30分钟）

### 今日笔记

1. 完成的JOIN查询：

2. INNER JOIN vs LEFT JOIN的理解：

3. 竞品价格差距的发现：

4. 卡壳的地方：

---

## 检查清单

- [ ] 理解了INNER JOIN和LEFT JOIN的区别
- [ ] 完成了3个JOIN查询
- [ ] 计算了竞品价格差距
- [ ] 记录了今日笔记

---

## 明天预告

Day 3：SQL进阶 - 子查询 + CTE

- 用CTE改写复杂查询
- 写2个嵌套子查询
