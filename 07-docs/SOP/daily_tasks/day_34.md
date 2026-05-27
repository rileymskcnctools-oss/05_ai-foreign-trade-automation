# Day 34 任务：项目05推进 - 写自动化脚本v1

> 日期：Week 5 / Day 6
> 时间：约2.5小时
> 目标：编写第一个版本的自动化脚本

---

## 动手任务（90分钟）

### 任务 1：创建 run_pipeline.py

```python
import pandas as pd, json, os
from datetime import datetime

EXCEL_PATH = r"C:\Users\Administrator\Desktop\code\05_AI-外贸自动化系统\01-产品数据库模板\产品参数表模板.xlsx"
OUTPUT_DIR = r"C:\Users\Administrator\Desktop\code\05_AI-外贸自动化系统\05-输出结果"

def run():
    df = pd.read_excel(EXCEL_PATH)
    print(f"Loaded {len(df)} products")

    for _, row in df.iterrows():
        product_id = row.get("product_id", "UNKNOWN")
        product_name = row.get("product_name_en", "UNKNOWN")
        print(f"Processing: {product_id} - {product_name}")
        # 组装Prompt -> 调用AI -> 保存
        # （先模拟AI返回）
        output = {"product_id": product_id, "seo_titles": []}
        product_dir = os.path.join(OUTPUT_DIR, product_id)
        os.makedirs(product_dir, exist_ok=True)
        with open(os.path.join(product_dir, "output.json"), "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

    print("Pipeline complete!")

if __name__ == "__main__":
    run()
```

### 任务 2：运行脚本

```bash
cd "C:\Users\Administrator\Desktop\code\05_AI-外贸自动化系统"
python run_pipeline.py
```

### 任务 3：验证输出

检查05-输出结果/目录下是否生成了output.json。

---

## 总结（30分钟）

### 今日笔记

---

## 检查清单

- [ ] 创建了run_pipeline.py
- [ ] 运行了脚本
- [ ] 验证了输出
- [ ] 记录了今日笔记

---

## 明天预告

Day 35：复习日 - Week 1-5总复习
