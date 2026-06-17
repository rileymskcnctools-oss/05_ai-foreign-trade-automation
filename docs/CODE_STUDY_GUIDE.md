# 外贸AI工作台 V0.1 — 代码深度学习指南

> 目标：让你从"能跑就行"升级到"面试能讲清楚、出问题能排查"
> 建议阅读顺序：按章节从 1 → 8 顺序来，每章花 1-2 天

---

## 目录

1. [项目总览：一句话说清这个系统](#1-项目总览)
2. [架构地图：文件关系图](#2-架构地图)
3. [核心模块逐个攻破](#3-核心模块)
   - 3.1 database.py — 数据库核心
   - 3.2 config.py — 配置管理
   - 3.3 llm_client.py — AI大模型客户端
   - 3.4 prompts.py — 提示词模板引擎
   - 3.5 search.py — 搜索与过滤
   - 3.6 cleaner.py — 数据清洗
   - 3.7 exporter.py — 数据导出
4. [入口文件逐个攻破](#4-入口文件)
   - 4.1 ft_cli.py — CLI命令行
   - 4.2 app.py — Streamlit Web界面
5. [数据流全链路追踪](#5-数据流)
6. [数据库Schema深度解读](#6-数据库Schema)
7. [Prompt模板工程](#7-Prompt模板)
8. [面试高频Q&A速查表](#8-面试QA)

---

## 1. 项目总览

**一句话**：这是一个"手动农具外贸AI工作台"——把产品数据存进SQLite数据库，用AI批量生成阿里国际站SEO标题、产品卖点、WhatsApp开发话术，通过CLI和Web两种界面操作。

**面试版一句话**：
> 我搭建了一个面向外贸业务场景的AI辅助工作台，使用Python + SQLite + DeepSeek API，实现了产品数据管理、AI批量内容生成、多条件搜索过滤，前端用Streamlit做可视化操作界面，后端用CLI做批量自动化。

**你必须能回答的3个问题**：
1. 这个系统解决什么问题？→ 手动写SEO标题/话术太慢，AI批量生成
2. 技术栈是什么？→ Python + SQLite + DeepSeek API + Streamlit
3. 数据怎么流的？→ CSV导入 → SQLite → AI读取+模板填充 → AI生成 → 写回SQLite

---

## 2. 架构地图

```
项目根目录/
├── app.py                  ← [入口B] Streamlit Web界面（344行）
├── data/
│   ├── ft_workspace.db     ← SQLite数据库文件（215个产品）
│   └── schema.sql          ← 数据库表结构定义（283行）
├── config/
│   ├── settings.yaml       ← 公开配置（端口、模型、路径）
│   └── .env                ← 私密配置（API Key，不上传GitHub）
├── prompts/                ← AI提示词模板库（19个.md文件）
│   ├── seo/
│   │   ├── alibaba_title.md    ← 阿里SEO标题模板（最核心）
│   │   ├── selling_points.md   ← 产品卖点模板
│   │   └── ...
│   └── social/
│       └── whatsapp.md         ← WhatsApp话术模板
├── scripts/
│   └── ft_cli.py           ← [入口A] CLI命令行（530行）
├── src/
│   ├── core/               ← 核心基础设施
│   │   ├── database.py     ← 数据库操作类（341行）★最重要
│   │   ├── config.py       ← 配置加载器（198行）
│   │   └── llm_client.py   ← AI大模型客户端（349行）★重要
│   ├── utils/
│   │   └── prompts.py      ← 提示词模板引擎（236行）★重要
│   ├── m1_product_db/      ← 模块1：产品数据库
│   │   ├── search.py       ← 搜索+过滤（147行）
│   │   ├── cleaner.py      ← 数据清洗（158行）
│   │   ├── exporter.py     ← CSV/Excel导出（140行）
│   │   ├── importer.py     ← CSV/Excel导入
│   │   └── ai_completer.py ← AI自动补全字段
│   ├── m3_seo/             ← 模块3：SEO内容生成
│   ├── m2_marketing/       ← 模块2：营销材料
│   └── m4~m9/              ← 未实现模块（只有空__init__.py）
└── output/
    └── generate_log.txt    ← 批量生成日志
```

**关键认知**：
- 共有 9 个模块（m1~m9），V0.1只实现了 M1（产品数据库）+ M3（SEO内容）+ CLI + Web
- 其他模块（客户CRM、报价、市场调研等）只有schema.sql里的表结构，代码是空的
- 这是"先跑通核心链路，再逐步扩展"的务实策略

---

## 3. 核心模块逐个攻破

### 3.1 database.py — 数据库核心（341行）★★★最重要

**位置**：`src/core/database.py`

**面试定位**：这是整个系统的"数据层"，所有数据的读写都经过这里。

#### 你需要掌握的知识点

**A. SQLite连接配置（第18-42行）**
```python
self.conn = sqlite3.connect(db_path, check_same_thread=False, timeout=10)
self.conn.row_factory = sqlite3.Row
self.conn.execute("PRAGMA journal_mode=WAL")
self.conn.execute("PRAGMA foreign_keys=ON")
```

面试必答：
- `check_same_thread=False` → 允许多线程访问（Streamlit需要，因为每个用户请求是独立线程）
- `timeout=10` → 等待锁最多10秒，避免"database is locked"错误
- `row_factory = sqlite3.Row` → 查询结果可以用`row['column_name']`取值，不用记下标
- `PRAGMA journal_mode=WAL` → Write-Ahead Logging模式，读写并发不互相阻塞
- `PRAGMA foreign_keys=ON` → 开启外键约束，保证数据完整性

**B. 上下文管理器（第101-108行）**
```python
def __enter__(self):
    return self
def __exit__(self, exc_type, exc_val, exc_tb):
    if exc_type is None:
        self.commit()
    self.close()
```

面试必答：这叫"Context Manager模式"，用`with FTDatabase() as db:`时自动管理连接生命周期，异常时自动回滚，正常时自动提交。

**C. 四个底层CRUD方法（第73-90行）**
- `execute(sql, params)` → 单条增删改
- `executemany(sql, params_list)` → 批量增删改
- `fetchone(sql, params)` → 查一条，返回dict或None
- `fetchall(sql, params)` → 查多条，返回dict列表

面试必答：所有SQL都用参数化查询（`?`占位符），防止SQL注入攻击。

**D. 业务方法（第114-309行）**
- 产品：`product_get` / `product_list` / `product_search` / `product_insert` / `product_insert_many`
- 客户：`client_create` / `client_get` / `client_search`
- 活动：`activity_log` / `activity_list`
- 报价：`quotation_create`（自动生成编号 `QT-2026-0001`）
- 看板：`stats_summary`（汇总6个核心指标）
- 备份：`backup`（物理复制.db文件）

**E. 动态SQL拼接（第168-180行）**
```python
columns = ", ".join(product.keys())
placeholders = ", ".join(["?"] * len(product))
sql = f"INSERT OR REPLACE INTO products ({columns}) VALUES ({placeholders})"
```

面试必答：这种方式让代码自动适应数据库字段变化——即使以后加了新字段，这行代码不用改。

---

### 3.2 config.py — 配置管理（198行）★★重要

**位置**：`src/core/config.py`

#### 你需要掌握的知识点

**A. 双层配置架构**
- `settings.yaml` → 公开配置（模型名称、路径、默认值），可以上传Git
- `.env` → 私密配置（API Key），绝不上传Git

**B. 环境变量注入（第74-80行）**
```python
def replace_var(match):
    var_name = match.group(1)
    return os.environ.get(var_name, match.group(0))
content = re.sub(r'\$\{(\w+)\}', replace_var, content)
```

面试必答：YAML里的`${DEEPSEEK_API_KEY}`会被正则替换为.env里的真实密钥。这是12-Factor App配置管理的标准做法。

**C. 单例模式（第187-199行）**
```python
_config_instance = None
def get_config():
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance
```

面试必答：Singleton模式确保整个程序运行期间只有一个配置实例，节省内存，避免不同模块读到不同配置。

**D. 点号路径访问（第127-141行）**
```python
config.get("defaults.port")  # 返回 "Tianjin"
```

面试必答：支持嵌套字典的点号路径访问，类似YAML的层级结构，调用方不需要关心内部嵌套深度。

---

### 3.3 llm_client.py — AI大模型客户端（349行）★★★重要

**位置**：`src/core/llm_client.py`

#### 你需要掌握的知识点

**A. 多供应商路由（第53-60行）**
```python
ROUTING = {
    "seo_content": "deepseek",
    "market_research": "deepseek",
    "client_analysis": "deepseek",
    ...
}
```

面试必答：Scenario-based Routing（基于场景的路由）。不同任务可以自动分配给不同AI供应商，比如SEO用DeepSeek省钱，重要客户分析用Claude更精准。

**B. 懒加载导入（第27-46行）**
```python
def _lazy_import():
    global openai, anthropic, google_ai
    if openai is None:
        try:
            import openai as _openai
            openai = _openai
        except ImportError:
            pass
```

面试必答：Lazy Import——只在真正需要时才导入依赖库。好处：(1)启动速度快 (2)没装某个库也不会报错 (3)减少内存占用。

**C. API Key三级查找（第146-167行）**
优先级：代码传参 > YAML配置 > 环境变量
```python
# 1. 代码里传入的api_key参数
if self._override_api_key: return self._override_api_key
# 2. settings.yaml里的配置
if self._config: key = self._config.get_api_key(...)
# 3. 环境变量
api_key = os.environ.get(pc["api_key_env"], "")
```

**D. JSON输出格式化（第283-340行）**
- `generate_json()` → 强制AI返回JSON格式，自动清理```json包裹
- `generate_list()` → 强制AI返回JSON数组

面试必答：这是"Prompt Engineering + Output Parsing"的实践——通过prompt约束输出格式，再用代码做容错清理（去除markdown代码块包裹）。

**E. Claude vs OpenAI的API差异**
```python
# OpenAI (Qwen也兼容这个接口)
response = client.chat.completions.create(model=..., messages=[...])
return response.choices[0].message.content

# Claude
response = client.messages.create(model=..., messages=[...])
for block in response.content:
    if block.type == "text": return block.text
```

面试必答：OpenAI和Anthropic的API接口不同，但这个客户端通过统一的`chat()`方法屏蔽了差异——这就是"Adapter模式"。

---

### 3.4 prompts.py — 提示词模板引擎（236行）★★重要

**位置**：`src/utils/prompts.py`

#### 你需要掌握的知识点

**A. 模板加载流程**
```
prompts/seo/alibaba_title.md  (含 ${key} 占位符)
    ↓ load_prompt("seo/alibaba_title")   从磁盘读取
    ↓ fill_prompt(template, data)          正则替换占位符
    ↓ 填充后的完整prompt
    ↓ 发给AI
```

**B. 双格式占位符（第97-122行）**
```python
# 第一轮：替换 ${key} 格式（v1.0旧版模板）
result = re.sub(r'\$\{(\w+)\}', replace_dollar, template)
# 第二轮：替换 {key} 格式（v2.0新版模板，注意要排除已被替换的${}）
return re.sub(r'(?<!\$)\{(\w+)\}', replace_brace, result)
```

面试必答：兼容新旧两种占位符格式。`(?<!\$)`是负向前瞻，确保`${key}`里的`{key}`不会被重复替换。

**C. 一站式函数 fill_and_send()（第125-163行）**
把"加载模板 → 填充数据 → 调用AI → 返回结果"封装成一个函数调用。

**D. build_product_data()（第184-236行）**
```python
# 两个关键动作：
# 1. 所有值转字符串（数据库可能存的是数字/None）
# 2. 拼接一个 "specifications" 综合规格字段
data["specifications"] = "Material: Carbon Steel\nHandle: Ash Wood\n..."
```

面试必答：这是一个"数据适配层"——数据库的原始数据和Prompt模板需要的格式不完全一致，build_product_data做中间转换。

---

### 3.5 search.py — 搜索与过滤（147行）★了解

**位置**：`src/m1_product_db/search.py`

**关键模式**：动态SQL构建
```python
sql = "SELECT * FROM products WHERE 1=1"
if category:
    sql += " AND category = ?"
    params.append(category)
```

面试必答：`WHERE 1=1`是一个经典技巧——它永远为True，这样后面所有条件都可以用`AND`拼接，不用特殊处理第一个条件。

---

### 3.6 cleaner.py — 数据清洗（158行）★了解

**位置**：`src/m1_product_db/cleaner.py`

**关键知识点**：
- 包装类型标准化（中英文映射表）
- 数值字段类型转换（字符串→int/float）
- 字符串去空格、空值转None

面试必答：这是"ETL中的T（Transform）"的实践——数据从CSV导入后，需要清洗标准化才能用于AI生成。

---

### 3.7 exporter.py — 数据导出（140行）★了解

**位置**：`src/m1_product_db/exporter.py`

**关键知识点**：
- `csv.DictWriter` → 字典直接写CSV，自动对齐列
- `extrasaction="ignore"` → 多余的key自动忽略，不会报错
- `os.makedirs(exist_ok=True)` → 自动创建目录，目录已存在也不报错

---

## 4. 入口文件逐个攻破

### 4.1 ft_cli.py — CLI命令行（530行）★★★重要

**位置**：`scripts/ft_cli.py`

**架构理解**：
```
用户输入命令 → main()解析sys.argv → 路由到cmd_xxx函数 → 调用底层模块
```

**8个命令**：
| 命令 | 函数 | 作用 |
|------|------|------|
| `stats` | `cmd_stats()` | 系统大盘统计 |
| `search <词>` | `cmd_search()` | 模糊搜索产品 |
| `list --category X` | `cmd_list()` | 按分类列表 |
| `get <编码>` | `cmd_get()` | 精确查看单个产品 |
| `export <路径>` | `cmd_export()` | 导出CSV |
| `missing` | `cmd_missing()` | 显示缺失字段 |
| `generate <编码>` | `cmd_generate()` | 单个产品AI生成 |
| `generate all` | `cmd_generate_all()` | 批量AI生成（带重试+日志） |

**面试核心：cmd_generate的数据管道（第157-251行）**
```
数据库产品数据 → build_product_data() → load_prompt() → fill_prompt() → AI生成 → 写回数据库
```
这个管道面试必讲。

**面试核心：cmd_generate_all的容错设计（第254-408行）**
- 失败重试：`for attempt in range(1, max_retries + 1)`
- 递增等待：`time.sleep(2 * attempt)` → 第1次等2s，第2次等4s
- 日志记录：每次操作写入`output/generate_log.txt`
- 进度显示：`[3/215] GS-003 — Garden Fork`
- 最终汇总：成功/失败/跳过/重试次数/总耗时

**面试必答**：这是"Batch Processing + Error Handling"的实践——批量任务不能因为一个失败就全停，需要重试+跳过+记录。

---

### 4.2 app.py — Streamlit Web界面（344行）★★★重要

**位置**：`app.py`

**架构理解**：
```
页面加载 → get_db()获取数据库连接 → 侧边栏搜索 → 查询产品 → 展示列表 → 点击查看详情 → AI生成
```

**关键知识点**：

**A. 数据库连接缓存（第29-34行）**
```python
@st.cache_resource
def get_db():
    return FTDatabase()
```

面试必答：`@st.cache_resource`是Streamlit的单例缓存装饰器——多次刷新页面时复用同一个数据库连接，避免反复打开/关闭。这就是为什么需要`check_same_thread=False`。

**B. PRAGMA table_info的坑（第210-211行）**
```python
col_names = [c[1] for c in db.execute("PRAGMA table_info(products)").fetchall()]
prod_dict = dict(zip(col_names, product))
```

面试必答：这是踩过的坑——`PRAGMA table_info`返回的第一列`c[0]`是序号(cid)，第二列`c[1]`才是列名(name)。最初写成`c[0]`导致所有产品详情参数显示为空。

**C. 三列布局（第256-286行）**
```python
gen_col1, gen_col2, gen_col3 = st.columns(3)
```

**D. rerun()刷新（第264行）**
```python
st.rerun()  # AI生成成功后刷新页面，显示新内容
```

**E. 数据库直接SQL查询（第142-155行）**
Streamlit页面直接写SQL查询，没有走database.py的封装——这是为了简化页面逻辑。面试时可以说"在快速原型阶段，直接SQL更高效"。

---

## 5. 数据流全链路追踪

### 5.1 产品数据从哪来？
```
Excel/CSV产品表 
    → scripts/importer.py（数据清洗+格式化）
    → database.py product_insert_many() 
    → SQLite products表（215条记录）
```

### 5.2 AI内容怎么生成的？
```
1. 读取产品数据：db.product_get("GS-001")
   → 返回 dict: {product_name_en: "Garden Fork", material: "Carbon Steel", ...}

2. 转换为模板格式：build_product_data(product)
   → 返回扁平dict，所有值转字符串，拼接specifications字段

3. 加载提示词模板：load_prompt("seo/alibaba_title")
   → 读取 prompts/seo/alibaba_title.md，包含 ${product_name_en} 等占位符

4. 填充模板：fill_prompt(template, data)
   → 正则替换所有 ${xxx} 为实际值

5. 调用AI：LLMClient(scenario="seo_content").chat(filled)
   → DeepSeek API返回3个SEO标题

6. 保存回数据库：db.execute("UPDATE products SET seo_title_1=?...", ...)
   → 写入SQLite
```

### 5.3 Web界面怎么工作的？
```
用户打开浏览器 → streamlit run app.py
    → @st.cache_resource 创建数据库连接（单例）
    → 页面渲染：搜索框 + 分类下拉 + 产品列表
    → 用户搜索/选择分类 → SQL查询 → DataFrame展示
    → 用户选择产品 → 显示详情卡片
    → 用户点击"生成SEO标题" → generate_ai_content() → 保存 → rerun()刷新
```

---

## 6. 数据库Schema深度解读

### products表（54个字段）— 核心表

**产品基本信息**：
- `product_code` (TEXT UNIQUE) → 产品编码，如"GS-001"
- `product_name_en/cn` → 英文/中文名
- `category` / `sub_category` → 分类/子分类

**物理参数**：
- `material` / `handle_material` → 材质/手柄材质
- `length_cm` / `weight_kg` / `head_width_cm` → 尺寸参数
- `tine_count` → 齿数（耙子专用）
- `hardness` / `surface_treatment` → 硬度/表面处理

**商务参数**：
- `moq` → 最小起订量
- `packaging_type` / `qty_per_carton` / `carton_size_cm` → 包装信息
- `gw_per_carton_kg` → 每箱毛重
- `lead_time_days` → 交货期
- `certification` → 认证（CE等）

**AI生成内容**：
- `seo_title_1/2/3` → 3个SEO标题
- `selling_points` → 产品卖点
- `whatsapp_script` → WhatsApp话术

**物流**：
- `loading_qty_20ft/40ft/40hq` → 装柜数量
- `hs_code` → 海关编码

**其他表**（V0.1已建表但未实现业务逻辑）：
- `clients` → 客户档案
- `activities` → 跟进记录
- `inquiries` → 询盘
- `quotations` → 报价单
- `orders` → 订单
- `market_reports` / `market_knowledge` → 市场调研
- `content_records` → 内容版本管理
- `outreach_templates` → 开发信模板
- `price_records` → 价格记录

---

## 7. Prompt模板工程

### 以alibaba_title.md为例的Prompt结构

```
1. 角色设定：你是一个有10年经验的阿里国际站SEO专家
2. 任务描述：为以下产品生成3个SEO标题
3. 产品信息（用占位符填充）：
   - ${product_name_en}
   - ${category} / ${sub_category}
   - ${material}
   - ${specifications}
4. 目标关键词：${target_keywords}
5. 规则约束：
   - 不超过128字符
   - 关键词前置
   - 3个标题不同侧重点
   - 禁用无意义词
6. 输出格式：直接输出，每行一个
```

**面试必答的Prompt Engineering原则**：
1. **角色设定** → 帮AI进入专业领域
2. **明确输出格式** → 避免AI自作主张输出JSON/Markdown
3. **规则约束** → 字数限制、关键词前置、禁止用语
4. **变量填充** → 同一个模板适用于所有产品，动态填入数据
5. **Few-shot缺失** → 当前版本没有给示例，这是可以优化的方向

---

## 8. 面试高频Q&A速查表

### Q1: 这个项目的架构是怎样的？
> 分层架构：数据层(SQLite) → 业务层(搜索/清洗/AI生成) → 展示层(CLI + Streamlit)。模块化设计，核心4个文件：database.py管数据、llm_client.py管AI、prompts.py管模板、app.py/ft_cli.py管入口。

### Q2: 为什么选SQLite不用MySQL/PostgreSQL？
> 单用户/小团队场景，SQLite零配置、一个文件就是一个数据库、性能足够（215条记录毫秒级查询）。如果未来团队扩大，切换到PostgreSQL只需改database.py的连接方式，SQL语法90%兼容。

### Q3: AI调用失败怎么处理的？
> 三层容错：(1)try-catch捕获异常 (2)自动重试最多3次，递增等待2s/4s/6s (3)日志记录到generate_log.txt，最终汇总报告。

### Q4: Streamlit和CLI有什么区别？
> CLI适合批量操作（一次性给215个产品生成内容），Streamlit适合日常交互（搜索某个产品、查看详情、单个生成）。两者共用同一套底层模块（database.py, llm_client.py）。

### Q5: 数据库为什么用check_same_thread=False？
> Streamlit每个用户请求跑在独立线程上，SQLite默认禁止跨线程访问。加上这个参数后允许多线程共享同一个连接，配合`timeout=10`避免并发锁冲突。

### Q6: 这个项目有什么可以改进的？
> (1)Prompt没给Few-shot示例，生成质量不稳定 (2)没有异步处理，批量生成215个产品耗时长 (3)AI生成结果没做自动质检（长度/关键词覆盖） (4)没有版本控制（同一产品多次生成会覆盖） (5)Web界面没有用户认证。

### Q7: 批量生成的日志系统怎么设计的？
> 每次操作追加写入`generate_log.txt`，格式：`[时间戳] 操作 产品编码 类型`。成功记`OK`，失败记`FAIL`，重试记`RETRY`。最终汇总成功数/失败数/跳过数/重试次数/总耗时。

### Q8: config.py的环境变量注入原理？
> YAML配置里写`${DEEPSEEK_API_KEY}`占位符，程序启动时先用python-dotenv把.env文件加载到`os.environ`，再用正则`re.sub`把YAML里的占位符替换成真实的环境变量值。API Key永远不会明文出现在代码或Git里。

### Q9: PRAGMA table_info的坑是什么？
> `PRAGMA table_info(products)`返回的每一行是`(cid, name, type, notnull, dflt_value, pk)`，`c[0]`是序号不是列名！必须用`c[1]`取列名。最初写错导致产品详情页面所有参数显示为空。

### Q10: 你的项目中用到了哪些设计模式？
> (1)Singleton → config.py全局配置实例 (2)Context Manager → database.py的with语句 (3)Adapter → llm_client.py统一OpenAI/Claude接口 (4)Template Method → prompts.py的模板填充流程 (5)Pipeline → 数据从CSV→清洗→存储→AI生成→回写。

### Q11: 怎么保证SQL安全？
> 所有查询使用参数化查询（`?`占位符+params元组），绝不做字符串拼接。比如：`db.execute("SELECT * FROM products WHERE code=?", (code,))`。

### Q12: 这个项目用到了哪些Python高级特性？
> (1)装饰器 → `@st.cache_resource` (2)上下文管理器 → `with FTDatabase() as db` (3)类型注解 → `Optional[str]`, `list[dict]` (4)动态SQL拼接 → `", ".join(keys)` (5)正则表达式 → 占位符替换 (6)lazy import → 延迟加载第三方库。

---

## 学习进度自检表

学完每一章后，对照以下标准：

| 章节 | 通过标准 |
|------|---------|
| 1. 项目总览 | 能用一句话向外行解释这个项目 |
| 2. 架构地图 | 能画出文件关系图（手画或白板） |
| 3.1 database.py | 能解释5个PRAGMA参数的作用 |
| 3.2 config.py | 能画出"env → yaml → 代码"的数据流 |
| 3.3 llm_client.py | 能说出路由机制和懒加载的好处 |
| 3.4 prompts.py | 能解释模板填充的两轮正则替换 |
| 4.1 ft_cli.py | 能手画generate命令的数据管道 |
| 4.2 app.py | 能解释@st.cache_resource和PRAGMA坑 |
| 5. 数据流 | 能画出"CSV → SQLite → AI → 回写"全流程 |
| 6. Schema | 能说出products表5大字段分类 |
| 7. Prompt | 能说出5个Prompt Engineering原则 |
| 8. 面试QA | 能流利回答12个问题（每题30秒内） |

---

*文档生成时间：2026-06-17*
*代码版本：V0.1（commit 35afe7b）*
