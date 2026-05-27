# Day 45 任务：数据质量检查脚本

> 日期：Week 7 / Day 3
> 时间：约1.5小时
> 目标：写一个检查脚本，验证输出JSON的完整性

---

## 学习任务（20分钟）

### 检查维度

| 检查项 | 规则 |
|--------|------|
| 字段完整性 | 必须包含所有必填字段 |
| SEO标题数量 | 必须有5个标题 |
| 标题长度 | 每个标题≤128字符 |

---

## 动手任务（50分钟）

### 任务 1：创建 validate_output.py

```python
import json, os, glob

REQUIRED_FIELDS = ["product_id", "product_name", "seo_titles"]

def validate_product(output_dir):
    output_path = os.path.join(output_dir, "output.json")
    if not os.path.exists(output_path):
        return False, "output.json not found"
    with open(output_path, "r", encoding="utf-8") as f:
        output = json.load(f)
    for field in REQUIRED_FIELDS:
        if field not in output:
            return False, f"Missing: {field}"
    return True, "OK"

def validate_all(base_dir):
    results = {}
    for d in glob.glob(os.path.join(base_dir, "*/")):
        pid = os.path.basename(d.rstrip("/"))
        passed, msg = validate_product(d)
        results[pid] = {"passed": passed, "message": msg}
    total = len(results)
    passed = sum(1 for r in results.values() if r["passed"])
    print(f"Validation: {passed}/{total} passed")
    for pid, r in results.items():
        status = "PASS" if r["passed"] else "FAIL"
        print(f"  [{status}] {pid}: {r['message']}")

if __name__ == "__main__":
    validate_all(r"C:\Users\Administrator\Desktop\code\05_AI-外贸自动化系统\05-输出结果")
```

### 任务 2：运行检查

---

## 总结（20分钟）

### 今日笔记

---

## 检查清单

- [ ] 创建了validate_output.py
- [ ] 运行了检查
- [ ] 记录了结果
- [ ] 记录了今日笔记

---

## 明天预告

Day 46：项目05最终检查
