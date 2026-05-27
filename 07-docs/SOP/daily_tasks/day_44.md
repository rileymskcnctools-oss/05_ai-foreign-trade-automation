# Day 44 任务：项目05模块化重构

> 日期：Week 7 / Day 2
> 时间：约2小时
> 目标：将run_pipeline.py拆分为3个模块

---

## 动手任务（80分钟）

### 任务 1：创建src目录

```bash
mkdir src
```

### 任务 2：拆分代码

创建3个文件：
- **src/fetch.py**：数据获取（Excel读取、API调用）
- **src/process.py**：数据处理（Prompt组装）
- **src/output.py**：数据输出（JSON保存、日志）

### 任务 3：更新run_pipeline.py使用模块

```python
from src.fetch import load_products
from src.process import build_seo_title_prompt
from src.output import save_product_output
```

---

## 总结（30分钟）

### 今日笔记

---

## 检查清单

- [ ] 创建了src目录
- [ ] 创建了3个模块文件
- [ ] 更新了run_pipeline.py
- [ ] 运行测试通过
- [ ] 记录了今日笔记

---

## 明天预告

Day 45：数据质量检查脚本
