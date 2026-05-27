# Day 22 任务：Python基础 - 变量与数据类型

> 日期：Week 4 / Day 1
> 时间：约2小时
> 目标：安装Python环境，掌握变量、数据类型和基本运算

---

## 学习任务（40分钟）

### 安装

```bash
python --version
pip install jupyter
jupyter notebook
```

### 变量与数据类型

```python
product_name = "Garden Fork"    # str
moq = 500                        # int
price = 12.99                    # float
is_fba = True                    # bool
```

### 基本运算

```python
total = price * moq
info = f"产品: {product_name}, 价格: ${price}"
```

---

## 动手任务（50分钟）

### 任务 1：创建Jupyter Notebook

```python
# Cell 1: 创建产品变量
product_id = "GF-001"
product_name = "Garden Fork"
price = 12.99
weight = 0.8
moq = 500

# Cell 2: 计算
total_revenue = price * moq
print(f"总收入: ${total_revenue:.2f}")

# Cell 3: 条件判断
if price > 10:
    print(f"{product_name} 是高端产品")
```

### 任务 2：用项目05的产品数据练习

```python
products = [
    {"id": "GF-001", "name": "Garden Fork", "price": 12.99},
    {"id": "GS-001", "name": "Garden Spade", "price": 9.99},
    # ... 补全5个产品
]
for p in products:
    print(f"{p['id']}: {p['name']} - ${p['price']}")
```

---

## 总结（30分钟）

### 今日笔记

1. Python版本：

2. 学到的数据类型：

---

## 检查清单

- [ ] 安装了Python和Jupyter
- [ ] 创建了第一个Notebook
- [ ] 完成了变量练习
- [ ] 记录了今日笔记

---

## 明天预告

Day 23：Python基础 - 列表与字典
