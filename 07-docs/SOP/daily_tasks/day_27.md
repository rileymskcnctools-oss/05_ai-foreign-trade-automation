# Day 27 任务：pandas进阶 - 数据清洗

> 日期：Week 4 / Day 6
> 时间：约2小时
> 目标：掌握缺失值、重复值处理、类型转换

---

## 学习任务（40分钟）

### 缺失值

```python
df.isnull().sum()
df.dropna()
df["price"].fillna(df["price"].median(), inplace=True)
```

### 重复值

```python
df.duplicated().sum()
df.drop_duplicates(subset=["product_id"])
```

### 衍生字段

```python
df["price_per_kg"] = df["price"] / df["weight_kg"]
df["price_tier"] = pd.cut(df["price"], bins=[0,10,25,50,100,999],
                          labels=["入门","低端","中端","高端","工业级"])
```

---

## 动手任务（50分钟）

### 任务 1：清洗项目05的Excel

```python
import pandas as pd
df = pd.read_excel(r"C:\Users\Administrator\Desktop\code\05_AI-外贸自动化系统\01-产品数据库模板\产品参数表模板.xlsx")

# 1. 检查缺失值
# 2. 处理缺失值
# 3. 检查重复值
# 4. 类型转换
# 5. 创建衍生字段
# 6. 保存清洗后的数据
df.to_csv("products_clean_v1.csv", index=False)
```

---

## 总结（30分钟）

### 今日笔记

---

## 检查清单

- [ ] 检查了缺失值
- [ ] 处理了重复值
- [ ] 创建了衍生字段
- [ ] 保存了清洗后的数据
- [ ] 记录了今日笔记

---

## 明天预告

Day 28：复习日
