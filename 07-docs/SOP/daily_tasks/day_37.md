# Day 37 任务：日志记录 - logging模块

> 日期：Week 6 / Day 2
> 时间：约1.5小时
> 目标：用logging替代print

---

## 学习任务（30分钟）

### logging基础

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("pipeline.log", encoding="utf-8"),
    ],
)
logging.info("Pipeline started")
logging.error("API call failed")
```

---

## 动手任务（30分钟）

### 任务 1：给run_pipeline.py加日志

替换所有print为logging调用。

### 任务 2：运行并检查日志文件

```bash
cat pipeline.log
```

---

## 总结（30分钟）

### 今日笔记

---

## 检查清单

- [ ] 配置了logging
- [ ] 替换了print
- [ ] 检查了日志文件
- [ ] 记录了今日笔记

---

## 明天预告

Day 38：配置文件 - config.py
