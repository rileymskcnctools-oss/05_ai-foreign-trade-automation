# Day 31 任务：pandas + API数据合并

> 日期：Week 5 / Day 3
> 时间：约2小时
> 目标：将API返回的数据与Excel产品数据合并

---

## 学习任务（30分钟）

### pandas合并数据

```python
df["price_eur"] = df["price_usd"] * 0.85
df["weight_lbs"] = (df["weight_kg"] * 2.20462).round(2)
```

---

## 动手任务（60分钟）

### 任务 1：读取Excel并合并汇率

```python
import pandas as pd, requests
response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
rates = response.json()["rates"]

df = pd.read_excel(r"C:\Users\Administrator\Desktop\code\05_AI-外贸自动化系统\01-产品数据库模板\产品参数表模板.xlsx")
df["weight_lbs"] = (df["weight_kg"] * 2.20462).round(2)
print(df[["product_name_en", "weight_kg", "weight_lbs"]])
```

### 任务 2：保存合并后的数据

```python
df.to_csv("products_with_conversions.csv", index=False)
df.to_excel("products_with_conversions.xlsx", index=False)
```

---

## 总结（30分钟）

### 今日笔记

---

## 检查清单

- [ ] 获取了汇率API
- [ ] 合并了数据
- [ ] 保存了文件
- [ ] 验证了数据
- [ ] 记录了今日笔记

---

## 明天预告

Day 32：函数编写 - 封装Prompt逻辑
