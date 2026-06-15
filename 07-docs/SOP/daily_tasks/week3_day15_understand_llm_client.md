# Day 15: 理解 LLM Client 和 Prompt 系统

> 日期: Week 3 / Day 15
> 时间: 约 1.5 小时
> 目标: 理解项目中已有的 AI 调用架构, 搞清楚数据如何从数据库流向 AI

---

## 学习任务 (45 分钟)

### 1. 阅读 LLM Client 模块
文件: `src/core/llm_client.py`

**核心概念:**
- `LLMClient` 类: 统一的 AI 调用接口, 支持多个供应商 (Qwen/OpenAI/Claude/Gemini)
- `chat()` 方法: 最核心的函数, 发送 prompt 给 AI, 拿回文本
- `scenario` 路由: 不同业务场景自动选择不同 AI 供应商
  - `seo_content` -> Qwen (便宜、快)
  - `market_research` -> OpenAI (质量高)
  - `client_analysis` -> Claude (分析强)

**理解要点:**
1. `__init__` 做了什么? -> 加载配置、决定用哪个供应商
2. `_get_api_key()` 从哪里拿密钥? -> 先查 YAML 配置, 再查环境变量
3. `chat()` 方法的参数含义:
   - `prompt`: 你要问 AI 的问题
   - `system_prompt`: AI 的角色设定 (可选)
   - `max_tokens`: 最大输出长度
   - `temperature`: 创造力系数 (0.0=死板, 1.0=天马行空)

### 2. 阅读 Prompt 模板系统
文件: `src/utils/prompts.py`

**核心概念:**
- `load_prompt("seo/alibaba_title")`: 从 `prompts/` 目录加载模板文件
- `fill_prompt(template, data)`: 用 `${变量名}` 占位符替换为真实产品数据
- `build_product_data(product)`: 从数据库行构建模板需要的字典

**数据流向 (重点!):**
```
数据库 product_get("GF-001")
    | 返回 dict
build_product_data(product)
    | 构建 {product_name_en: "Garden Fork", material: "Carbon Steel", ...}
load_prompt("seo/alibaba_title")
    | 加载模板文本 (含 ${xxx} 占位符)
fill_prompt(template, data)
    | 替换占位符 -> 完整的 prompt 文本
LLMClient.chat(filled_prompt)
    | 发送给 AI
AI 返回 SEO 标题文本
```

---

## 动手任务 (30 分钟)

### 任务 1: 画出数据流图
在纸上或笔记软件中画出上面的数据流向图, 用自己的话标注每一步。

### 任务 2: 阅读 Prompt 模板
打开以下 3 个文件, 逐行阅读:
- `prompts/seo/alibaba_title.md` (SEO 标题模板)
- `prompts/seo/selling_points.md` (卖点模板)
- `prompts/social/whatsapp.md` (WhatsApp 话术模板)

思考:
1. 模板中的 `${product_name_en}` 等变量从哪里来?
2. 模板中的 "规则" 部分对 AI 输出有什么影响?
3. 为什么需要 `system_prompt` 和 `user_prompt` 分开?

### 任务 3: 检查数据库字段
运行以下命令, 确认数据库中有 `seo_title_1`, `seo_title_2`, `seo_title_3` 字段:
```bash
cd /c/Users/Administrator/Desktop/code/05_ai-foreign-trade-automation
python -c "from src.core.database import FTDatabase; db=FTDatabase(); p=db.product_get('GF-001'); print([k for k in p.keys() if 'seo' in k.lower() or 'sell' in k.lower() or 'whatsapp' in k.lower()]); db.close()"
```

---

## 总结 (15 分钟)

用自己的话回答以下问题 (写在笔记中):

1. **LLM Client 的作用是什么?**
   答:

2. **Prompt 模板中的 `${xxx}` 占位符是如何被替换的?**
   答:

3. **为什么 `seo_content` 场景用 Qwen 而不用 Claude?**
   答:

---

## 检查清单
- [ ] 阅读了 `llm_client.py`, 理解 `chat()` 方法
- [ ] 阅读了 `prompts.py`, 理解 `load_prompt()` 和 `fill_prompt()`
- [ ] 阅读了 3 个 prompt 模板文件
- [ ] 画出了数据流图
- [ ] 确认了数据库中有 SEO/WhatsApp 相关字段
- [ ] 完成了 3 道总结题

---

## 明天预告
Day 16: 第一次真正调用 AI API, 让 Qwen 为你生成第一个 SEO 标题!
