# Day 36 任务：错误处理 - try-except

> 日期：Week 6 / Day 1
> 时间：约2小时
> 目标：给自动化脚本加错误处理

---

## 学习任务（40分钟）

### try-except基础

```python
try:
    response = requests.get("https://api.example.com", timeout=10)
    response.raise_for_status()
except requests.exceptions.Timeout:
    print("请求超时")
except requests.exceptions.HTTPError as e:
    print(f"HTTP错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```

---

## 动手任务（50分钟）

### 任务 1：给run_pipeline.py加错误处理

```python
def run():
    success_count = 0
    error_count = 0
    for _, row in df.iterrows():
        try:
            # 处理逻辑
            success_count += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            error_count += 1
    print(f"Results: {success_count} succeeded, {error_count} failed")
```

### 任务 2：测试错误处理

```python
# 故意制造错误测试
try:
    pd.read_excel("nonexistent.xlsx")
except FileNotFoundError:
    print("Caught FileNotFoundError!")
```

---

## 总结（30分钟）

### 今日笔记

---

## 检查清单

- [ ] 加了try-except
- [ ] 测试了错误场景
- [ ] 验证了成功/失败计数
- [ ] 记录了今日笔记

---

## 明天预告

Day 37：日志记录 - logging模块
