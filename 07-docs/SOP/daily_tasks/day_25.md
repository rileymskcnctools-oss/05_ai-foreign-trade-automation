# Day 25 任务：pandas入门 - 读取与查看数据

> 日期：Week 4 / Day 4
> 时间：约2小时
> 目标：安装pandas，读取Excel/CSV数据并探索

---

## 学习任务（40分钟）

```bash
pip install pandas openpyxl
```

### 读取数据

```python
import pandas as pd
df = pd.read_csv("products_clean.csv")
df = pd.read_excel("产品参数表模板.xlsx")
```

### 数据探索

```python
df.head()      # 前5行
df.info()      # 基本信息
df.describe()  # 统计信息
df.columns     # 列名
df.shape       # (行数, 列数)
df["col"].value_counts()  # 计数
```

---

## 动手任务（50分钟）

### 任务 1：读取项目05的Excel

```python
import pandas as pd
df = pd.read_excel(r"C:\Users\Administrator\Desktop\code\05_AI-外贸自动化系统\01-产品数据库模板\产品参数表模板.xlsx")
print("形状:", df.shape)
print("列名:", df.columns.tolist())
print(df.head())
```

### 任务 2：数据探索

```python
# 1. 查看每列的缺失值
# 2. 查看品类分布
# 3. 查看目标市场分布
# 4. 查看MOQ统计
# 5. 读取项目04的CSV并探索
```

---

## 总结（30分钟）

### 今日笔记

---

## 检查清单

- [ ] 安装了pandas
- [ ] 读取了项目05的Excel
- [ ] 读取了项目04的CSV
- [ ] 完成了数据探索
- [ ] 记录了今日笔记

---

## 明天预告

Day 26：pandas进阶 - 筛选+排序+分组
