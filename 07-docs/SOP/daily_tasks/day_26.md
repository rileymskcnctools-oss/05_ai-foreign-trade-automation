# Day 26 任务：pandas进阶 - 筛选、排序与分组

> 日期：Week 4 / Day 5
> 时间：约2小时
> 目标：掌握数据筛选、排序和分组聚合

---

## 学习任务（40分钟）

### 筛选

```python
df_europe = df[df["target_markets"].str.contains("Europe", na=False)]
df_mid = df[(df["price"] >= 25) & (df["price"] < 50)]
```

### 排序

```python
df.sort_values("price", ascending=False)
```

### 分组

```python
df.groupby("category")["price"].mean()
df.groupby("category").agg(
    count=("product_id", "count"),
    avg_price=("price", "mean"),
)
```

---

## 动手任务（50分钟）

### 任务 1：项目04数据练习

```python
import pandas as pd
df = pd.read_csv(r"C:\Users\Administrator\Desktop\code\04_Amazon CNC Tools Market Analysis\02_data_cleaning\products_clean.csv")

# 1. 筛选FBA产品
# 2. 筛选$50-100价格带
# 3. 按品牌分组，计算产品数和均价
# 4. 按品类分组，计算均评和评论数
# 5. 评论数最多的Top 10产品
```

---

## 总结（30分钟）

### 今日笔记

---

## 检查清单

- [ ] 完成了筛选练习
- [ ] 完成了分组聚合
- [ ] 记录了今日笔记

---

## 明天预告

Day 27：pandas进阶 - 数据清洗
