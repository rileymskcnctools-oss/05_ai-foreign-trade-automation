# Day 17: Prompt 工程入门

> 日期: Week 3 / Day 17
> 时间: 约 1 小时
> 目标: 理解 Prompt 工程的核心技巧, 能修改 Prompt 模板并观察输出变化

---

## 学习任务 (30 分钟)

### Prompt 工程三板斧

**1. 角色设定 (System Prompt)**
告诉 AI "你是谁": `你是一个有 10 年经验的阿里国际站 SEO 专家`
- 角色越具体, 输出越专业
- 行业经验年限 = 专业度暗示

**2. 结构化输入 (Context)**
用编号、标签、分隔线组织信息:
```
[产品信息]
- 产品名: xxx
- 材质: xxx
[规则]
1. xxx
2. xxx
```
- 结构化 > 自然语言 (AI 更容易解析)

**3. 输出格式约束**
明确告诉 AI 怎么输出:
- `直接输出 3 个标题, 每行一个, 不要编号`
- `用 JSON 格式输出`
- `不超过 128 个字符`

### 对比实验
分别看 `prompts/seo/alibaba_title.md` 和 `prompts/seo/selling_points.md`:

| 维度 | alibaba_title | selling_points |
|------|--------------|----------------|
| 角色 | SEO 专家 | 产品开发+销售文案 |
| 输出数量 | 3 个标题 | 5 个卖点 |
| 格式要求 | 每行一个 | Feature->Benefit |
| 温度建议 | 0.7 | 0.7 |

---

## 动手任务 (25 分钟)

### 任务 1: 修改 Prompt 模板, 观察输出变化
复制 `prompts/seo/alibaba_title.md` 为 `prompts/seo/alibaba_title_v2.md`, 修改:
- 把角色改为 `"你是一个专注非洲市场的 Garden Tools 进口商"`
- 加一条规则: `标题必须包含产地信息 (Made in China)`

然后写脚本测试:
```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.database import FTDatabase
from src.core.llm_client import LLMClient
from src.utils.prompts import load_prompt, fill_prompt, build_product_data

db = FTDatabase()
product = db.product_get("GF-001")
data = build_product_data(product)

# 用原版模板
template_v1 = load_prompt("seo/alibaba_title")
filled_v1 = fill_prompt(template_v1, data)

# 用修改版模板
template_v2 = load_prompt("seo/alibaba_title_v2")
filled_v2 = fill_prompt(template_v2, data)

llm = LLMClient(scenario="seo_content")

print("=== 原版模板输出 ===")
print(llm.chat(filled_v1, max_tokens=300, temperature=0.7))

print("\n=== 修改版模板输出 ===")
print(llm.chat(filled_v2, max_tokens=300, temperature=0.7))

db.close()
```

### 任务 2: 尝试不同的 temperature
用同一个 prompt, 分别设置 `temperature=0.3` 和 `temperature=0.9`, 观察输出差异。

---

## 总结 (5 分钟)

1. 修改 Prompt 模板后, AI 输出有什么变化?
2. temperature 高和低的区别是什么?
3. 你觉得当前的 `alibaba_title.md` 模板还需要改进什么?

---

## 检查清单
- [ ] 理解了 Prompt 工程三板斧
- [ ] 创建了 `alibaba_title_v2.md` 并测试
- [ ] 测试了不同 temperature 的效果
- [ ] 完成了总结

---

## 明天预告
Day 18: 在 ft_cli.py 中实现 `generate` 命令, 串联整个流程!
