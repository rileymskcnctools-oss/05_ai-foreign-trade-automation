# Day 29 任务：requests库 - HTTP GET请求

> 日期：Week 5 / Day 1
> 时间：约2小时
> 目标：掌握requests库，发送HTTP请求获取API数据

---

## 学习任务（40分钟）

### 什么是API？

API = 应用程序编程接口。一个网址，你发送请求，它返回数据。

### requests基础

```python
import requests
response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
print(response.status_code)  # 200 = 成功
data = response.json()
print(data["rates"]["EUR"])
```

---

## 动手任务（50分钟）

### 任务 1：获取汇率数据

```python
import requests
url = "https://api.exchangerate-api.com/v4/latest/USD"
response = requests.get(url)
data = response.json()
print(f"EUR: {data['rates']['EUR']}")
print(f"CNY: {data['rates']['CNY']}")
```

### 任务 2：汇率转换产品价格

```python
products = [
    {"name": "Garden Fork", "price_usd": 12.99},
    {"name": "Garden Spade", "price_usd": 9.99},
]
rates = data["rates"]
for p in products:
    p["price_eur"] = round(p["price_usd"] * rates["EUR"], 2)
    print(f"{p['name']}: ${p['price_usd']} -> EUR {p['price_eur']}")
```

### 任务 3：封装为函数

```python
def get_exchange_rates(base="USD"):
    url = f"https://api.exchangerate-api.com/v4/latest/{base}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
```

---

## 总结（30分钟）

### 今日笔记

---

## 检查清单

- [ ] 成功发送了HTTP请求
- [ ] 获取并解析了JSON
- [ ] 用汇率转换了价格
- [ ] 封装了函数
- [ ] 记录了今日笔记

---

## 明天预告

Day 30：API与LLM调用基础
