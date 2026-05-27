# Day 38 任务：配置文件 - config.py

> 日期：Week 6 / Day 3
> 时间：约1.5小时
> 目标：创建配置文件管理参数

---

## 动手任务（60分钟）

### 任务 1：创建 config.py

```python
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "01-产品数据库模板", "产品参数表模板.xlsx")
OUTPUT_DIR = os.path.join(BASE_DIR, "05-输出结果")
API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
SEO_TITLE_MAX_LENGTH = 128
```

### 任务 2：更新run_pipeline.py使用配置

### 任务 3：创建 .env.example 和更新 .gitignore

---

## 总结（30分钟）

### 今日笔记

---

## 检查清单

- [ ] 创建了config.py
- [ ] 更新了run_pipeline.py
- [ ] 创建了.env.example
- [ ] 更新了.gitignore
- [ ] 记录了今日笔记

---

## 明天预告

Day 39：数据可视化 - matplotlib
