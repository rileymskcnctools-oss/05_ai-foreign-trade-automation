# AI Foreign Trade Intelligent Workspace
# 外贸AI智能工作台 — 项目文档 v2.0

> 定位升级: 从「AI文案生成工具」到「AI + 外贸 + 数据运营」智能工作台
> 行业聚焦: 手动农具 (Shovel / Hoe / Rake / Pickaxe / Garden Tools / Farm Tools)
> 更新日期: 2026-06-05
> 版本: v2.0 (全面重构)

---

## 一、项目背景

### 1.1 现状与痛点

当前项目（v1.0）已实现以下能力：
- 215个SKU产品数据库（31字段，100%完整）
- AI生成SEO标题（每个产品3个变体）
- AI生成产品详情页（阿里国际站格式）
- AI生成WhatsApp开发话术
- AI生成RFQ回复模板
- 4大市场版本差异化内容

**但v1.0存在根本性局限：**

| 痛点 | 现状 | 影响 |
|------|------|------|
| 工具定位 | 单一内容生成器 | 只解决"写文案"，不解决"找客户、做决策" |
| 数据资产 | CSV文件散落 | 产品/客户/市场数据无统一管理，无法关联分析 |
| 业务覆盖 | 仅限上架内容 | 缺少客户开发、市场分析、报价、CRM等核心环节 |
| 自动化程度 | 手动触发AI | 无Agent化工作流，无定时任务，无自动化pipeline |
| 可扩展性 | 紧耦合 | 新模块需要重写大量代码，无法插件化扩展 |

### 1.2 升级动机

外贸业务员每天重复劳动集中在：
1. **产品资料制作** — 每个产品要写详情页、SEO标题、社交媒体文案
2. **客户开发** — 搜索客户、写开发信、WhatsApp/LinkedIn跟进
3. **市场调研** — 了解目标国家农业情况、竞品、价格区间
4. **报价响应** — 查产品参数、算价格、写报价邮件
5. **客户管理** — 记录联系历史、跟进状态、成交情况
6. **数据分析** — 哪些产品询盘多、哪个国家转化率高、下一步重点在哪

**v2.0目标：用AI + 数据运营，把以上6件事从"手动重复"变成"自动化 + 辅助决策"。**

---

## 二、项目目标

### 2.1 核心定位

打造一个服务于手动农具行业的 **AI外贸运营系统**，核心目标：

```
产品数据资产化  →  一个产品库，所有模块共享
客户数据资产化  →  CRM数据库，记录一切交互
市场研究自动化  →  输入国家+产品，自动出报告
营销资料自动化  →  一键生成Catalog/PPT/Word
报价流程自动化  →  参数+价格+模板，自动生成
客户开发辅助    →  AI辅助搜索、分级、写开发信
```

### 2.2 关键指标（KPI）

| 指标 | v1.0现状 | v2.0目标 |
|------|----------|----------|
| 产品资料生成时间 | 5-10分钟/产品 | <1分钟/产品 |
| 市场调研报告 | 手动搜集2-3小时 | AI自动生成10分钟 |
| 客户开发信 | 手动写15分钟/封 | AI生成+个性化2分钟/封 |
| 报价响应 | 查数据+写邮件20分钟 | 5分钟内完成 |
| 客户信息查找 | 翻聊天记录/Excel | CRM搜索10秒 |
| 数据洞察 | 靠经验和感觉 | 自动报表+趋势分析 |

### 2.3 设计原则

1. **MVP优先** — 先跑通核心流程，再逐步增强
2. **数据为中心** — 一切围绕SQLite数据库，CSV只是导入导出格式
3. **模块化** — 每个模块独立，可单独使用，可组合工作流
4. **个人友好** — 适合1人维护，不需要团队基础设施
5. **Agent-ready** — 预留Agent工作流接口，后续可接Dify/n8n

---

## 三、用户角色

### 3.1 主要用户：外贸业务员（Operator）

- **背景**: 手动农具外贸，6个月-2年经验
- **技能**: Excel(VLOOKUP/XLOOKUP)、SQL基础、Power BI基础
- **日常任务**:
  - 在阿里国际站/独立站上架产品
  - 开发新客户（Google搜索、LinkedIn、展会名片）
  - 回复客户询盘和RFQ
  - 制作产品目录和报价单
  - 跟进客户和维护关系
- **痛点**: 重复性文案工作耗时、市场信息搜集困难、客户管理混乱

### 3.2 次要用户：数据运营人员（Analyst）

- **需求**: 产品热度分析、国家机会分析、转化率跟踪
- **使用模块**: 数据运营分析中心、CRM数据库

### 3.3 系统角色（AI Agent）

- **Market Research Agent** — 自动搜集和分析目标市场信息
- **Client Analysis Agent** — 分析潜在客户并分级
- **Content Generator Agent** — 生成各类营销内容
- **Quotation Agent** — 辅助报价流程

---

## 四、功能模块设计

### 模块总览

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Foreign Trade Workspace                    │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────┤
│ M1       │ M2       │ M3       │ M4       │ M5       │ M6       │
│ 产品     │ AI产品   │ AI SEO   │ AI市场   │ AI客户   │ 开发信   │
│ 数据库   │ 营销资料 │ 平台内容 │ 研究Agent│ 分析Agent│ 跟进Agent│
├──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ M7       │ M8       │ M9       │                                  │
│ 报价     │ 客户CRM  │ 数据运营 │                                  │
│ 辅助Agent│ 数据库   │ 分析中心 │                                  │
└──────────┴──────────┴──────────┴──────────────────────────────────┘

所有模块共享 → SQLite数据库 (products + customers + markets + activities)
```

---

### M1: 产品数据库系统 (Product Database)

**定位**: 整个系统的数据基石，所有模块共享的产品数据源。

#### 4.1.1 数据模型

```sql
-- 产品主表
CREATE TABLE products (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    product_code    TEXT UNIQUE NOT NULL,     -- GF-001
    product_name_en TEXT NOT NULL,            -- Fiberglass Handle Garden Hoe
    product_name_cn TEXT,                     -- 玻璃纤维柄锄头
    category        TEXT NOT NULL,            -- Weeding Tools
    sub_category    TEXT,                     -- Garden Hoe
    hs_code         TEXT,                     -- 8201.30

    -- 技术参数
    material        TEXT,                     -- Carbon Steel + Fiberglass
    handle_material TEXT,                     -- Fiberglass
    length_cm       REAL,                     -- 105.0
    weight_kg       REAL,                     -- 0.85
    head_width_cm   REAL,                     -- 15.0
    tine_count      INTEGER,                  -- N/A for hoe
    hardness        TEXT,                     -- HRC 45-50
    surface_treatment TEXT,                   -- Polished + Powder Coated

    -- 商业信息
    moq             INTEGER,                  -- 500
    packaging_type  TEXT,                     -- Color Box
    qty_per_carton  INTEGER,                  -- 20
    carton_size_cm  TEXT,                     -- 108x22x18
    gw_per_carton_kg REAL,                    -- 18.5
    lead_time_days  INTEGER,                  -- 25
    loading_qty_20ft INTEGER,                 -- 1330
    loading_qty_40ft INTEGER,                 -- 2700
    loading_qty_40hq INTEGER,                 -- 3200

    -- 营销字段（AI填充）
    target_keywords TEXT,                     -- garden hoe, weeding tool
    use_scenario    TEXT,                     -- Garden weeding, soil breaking
    target_markets  TEXT,                     -- Africa, South America
    selling_angle   TEXT,                     -- Lightweight & durable
    competitor_ref  TEXT,                     -- Fiskars, Spear & Jackson

    -- AI生成内容
    seo_title_1     TEXT,
    seo_title_2     TEXT,
    seo_title_3     TEXT,
    selling_points  TEXT,                     -- JSON array
    whatsapp_script TEXT,
    alibaba_detail  TEXT,                     -- Markdown content

    -- 图片
    image_urls      TEXT,                     -- JSON array of URLs
    image_paths     TEXT,                     -- JSON array of local paths

    -- 元数据
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now')),
    status          TEXT DEFAULT 'active'     -- active / discontinued / pending
);

-- 产品图片表（可选，如果图片多）
CREATE TABLE product_images (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    product_code    TEXT REFERENCES products(product_code),
    image_type      TEXT,                     -- main / detail / packaging / scene
    file_path       TEXT,
    url             TEXT,
    description     TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);
```

#### 4.1.2 功能清单

| 功能 | 说明 | 优先级 |
|------|------|--------|
| CSV导入 | 从CSV文件导入产品数据，自动映射字段 | P0 |
| Excel导入 | 从Excel文件导入产品数据 | P0 |
| 数据清洗 | 去重、补空值、格式标准化 | P0 |
| AI信息补全 | 对缺失字段调用AI自动推断填充 | P1 |
| 产品搜索 | 按编码/名称/类别/关键词搜索 | P0 |
| 产品筛选 | 按材质/重量/价格区间/市场筛选 | P1 |
| 批量编辑 | 选中多个产品批量修改字段 | P1 |
| 数据导出 | 导出为CSV/Excel/JSON | P0 |
| 变更记录 | 记录每次数据修改历史 | P2 |

---

### M2: AI产品营销资料生成器 (Marketing Material Generator)

**定位**: 一键生成面向客户的产品营销资料。

#### 4.2.1 输入

```
{
    "product_codes": ["GF-001", "GS-001"],   // 可选单个或多个产品
    "target_market": "Liberia",               // 目标国家/市场
    "output_format": ["pdf", "docx", "pptx"], // 输出格式
    "language": "en",                         // 语言
    "style": "professional"                   // 风格: professional / casual / technical
}
```

#### 4.2.2 输出

| 资料类型 | 内容 | 格式 |
|----------|------|------|
| 产品目录 (Catalog) | 产品图片 + 参数表 + 卖点 + 包装 + 场景 | PDF / Word |
| 单页产品卡 (Product Sheet) | 单产品A4页，适合邮件附件 | PDF |
| 多产品目录册 | 多个产品组合的完整Catalog | PDF |
| 市场定制版 | 针对Liberia/Sri Lanka/Kenya/Tanzania定制 | PDF / Word |
| PPT演示文稿 | 适合展会/视频会议展示 | PPTX |

#### 4.2.3 产品目录结构（Catalog）

```
┌──────────────────────────────────┐
│  Company Logo & Header           │
│  "Professional Garden Tools"     │
├──────────────────────────────────┤
│  [Product Image]                 │
│                                  │
│  Product Name: Garden Hoe        │
│  Model: GF-001                   │
│                                  │
│  Specifications:                 │
│  - Material: Carbon Steel        │
│  - Handle: Fiberglass            │
│  - Length: 105cm                 │
│  - Weight: 0.85kg                │
│                                  │
│  Key Selling Points:             │
│  1. Lightweight for all-day use  │
│  2. Rust-resistant coating       │
│  3. Ergonomic grip               │
│                                  │
│  Packaging: Color Box, 20pcs/ctn │
│  MOQ: 500 pcs                    │
│                                  │
│  [Application Scene Image]       │
│  Ideal for: Garden weeding,      │
│  soil breaking, farm work        │
└──────────────────────────────────┘
```

#### 4.2.4 技术实现

```
产品数据 (SQLite)
    → AI生成卖点/描述/市场适配文案 (LLM API)
    → 模板引擎 (Jinja2 + python-docx + FPDF/ReportLab)
    → 输出 PDF / DOCX / PPTX
```

---

### M3: AI SEO与平台内容中心 (SEO & Platform Content Center)

**定位**: 为各平台自动生成优化内容。

#### 4.3.1 平台覆盖

| 平台 | 生成内容 | 说明 |
|------|----------|------|
| Alibaba国际站 | SEO标题、产品详情页、关键词 | 128字符标题 + 完整详情页 |
| 独立站 | Product Description、Meta Title、Meta Description | SEO优化描述 |
| Facebook | 产品推广文案 + 配图建议 | 适合FB帖子 |
| LinkedIn | 专业推广文案 | B2B风格 |
| WhatsApp | 推广消息模板 | 适合群发/私聊 |

#### 4.3.2 生成流程

```
产品数据 (SQLite)
    + 关键词库 (keyword_database)
    + 市场知识库 (market_knowledge)
    ────────────────────────
    → AI Prompt组装
    → LLM调用
    → 格式化输出
    → 保存到SQLite + 导出文件
```

#### 4.3.3 数据表

```sql
-- 内容生成记录表
CREATE TABLE content_records (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    product_code    TEXT REFERENCES products(product_code),
    content_type    TEXT NOT NULL,     -- seo_title / detail_page / facebook / linkedin / whatsapp
    platform        TEXT,              -- alibaba / website / facebook / linkedin / whatsapp
    target_market   TEXT,              -- global / nigeria / kenya / ...
    content         TEXT,              -- 生成的内容
    version         INTEGER DEFAULT 1, -- 版本号
    status          TEXT DEFAULT 'draft', -- draft / reviewed / published
    created_at      TEXT DEFAULT (datetime('now')),
    reviewed_at     TEXT               -- 审核时间
);
```

---

### M4: AI市场研究Agent (Market Research Agent)

**定位**: 输入国家+产品，自动生成市场研究报告。

#### 4.4.1 输入

```
国家: Liberia
产品: Shovel / Hoe / Rake
```

#### 4.4.2 输出报告结构

```markdown
# Liberia — Garden Shovel Market Report
# 利比里亚 — 园艺铲市场研究报告

## 1. 市场概况 (Market Overview)
- 人口 / GDP / 农业占比
- 主要农业区域
- 农具市场规模估计

## 2. 农业情况 (Agriculture Profile)
- 主要作物类型
- 耕作方式（机械化程度）
- 小规模农场 vs 大型农场比例
- 季节性需求

## 3. 常用工具类型 (Common Tool Types)
- 当地最常用的铲/锄/耙类型
- 偏好特征（重量、材质、手柄）
- 价格敏感度

## 4. 产品偏好 (Product Preferences)
- 欧洲风格 vs 亚洲风格
- 重型 vs 轻型
- 木柄 vs 铁柄 vs 玻璃纤维柄
- 包装偏好

## 5. 进口情况 (Import Situation)
- 主要进口来源国
- 关税政策
- 认证要求
- 主要港口和物流

## 6. 竞争品牌 (Competitive Landscape)
- 当地主要品牌
- 中国品牌情况
- 印度品牌情况
- 价格区间对比

## 7. 进入建议 (Market Entry Recommendations)
- 推荐产品线
- 定价策略
- 渠道建议
- 风险提示
```

#### 4.4.3 技术实现

```
Web搜索 (Serper / Google Custom Search API)
    → 数据抓取和整理 (Python + BeautifulSoup)
    → AI分析和报告生成 (LLM API)
    → 输出 Markdown + PDF
    → 存储到 market_reports 表
```

#### 4.4.4 数据表

```sql
-- 市场报告表
CREATE TABLE market_reports (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    country         TEXT NOT NULL,
    product_category TEXT,
    report_title    TEXT,
    summary         TEXT,              -- 200字摘要
    full_report     TEXT,              -- 完整Markdown
    report_file     TEXT,              -- PDF文件路径
    data_sources    TEXT,              -- JSON: 数据来源列表
    confidence      TEXT,              -- high / medium / low
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

-- 市场知识表（累积的市场洞察）
CREATE TABLE market_knowledge (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    country         TEXT NOT NULL,
    category        TEXT,              -- agriculture / import / competitor / pricing
    knowledge       TEXT,              -- 知识点
    source          TEXT,              -- 来源
    verified        BOOLEAN DEFAULT 0, -- 是否已验证
    created_at      TEXT DEFAULT (datetime('now'))
);
```

---

### M5: AI客户分析Agent (Client Analysis Agent)

**定位**: 分析潜在客户，自动评级并给出跟进策略。

#### 4.5.1 输入

```
公司名称: ABC Agricultural Supplies Ltd.
公司网址: https://www.example.com
（可选）LinkedIn页面
（可选）已知的联系信息
```

#### 4.5.2 输出

```markdown
# Client Profile: ABC Agricultural Supplies Ltd.

## 基本信息
- 国家: Kenya
- 成立时间: 2015
- 员工规模: 50-200人
- 网站: https://www.example.com

## 主营业务
- 农业工具批发与零售
- 主要品类: Garden Tools, Farm Equipment
- 销售渠道: 线下批发 + 线上零售

## 市场区域
- 主要市场: Kenya (内罗毕、蒙巴萨)
- 扩展市场: Tanzania, Uganda

## 潜在采购产品
- Garden Hoe (高匹配)
- Garden Fork (中匹配)
- Pruning Shears (低匹配)

## 客户评级: B+ (潜力客户)

### 评分维度
| 维度 | 分数 | 说明 |
|------|------|------|
| 业务匹配度 | 8/10 | 产品线高度重合 |
| 采购能力 | 7/10 | 中型批发商，有一定采购量 |
| 市场覆盖 | 6/10 | 主要在Kenya，东非有覆盖 |
| 在线可见度 | 7/10 | 有网站和社交媒体 |

## 跟进建议
1. 首封邮件重点介绍Garden Hoe产品线
2. 附上产品目录PDF
3. 提供样品报价
4. 2周后跟进WhatsApp
```

#### 4.5.3 客户分级标准

| 等级 | 标准 | 跟进策略 |
|------|------|----------|
| A级 | 大型进口商/批发商，产品线高度匹配，有明显采购需求 | 优先跟进，定制方案，样品优先 |
| B级 | 中型经销商，有一定匹配度，可能有采购需求 | 标准开发信 + 产品目录，定期跟进 |
| C级 | 小型零售商，匹配度一般，采购量不确定 | 群发式开发，低成本维护 |

#### 4.5.4 数据表

```sql
-- 客户表
CREATE TABLE clients (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name    TEXT NOT NULL,
    country         TEXT,
    website         TEXT,
    contact_person  TEXT,
    email           TEXT,
    phone           TEXT,
    whatsapp        TEXT,
    linkedin        TEXT,
    business_type   TEXT,              -- wholesaler / retailer / distributor / importer
    main_products   TEXT,              -- JSON array
    market_regions  TEXT,              -- JSON array
    estimated_volume TEXT,             -- small / medium / large
    grade           TEXT,              -- A / B / C (+/- suffix)
    grade_score     INTEGER,           -- 0-100
    source          TEXT,              -- google / alibaba / exhibition / referral / linkedin
    notes           TEXT,              -- 备注
    status          TEXT DEFAULT 'prospect', -- prospect / contacted / negotiating / customer / lost
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

-- 客户分析记录
CREATE TABLE client_analyses (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id       INTEGER REFERENCES clients(id),
    analysis_type   TEXT,              -- initial / update
    summary         TEXT,              -- 分析摘要
    full_analysis   TEXT,              -- 完整分析报告
    grade_suggested TEXT,              -- AI建议评级
    recommendations TEXT,              -- 跟进建议
    created_at      TEXT DEFAULT (datetime('now'))
);
```

---

### M6: 开发信与跟进Agent (Outreach & Follow-up Agent)

**定位**: 根据不同场景自动生成开发信和跟进消息。

#### 4.6.1 支持的场景

| 场景 | 渠道 | 风格选项 |
|------|------|----------|
| 首封开发信 | Email | 正式 / 简洁 / 关系型 |
| WhatsApp开发消息 | WhatsApp | 简洁 / 友好 / 直接 |
| LinkedIn开发消息 | LinkedIn | 专业 / 社交化 |
| 跟进邮件 | Email | 温和跟进 /  urgency / 价值补充 |
| 展会后跟进 | Email / WhatsApp | 回忆型 / 报价型 |
| 报价后跟进 | Email | 催单型 / 方案调整型 |

#### 4.6.2 输入参数

```json
{
    "client_info": {
        "company": "ABC Agricultural Supplies",
        "country": "Kenya",
        "contact_person": "John Smith",
        "grade": "B+"
    },
    "products": ["GF-001", "GS-001"],
    "scenario": "initial_outreach",
    "channel": "email",
    "style": "professional",
    "language": "en"
}
```

#### 4.6.3 输出

- 邮件正文（HTML + 纯文本）
- 邮件标题（3个变体）
- WhatsApp消息文本
- LinkedIn消息文本

#### 4.6.4 数据表

```sql
-- 联系记录表
CREATE TABLE activities (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id       INTEGER REFERENCES clients(id),
    activity_type   TEXT NOT NULL,     -- email / whatsapp / linkedin / call / meeting
    direction       TEXT,              -- outbound / inbound
    subject         TEXT,              -- 主题
    content         TEXT,              -- 内容
    status          TEXT,              -- sent / replied / no_reply / meeting_scheduled
    scheduled_date  TEXT,              -- 计划日期
    actual_date     TEXT,              -- 实际日期
    follow_up_date  TEXT,              -- 下次跟进日期
    notes           TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- 开发信模板表
CREATE TABLE outreach_templates (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    scenario        TEXT,              -- initial / follow_up / post_exhibition / quotation_followup
    channel         TEXT,              -- email / whatsapp / linkedin
    style           TEXT,              -- professional / casual / relationship
    template_body   TEXT,              -- 模板正文（含变量占位符）
    subject_line    TEXT,              -- 邮件标题模板
    usage_count     INTEGER DEFAULT 0,
    success_rate    REAL,              -- 回复率
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);
```

---

### M7: 报价辅助Agent (Quotation Assistant Agent)

**定位**: 快速生成专业报价单和报价邮件。

#### 4.7.1 输入

```json
{
    "product_code": "GF-001",
    "quantity": 1000,
    "country": "Kenya",
    "incoterm": "FOB",               // FOB / CIF / EXW
    "currency": "USD",               // USD / EUR
    "payment_terms": "T/T 30% deposit, 70% before shipment",
    "validity_days": 30
}
```

#### 4.7.2 输出

| 输出项 | 说明 |
|--------|------|
| 产品参数摘要 | 自动从数据库提取 |
| 参考价格 | 基于成本+利润率的计算 |
| 装柜量 | 20'/40'/40HQ的装载数量 |
| 报价邮件模板 | 专业报价邮件正文 |
| 报价单 (Quotation) | 正式报价单PDF/Excel |

#### 4.7.3 数据表

```sql
-- 报价表
CREATE TABLE quotations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    quotation_no    TEXT UNIQUE,       -- QT-2026-0001
    client_id       INTEGER REFERENCES clients(id),
    product_code    TEXT REFERENCES products(product_code),
    quantity        INTEGER,
    unit_price      REAL,
    currency        TEXT DEFAULT 'USD',
    incoterm        TEXT,              -- FOB / CIF / EXW
    port            TEXT,              -- Tianjin / Shanghai
    payment_terms   TEXT,
    lead_time_days  INTEGER,
    validity_days   INTEGER,
    total_amount    REAL,
    email_body      TEXT,              -- 报价邮件正文
    quotation_file  TEXT,              -- 报价单文件路径
    status          TEXT DEFAULT 'draft', -- draft / sent / negotiated / accepted / rejected / expired
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

-- 价格记录表（用于分析价格趋势）
CREATE TABLE price_records (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    product_code    TEXT REFERENCES products(product_code),
    base_price_usd  REAL,              -- 基础出厂价
    min_price_usd   REAL,              -- 最低可接受价
    target_market   TEXT,
    effective_date  TEXT,
    notes           TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);
```

---

### M8: 客户CRM数据库 (Customer CRM)

**定位**: 统一管理所有客户信息和交互历史。

#### 4.8.1 核心功能

| 功能 | 说明 |
|------|------|
| 客户搜索 | 按名称/国家/等级/状态搜索 |
| 客户标签 | 自定义标签管理（如"展会认识"、"阿里询盘"） |
| 联系历史 | 查看所有联系记录（邮件/WhatsApp/电话） |
| 跟进提醒 | 设置下次跟进日期，到期提醒 |
| 客户看板 | 按国家/等级/状态统计 |
| 客户导入 | 从Excel/CSV批量导入 |
| 客户导出 | 导出为Excel/CSV |

#### 4.8.2 数据模型

（已在M5和M6中定义了clients、activities、client_analyses表）

补充：

```sql
-- 客户标签表
CREATE TABLE client_tags (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT UNIQUE NOT NULL,
    color           TEXT,              -- 标签颜色
    description     TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- 客户-标签关联表
CREATE TABLE client_tag_mapping (
    client_id       INTEGER REFERENCES clients(id),
    tag_id          INTEGER REFERENCES client_tags(id),
    PRIMARY KEY (client_id, tag_id)
);

-- 询盘记录表
CREATE TABLE inquiries (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id       INTEGER REFERENCES clients(id),
    product_code    TEXT,
    inquiry_source  TEXT,              -- alibaba / email / whatsapp / website / exhibition
    inquiry_content TEXT,
    quantity_requested INTEGER,
    target_price    REAL,
    status          TEXT DEFAULT 'new', -- new / quoted / negotiating / closed
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

-- 成交记录表
CREATE TABLE orders (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id       INTEGER REFERENCES clients(id),
    order_no        TEXT UNIQUE,
    products        TEXT,              -- JSON: [{product_code, quantity, price}]
    total_amount    REAL,
    currency        TEXT DEFAULT 'USD',
    order_date      TEXT,
    delivery_date   TEXT,
    status          TEXT DEFAULT 'pending', -- pending / confirmed / shipped / delivered
    notes           TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);
```

---

### M9: 数据运营分析中心 (Data Operations & Analytics)

**定位**: 多维度数据分析，辅助业务决策。

#### 4.9.1 分析维度

**产品维度：**
- 热门产品（询盘次数最多的产品）
- 高成交产品（成交率最高的产品）
- 产品类别分布
- 产品关键词热度

**客户维度：**
- 客户国家分布
- 客户等级分布
- 各等级成交率
- 客户来源渠道效果

**市场维度：**
- 国家机会分析（综合询盘量、成交率、市场规模）
- 产品需求趋势（哪些产品在哪些国家需求增长）
- 价格趋势分析

#### 4.9.2 输出

| 报表类型 | 格式 | 说明 |
|----------|------|------|
| 仪表盘 (Dashboard) | HTML (Streamlit) | 交互式可视化 |
| 周报/月报 | PDF | 定期自动生成的业务报告 |
| 自定义分析 | 图表 + 表格 | 按需生成的分析报告 |

#### 4.9.3 技术实现

```
SQLite数据库
    → Pandas数据提取和计算
    → Plotly/Altair可视化
    → Streamlit仪表盘
    → 或导出为静态图表
```

#### 4.9.4 数据表

```sql
-- 分析视图（由现有表聚合生成，可选物化）
-- 产品热度统计
CREATE VIEW product_stats AS
SELECT
    p.product_code,
    p.product_name_en,
    p.category,
    COUNT(DISTINCT i.id) as inquiry_count,
    COUNT(DISTINCT q.id) as quotation_count,
    COUNT(DISTINCT o.id) as order_count,
    CASE WHEN COUNT(DISTINCT i.id) > 0
         THEN CAST(COUNT(DISTINCT o.id) AS REAL) / COUNT(DISTINCT i.id)
         ELSE 0 END as conversion_rate
FROM products p
LEFT JOIN inquiries i ON p.product_code = i.product_code
LEFT JOIN quotations q ON p.product_code = q.product_code
LEFT JOIN orders o ON p.product_code LIKE '%' || o.products || '%'
GROUP BY p.product_code;

-- 客户统计
CREATE VIEW client_stats AS
SELECT
    c.country,
    c.grade,
    c.status,
    COUNT(DISTINCT c.id) as client_count,
    COUNT(DISTINCT CASE WHEN c.status = 'customer' THEN c.id END) as converted_count,
    COUNT(DISTINCT i.id) as total_inquiries,
    COUNT(DISTINCT o.id) as total_orders,
    COALESCE(SUM(o.total_amount), 0) as total_revenue
FROM clients c
LEFT JOIN inquiries i ON c.id = i.client_id
LEFT JOIN orders o ON c.id = o.client_id
GROUP BY c.country, c.grade, c.status;
```

---

## 五、完整数据库设计

### 5.1 数据库文件

```
data/ft_workspace.db    — 主SQLite数据库
```

### 5.2 表关系图

```
┌────────────┐     1:N      ┌──────────────┐     1:N      ┌──────────────┐
│  products  │────────────→│ inquiries    │←────────────│   clients    │
│  (产品表)   │     1:N      │  (询盘表)     │     1:N      │  (客户表)     │
└─────┬──────┘              └──────────────┘              └──────┬───────┘
      │ 1:N                                        1:N │         │ 1:N
      │ ↓                                              │         │ ↓
      │ ┌──────────────┐                    ┌───────────┴──┐  ┌──────────┐
      │ │content_records│                    │  activities  │  │  orders  │
      │ │(内容记录表)    │                    │ (联系记录表)  │  │ (成交表)  │
      │ └──────────────┘                    └──────────────┘  └──────────┘
      │ 1:N                                                      │
      │ ↓                                                        │
      │ ┌──────────────┐                    ┌──────────────────┐ │
      └─│ quotations   │                    │ client_analyses  │←┘
        │  (报价表)     │                    │  (客户分析表)     │
        └──────────────┘                    └──────────────────┘
                                                    │
        ┌──────────────┐     ┌──────────────┐       │
        │market_reports│     │market_knowledge│      │
        │ (市场报告表)  │     │ (市场知识表)   │      │
        └──────────────┘     └──────────────┘       │
                                                    │
        ┌──────────────┐     ┌─────────────────┐    │
        │outreach_templates│ │  client_tags    │    │
        │ (开发信模板表)  │    │  (标签表)        │    │
        └──────────────┘     └────────┬────────┘    │
                                     │ 1:N          │
                                     │ ↓            │
                          ┌─────────────────────┐   │
                          │client_tag_mapping   │   │
                          │(客户-标签关联表)      │   │
                          └─────────────────────┘   │
```

### 5.3 数据库初始化脚本

```sql
-- schema.sql: 完整数据库初始化脚本
-- 详见: data/schema.sql

-- 核心表: products, clients, activities, inquiries, quotations, orders
-- 辅助表: product_images, market_reports, market_knowledge,
--         client_analyses, outreach_templates, client_tags,
--         client_tag_mapping, price_records, content_records

-- 视图: product_stats, client_stats, market_opportunity
```

---

## 六、Agent设计

### 6.1 Agent架构

```
┌─────────────────────────────────────────────────────────┐
│                    Orchestrator                          │
│         (工作流编排器 - Dify / n8n / Python)             │
└──────────────┬──────────────┬──────────────┬────────────┘
               │              │              │
    ┌──────────┴──────┐ ┌─────┴───────┐ ┌───┴──────────┐
    │Market Research  │ │Client       │ │Content       │
    │Agent            │ │Analysis     │ │Generator     │
    │(市场研究)        │ │Agent        │ │Agent         │
    │                 │ │(客户分析)    │ │(内容生成)     │
    │ Input: 国家+产品 │ │ Input: 公司  │ │ Input: 产品  │
    │ Output: 报告     │ │ Output: 评级 │ │ Output: 文案  │
    └─────────────────┘ └─────────────┘ └──────────────┘
               │              │              │
    ┌──────────┴──────┐ ┌─────┴───────┐ ┌───┴──────────┐
    │Quotation        │ │Outreach     │ │Data          │
    │Agent            │ │Agent        │ │Analytics     │
    │(报价辅助)        │ │(开发信)     │ │Agent         │
    │                 │ │(跟进)       │ │(数据分析)     │
    │ Input: 产品+数量 │ │ Input: 客户 │ │ Input: 数据库 │
    │ Output: 报价单   │ │ Output: 邮件 │ │ Output: 报表  │
    └─────────────────┘ └─────────────┘ └──────────────┘

所有Agent共享 → SQLite数据库 (统一数据源)
所有Agent使用 → LLM API (OpenAI / Claude / Gemini / Qwen)
```

### 6.2 Agent详细设计

#### Agent 1: Market Research Agent

```yaml
name: market_research_agent
description: 自动生成目标市场研究报告
trigger:
  - manual: 用户输入国家+产品
  - scheduled: 每周自动研究重点国家
input:
  country: string (required)
  product_category: string (required)
  depth: string (basic / detailed)  # 报告深度
process:
  1. Web搜索: 收集目标国家农业、进口、竞品信息
  2. 数据整理: 结构化搜索结果
  3. AI分析: 生成市场洞察和进入建议
  4. 报告生成: Markdown + PDF
  5. 知识入库: 提取关键知识点存入market_knowledge表
output:
  - markdown_report: str
  - pdf_report: file_path
  - knowledge_entries: list
tools:
  - web_search
  - web_scrape
  - llm_api
  - file_write
```

#### Agent 2: Client Analysis Agent

```yaml
name: client_analysis_agent
description: 分析潜在客户并自动评级
trigger:
  - manual: 用户输入公司信息
  - workflow: 从Alibaba询盘自动触发
input:
  company_name: string (required)
  website: string (optional)
  linkedin_url: string (optional)
  known_info: dict (optional)
process:
  1. 信息搜集: 搜索公司官网、LinkedIn、新闻
  2. 业务分析: 判断主营业务、产品线匹配度
  3. 市场评估: 评估客户市场覆盖和采购能力
  4. 评级打分: 多维度评分
  5. 策略建议: 生成跟进策略
  6. 数据入库: 写入clients和client_analyses表
output:
  - client_profile: dict
  - grade: string (A/B/C with +/-)
  - grade_score: int (0-100)
  - recommendations: list
  - matched_products: list
tools:
  - web_search
  - web_scrape
  - llm_api
  - sqlite_write
```

#### Agent 3: Content Generator Agent

```yaml
name: content_generator_agent
description: 生成各平台营销内容
trigger:
  - manual: 用户选择产品+平台
  - batch: 批量生成（选多个产品）
  - scheduled: 新产品上架自动生成
input:
  product_codes: list (required)
  platforms: list (required)  # [alibaba, website, facebook, linkedin, whatsapp]
  target_market: string (optional)
  language: string (default: en)
process:
  1. 读取产品数据 (SQLite)
  2. 加载知识库 (product_knowledge + market_knowledge)
  3. 组装Prompt (按平台模板)
  4. 调用LLM生成
  5. 格式化和质量检查
  6. 保存到content_records表
  7. 导出文件
output:
  - seo_titles: list
  - detail_pages: markdown
  - social_posts: dict
  - content_records: db_entries
tools:
  - sqlite_read
  - llm_api
  - template_engine
  - file_write
  - sqlite_write
```

#### Agent 4: Outreach Agent

```yaml
name: outreach_agent
description: 生成开发信和跟进消息
trigger:
  - manual: 用户选择客户+场景
  - scheduled: 跟进提醒自动触发
input:
  client_id: int (required)
  scenario: string (initial / follow_up / post_exhibition / quotation_followup)
  channel: string (email / whatsapp / linkedin)
  style: string (professional / casual / relationship)
  product_codes: list (optional)
process:
  1. 读取客户信息 (SQLite)
  2. 读取联系历史 (activities表)
  3. 加载对应模板 (outreach_templates)
  4. AI个性化生成
  5. 质量检查
  6. 返回生成内容
  7. (可选) 记录到activities表
output:
  - subject_lines: list (email only)
  - body: string
  - body_html: string (email only)
  - follow_up_date: string
tools:
  - sqlite_read
  - llm_api
  - template_engine
  - sqlite_write
```

#### Agent 5: Quotation Agent

```yaml
name: quotation_agent
description: 辅助生成报价单和报价邮件
trigger:
  - manual: 用户输入报价参数
  - workflow: 询盘转报价时自动触发
input:
  product_code: string (required)
  quantity: int (required)
  client_id: int (optional)
  country: string (optional)
  incoterm: string (FOB / CIF / EXW)
  currency: string (USD / EUR)
process:
  1. 读取产品参数 (products表)
  2. 读取价格记录 (price_records表)
  3. 计算装柜量
  4. 计算总价和单价
  5. 生成报价邮件模板
  6. 生成报价单 (PDF/Excel)
  7. 保存到quotations表
output:
  - quotation_record: db_entry
  - quotation_file: file_path (PDF/Excel)
  - email_body: string
  - loading_info: dict
tools:
  - sqlite_read
  - calculator
  - llm_api
  - file_write (PDF/Excel generation)
  - sqlite_write
```

---

## 七、技术架构

### 7.1 技术栈选型

| 层次 | 技术 | 选型理由 |
|------|------|----------|
| 语言 | Python 3.11+ | 生态丰富，AI/数据工具链完善 |
| 数据库 | SQLite | 零配置，单文件，适合个人使用 |
| 数据处理 | Pandas | CSV/Excel处理标准库 |
| 文档生成 | python-docx, FPDF2, python-pptx | 纯Python，无外部依赖 |
| LLM API | OpenAI / Claude / Gemini / Qwen | 多Provider支持，可按需切换 |
| Web框架 | Streamlit | 快速构建数据仪表盘，零前端代码 |
| 工作流 | Dify / n8n (后续) | 可视化Agent工作流编排 |
| 搜索 | Serper API / Google Custom Search | 市场研究数据源 |
| 任务调度 | APScheduler / Cron | 定时任务 |
| 配置管理 | YAML + python-dotenv | 敏感信息隔离 |

### 7.2 系统架构图

```
┌──────────────────────────────────────────────────────────────┐
│                        用户界面层                              │
│  ┌────────────┐  ┌────────────┐  ┌─────────────────────────┐ │
│  │ CLI工具     │  │Streamlit UI│  │ 直接调用 (Hermes/API)    │ │
│  │ (ft CLI)   │  │ (仪表盘)   │  │                         │ │
│  └──────┬─────┘  └──────┬─────┘  └────────────┬────────────┘ │
└─────────┼───────────────┼─────────────────────┼───────────────┘
          │               │                     │
┌─────────▼───────────────▼─────────────────────▼───────────────┐
│                        应用服务层                               │
│                                                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│  │ M1 产品  │ │ M2 营销  │ │ M3 SEO   │ │ M4 市场  │         │
│  │ 数据库   │ │ 资料生成  │ │ 内容中心  │ │ 研究Agent │         │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│  │ M5 客户  │ │ M6 开发信 │ │ M7 报价  │ │ M8 CRM   │         │
│  │ 分析Agent │ │ 跟进Agent │ │ 辅助Agent │ │ 数据库   │         │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘         │
│  ┌──────────────────────────────────┐                        │
│  │ M9 数据运营分析中心                 │                        │
│  └──────────────────────────────────┘                        │
│                                                               │
│  ┌──────────────────────────────────┐                        │
│  │        核心服务 (Core Services)    │                        │
│  │  - LLM Client (多Provider)       │                        │
│  │  - Template Engine (Jinja2)      │                        │
│  │  - Document Generator            │                        │
│  │  - Web Search Client             │                        │
│  │  - Export Service (PDF/Excel)    │                        │
│  └──────────────────────────────────┘                        │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│                        数据层                                  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              SQLite Database (ft_workspace.db)         │    │
│  │  products | clients | activities | inquiries          │    │
│  │  quotations | orders | market_reports | content       │    │
│  │  market_knowledge | client_analyses | outreach_templates│   │
│  └──────────────────────────────────────────────────────┘    │
│                                                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐    │
│  │ CSV/Excel   │ │ 产品图片    │ │ 生成文件            │    │
│  │ 导入导出     │ │ assets/    │ │ output/             │    │
│  └─────────────┘ └─────────────┘ └─────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│                        外部服务                                │
│                                                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │OpenAI API│ │Claude API│ │Gemini API│ │Qwen API  │        │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                     │
│  │Serper API│ │Google CS │ │ Dify/n8n │ (后续集成)           │
│  └──────────┘ └──────────┘ └──────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

### 7.3 模块依赖关系

```
M1 (产品数据库) ───→ 所有模块的依赖（数据基石）
M2 (营销资料) ─────→ M1 + LLM + 文档生成
M3 (SEO内容) ─────→ M1 + LLM + 关键词库
M4 (市场研究) ─────→ Web搜索 + LLM → M9数据源
M5 (客户分析) ─────→ Web搜索 + LLM → M8数据源
M6 (开发信) ───────→ M8(CRM) + LLM + 模板
M7 (报价) ─────────→ M1 + M8 + 文档生成
M8 (CRM) ──────────→ 核心数据库
M9 (数据分析) ─────→ M1 + M4 + M5 + M6 + M7 + M8 (聚合所有数据)
```

---

## 八、文件目录结构

### 8.1 v2.0 项目目录

```
ai-foreign-trade-automation/
│
├── config/                           # 配置文件
│   ├── settings.yaml                 # 系统配置 (LLM API, paths, defaults)
│   ├── .env                          # 敏感信息 (API keys, passwords)
│   └── field_mapping.yaml            # 产品字段映射定义
│
├── data/                             # 数据层
│   ├── ft_workspace.db               # SQLite主数据库
│   ├── schema.sql                    # 数据库建表脚本
│   ├── seed_data.sql                 # 种子数据 (从v1.0 CSV迁移)
│   ├── imports/                      # 待导入的CSV/Excel文件
│   │   ├── products/                 # 产品数据导入
│   │   └── clients/                  # 客户数据导入
│   └── backups/                      # 数据库备份
│
├── src/                              # 源代码
│   ├── __init__.py
│   │
│   ├── core/                         # 核心服务
│   │   ├── __init__.py
│   │   ├── database.py               # SQLite连接和操作封装
│   │   ├── llm_client.py             # 多LLM Provider客户端
│   │   ├── config.py                 # 配置管理
│   │   └── logger.py                 # 日志
│   │
│   ├── models/                       # 数据模型 (Pydantic)
│   │   ├── __init__.py
│   │   ├── product.py                # Product模型
│   │   ├── client.py                 # Client模型
│   │   ├── activity.py               # Activity模型
│   │   ├── quotation.py              # Quotation模型
│   │   └── report.py                 # Report模型
│   │
│   ├── m1_product_db/                # M1: 产品数据库系统
│   │   ├── __init__.py
│   │   ├── importer.py               # CSV/Excel导入
│   │   ├── cleaner.py                # 数据清洗
│   │   ├── ai_completer.py           # AI信息补全
│   │   ├── search.py                 # 搜索与筛选
│   │   └── exporter.py               # 数据导出
│   │
│   ├── m2_marketing/                 # M2: AI产品营销资料生成器
│   │   ├── __init__.py
│   │   ├── catalog_generator.py      # Catalog生成
│   │   ├── product_sheet.py          # 单页产品卡
│   │   ├── market_localizer.py       # 市场定制版
│   │   └── ppt_generator.py          # PPT生成
│   │
│   ├── m3_seo/                       # M3: AI SEO与平台内容中心
│   │   ├── __init__.py
│   │   ├── alibaba_generator.py      # 阿里内容生成
│   │   ├── website_generator.py      # 独立站内容
│   │   └── social_generator.py       # 社交媒体内容
│   │
│   ├── m4_market_research/           # M4: AI市场研究Agent
│   │   ├── __init__.py
│   │   ├── web_scraper.py            # 网页数据采集
│   │   ├── report_generator.py       # 报告生成
│   │   └── knowledge_extractor.py    # 知识提取入库
│   │
│   ├── m5_client_analysis/           # M5: AI客户分析Agent
│   │   ├── __init__.py
│   │   ├── company_scraper.py        # 公司信息搜集
│   │   ├── grader.py                 # 客户评级
│   │   └── advisor.py                # 策略建议
│   │
│   ├── m6_outreach/                  # M6: 开发信与跟进Agent
│   │   ├── __init__.py
│   │   ├── template_manager.py       # 模板管理
│   │   ├── email_generator.py        # 邮件生成
│   │   ├── whatsapp_generator.py     # WhatsApp消息
│   │   └── linkedin_generator.py     # LinkedIn消息
│   │
│   ├── m7_quotation/                 # M7: 报价辅助Agent
│   │   ├── __init__.py
│   │   ├── calculator.py             # 价格和装柜计算
│   │   ├── email_generator.py        # 报价邮件
│   │   └── document_generator.py     # 报价单生成
│   │
│   ├── m8_crm/                       # M8: 客户CRM数据库
│   │   ├── __init__.py
│   │   ├── client_manager.py         # 客户管理
│   │   ├── activity_tracker.py       # 联系记录
│   │   ├── tag_manager.py            # 标签管理
│   │   └── reminder.py               # 跟进提醒
│   │
│   ├── m9_analytics/                 # M9: 数据运营分析中心
│   │   ├── __init__.py
│   │   ├── product_analytics.py      # 产品维度分析
│   │   ├── client_analytics.py       # 客户维度分析
│   │   ├── market_analytics.py       # 市场维度分析
│   │   └── dashboard_data.py         # 仪表盘数据准备
│   │
│   ├── agents/                       # Agent编排层
│   │   ├── __init__.py
│   │   ├── base_agent.py             # Agent基类
│   │   ├── market_research_agent.py  # 市场研究Agent
│   │   ├── client_analysis_agent.py  # 客户分析Agent
│   │   ├── content_generator_agent.py# 内容生成Agent
│   │   ├── outreach_agent.py         # 开发信Agent
│   │   └── quotation_agent.py        # 报价Agent
│   │
│   └── utils/                        # 工具函数
│       ├── __init__.py
│       ├── prompts.py                # Prompt模板管理
│       ├── formatters.py             # 格式化工具
│       └── validators.py             # 数据验证
│
├── prompts/                          # AI提示词模板
│   ├── market_research/              # 市场研究Prompt
│   │   ├── basic_report.md
│   │   └── detailed_report.md
│   ├── client_analysis/              # 客户分析Prompt
│   ├── seo/                          # SEO内容Prompt
│   │   ├── alibaba_title.md
│   │   ├── alibaba_detail.md
│   │   ├── website_meta.md
│   │   └── website_description.md
│   ├── social/                       # 社交媒体Prompt
│   │   ├── facebook.md
│   │   ├── linkedin.md
│   │   └── whatsapp.md
│   ├── outreach/                     # 开发信Prompt
│   │   ├── initial_email.md
│   │   ├── follow_up_email.md
│   │   ├── whatsapp_outreach.md
│   │   └── linkedin_outreach.md
│   ├── quotation/                    # 报价Prompt
│   │   └── quotation_email.md
│   └── system/                       # 系统级Prompt
│       └── knowledge_injection.md    # 知识库注入模板
│
├── templates/                        # 文档模板
│   ├── catalog/                      # 产品目录模板
│   │   ├── single_product.docx
│   │   ├── multi_product.docx
│   │   └── catalog.pdf.j2
│   ├── quotation/                    # 报价单模板
│   │   └── quotation.xlsx.j2
│   └── reports/                      # 报告模板
│       └── market_report.md.j2
│
├── output/                           # 输出文件
│   ├── catalogs/                     # 生成的产品目录
│   ├── quotations/                   # 生成的报价单
│   ├── reports/                      # 市场研究报告
│   ├── seo_content/                  # SEO内容
│   ├── outreach/                     # 开发信
│   └── exports/                      # 导出数据
│
├── assets/                           # 静态资源
│   ├── images/                       # 产品图片
│   │   ├── main/                     # 主图
│   │   ├── detail/                   # 详情图
│   │   └── scenes/                   # 场景图
│   ├── logos/                        # Logo
│   └── fonts/                        # 字体
│
├── ui/                               # 用户界面
│   └── streamlit_app.py              # Streamlit仪表盘
│
├── scripts/                          # 脚本
│   ├── migrate_v1_to_v2.py           # v1.0数据迁移脚本
│   ├── init_db.py                    # 数据库初始化
│   └── backup_db.py                  # 数据库备份
│
├── tests/                            # 测试
│   ├── test_product_db.py
│   ├── test_llm_client.py
│   ├── test_agents.py
│   └── fixtures/
│
├── docs/                             # 文档
│   ├── api_reference.md              # API文档
│   ├── user_guide.md                 # 用户指南
│   ├── agent_design.md               # Agent设计文档
│   └── migration_guide.md            # v1→v2迁移指南
│
├── legacy/                           # v1.0历史文件（保留参考）
│   ├── 00-config/
│   ├── 01-input/
│   ├── 02-prompts/
│   ├── 03-workflows/
│   ├── 04-database/
│   ├── 05-output/
│   ├── 06-assets/
│   ├── 07-docs/
│   ├── 08-git/
│   └── 项目说明文档.md
│
├── requirements.txt                  # Python依赖
├── pyproject.toml                    # 项目配置
└── README.md                         # 项目说明（英文）
```

### 8.2 目录迁移策略

v1.0目录 → v2.0目录映射：

| v1.0 路径 | v2.0 路径 | 说明 |
|-----------|-----------|------|
| 00-config/ | config/ | 配置文件迁移 |
| 01-input/ | data/imports/ | 原始输入保留 |
| 02-prompts/ | prompts/ | 提示词重组 |
| 03-workflows/ | src/agents/ + scripts/ | 工作流升级为Agent |
| 04-database/ | data/ + src/m1_product_db/ | 数据库升级为SQLite |
| 05-output/ | output/ | 输出目录重组 |
| 06-assets/ | assets/ | 资源目录保留 |
| 07-docs/ | docs/ | 文档整理 |
| 08-git/ | README.md | 合并到根目录 |

---

## 九、开发路线图

### 9.1 总览

```
Phase 1 (MVP)          Phase 2 (增强)           Phase 3 (智能)
Week 1-3               Week 4-6                 Week 7-10
───────────────────    ────────────────────     ────────────────────
数据库基础              Agent工作流               Dify/n8n集成
产品管理 (M1)          市场研究 (M4)             自动化pipeline
CRM基础 (M8)           客户分析 (M5)             数据仪表盘 (M9)
内容生成 (M2+M3)       开发信 (M6)               智能推荐
报价辅助 (M7)          Streamlit UI             定时任务
```

---

## 十、MVP版本规划 (Phase 1: Week 1-3)

### 目标：跑通核心数据流

```
产品导入 → 产品管理 → 内容生成 → 文件导出
```

### Week 1: 基础设施 + 产品数据库

| 天 | 任务 | 交付物 |
|----|------|--------|
| D1 | 项目初始化、创建v2.0目录结构 | 新目录树 |
| D1 | 数据库schema设计 + 建表脚本 | data/schema.sql |
| D2 | core/database.py — SQLite封装 | 数据库操作模块 |
| D2 | core/config.py — 配置管理 | settings.yaml + .env |
| D3 | core/llm_client.py — LLM客户端 | 支持Qwen/OpenAI |
| D3 | m1_product_db/importer.py — CSV/Excel导入 | 导入脚本 |
| D4 | m1_product_db/cleaner.py — 数据清洗 | 清洗模块 |
| D4 | 迁移脚本: v1.0 CSV → v2.0 SQLite | 215条产品入库 |
| D5 | m1_product_db/search.py — 搜索与筛选 | 搜索功能 |
| D5 | m1_product_db/exporter.py — 数据导出 | 导出功能 |
| D6-7 | 测试 + 文档 | 测试报告 |

**MVP Milestone 1**: 产品数据库可用，215个SKU从CSV迁移到SQLite，支持搜索/筛选/导入/导出。

### Week 2: 内容生成 + 营销资料

| 天 | 任务 | 交付物 |
|----|------|--------|
| D8 | prompts/重组 — 迁移v1.0提示词 | 结构化Prompt库 |
| D8 | utils/prompts.py — Prompt模板管理 | 加载+注入 |
| D9 | m2_marketing/catalog_generator.py — Catalog生成 | Catalog PDF |
| D10 | m3_seo/alibaba_generator.py — 阿里内容 | SEO标题 + 详情页 |
| D10 | m3_seo/website_generator.py — 独立站内容 | Meta + Description |
| D11 | m3_seo/social_generator.py — 社交媒体 | FB/LinkedIn/WhatsApp |
| D12 | templates/ — 文档模板 (docx/pdf) | 模板文件 |
| D12-13 | 集成测试: 选1个产品 → 生成全套内容 | 完整输出包 |
| D14 | 测试 + 文档 | |

**MVP Milestone 2**: 选中一个产品，一键生成SEO标题、详情页、社交媒体文案、产品目录PDF。

### Week 3: 报价辅助 + CRM基础

| 天 | 任务 | 交付物 |
|----|------|--------|
| D15 | m8_crm/client_manager.py — 客户管理 | 客户CRUD |
| D15 | m8_crm/activity_tracker.py — 联系记录 | 活动记录 |
| D16 | m7_quotation/calculator.py — 价格计算 | 装柜/价格计算 |
| D16 | m7_quotation/email_generator.py — 报价邮件 | 报价邮件模板 |
| D17 | m7_quotation/document_generator.py — 报价单 | 报价单PDF/Excel |
| D17 | m6_outreach/template_manager.py — 模板管理 | 开发信模板库 |
| D18 | m6_outreach/email_generator.py — 邮件生成 | 开发信生成 |
| D18 | m6_outreach/whatsapp_generator.py — WhatsApp | WhatsApp消息 |
| D19 | 集成测试: 客户 → 报价 → 开发信全流程 | 端到端验证 |
| D20-21 | MVP总结 + 文档 | MVP发布 |

**MVP Milestone 3**: 完整业务流跑通：产品 → 内容生成 → 客户 → 报价 → 开发信。

### MVP核心交付物清单

| # | 交付物 | 状态 |
|---|--------|------|
| 1 | SQLite数据库 (13张表) | Week 1 |
| 2 | v1.0数据迁移 (215产品入库) | Week 1 |
| 3 | 产品搜索/筛选/导入/导出 | Week 1 |
| 4 | 结构化Prompt库 | Week 2 |
| 5 | Catalog PDF生成 | Week 2 |
| 6 | SEO标题 + 详情页生成 | Week 2 |
| 7 | 社交媒体文案生成 | Week 2 |
| 8 | 客户CRUD管理 | Week 3 |
| 9 | 报价计算 + 报价单生成 | Week 3 |
| 10 | 开发信生成 (Email + WhatsApp) | Week 3 |

---

## 十一、第二阶段规划 (Phase 2: Week 4-6)

### 目标：Agent化 + 市场研究 + 客户分析

### Week 4: 市场研究Agent (M4)

| 天 | 任务 | 交付物 |
|----|------|--------|
| D22 | m4_market_research/web_scraper.py | 网页数据采集 |
| D23 | m4_market_research/report_generator.py | 报告生成 |
| D24 | m4_market_research/knowledge_extractor.py | 知识入库 |
| D25 | agents/market_research_agent.py | Agent编排 |
| D26-27 | 测试: Liberia + Shovel → 完整报告 | 市场报告 |

### Week 5: 客户分析Agent (M5) + Streamlit UI

| 天 | 任务 | 交付物 |
|----|------|--------|
| D28 | m5_client_analysis/company_scraper.py | 公司信息搜集 |
| D29 | m5_client_analysis/grader.py | 客户评级 |
| D30 | m5_client_analysis/advisor.py | 策略建议 |
| D30 | agents/client_analysis_agent.py | Agent编排 |
| D31-32 | ui/streamlit_app.py — 基础UI | Streamlit应用 |
| D33-34 | Streamlit对接所有MVP模块 | 完整UI |

### Week 6: 开发信进阶 + 集成测试

| 天 | 任务 | 交付物 |
|----|------|--------|
| D35 | m6_outreach/linkedin_generator.py | LinkedIn消息 |
| D35 | 多场景开发信模板完善 | 4+场景模板 |
| D36 | agents/outreach_agent.py | 开发信Agent |
| D37 | agents/quotation_agent.py | 报价Agent |
| D38-39 | 端到端集成测试 | 全流程验证 |
| D40-42 | Phase 2总结 + 文档 | Phase 2发布 |

### Phase 2核心交付物

| # | 交付物 | 说明 |
|---|--------|------|
| 1 | 市场研究Agent | 输入国家+产品 → 自动生成报告 |
| 2 | 客户分析Agent | 输入公司信息 → 自动评级+建议 |
| 3 | 开发信Agent | 多场景/多渠道自动生成 |
| 4 | 报价Agent | 完整报价流程自动化 |
| 5 | Streamlit UI | 可视化操作界面 |

---

## 十二、第三阶段规划 (Phase 3: Week 7-10)

### 目标：数据运营 + 智能工作流 + 外部集成

### Week 7-8: 数据运营分析中心 (M9)

| 任务 | 交付物 |
|------|--------|
| m9_analytics/product_analytics.py | 产品维度分析 |
| m9_analytics/client_analytics.py | 客户维度分析 |
| m9_analytics/market_analytics.py | 市场维度分析 |
| m9_analytics/dashboard_data.py | 仪表盘数据 |
| ui/streamlit_app.py — 仪表盘页 | 交互式可视化 |
| 输出: 周报/月报自动生成 | PDF报告 |

### Week 9: Dify/n8n集成

| 任务 | 交付物 |
|------|--------|
| Dify工作流配置 | 可视化Agent流程 |
| n8n工作流配置 | 自动化触发 |
| 定时任务 (APScheduler) | 定时市场研究/报告 |
| 知识库自动更新 | 数据自我进化 |

### Week 10: 智能推荐 + 完善

| 任务 | 交付物 |
|------|--------|
| 产品推荐引擎 | 根据客户特征推荐产品 |
| 市场机会推荐 | 推荐优先开拓的国家 |
| 价格优化建议 | 基于历史数据的价格建议 |
| 完整文档 | 用户指南 + API文档 |
| 性能优化 | 缓存、批量处理优化 |

### Phase 3核心交付物

| # | 交付物 | 说明 |
|---|--------|------|
| 1 | 数据仪表盘 | 产品/客户/市场三维分析 |
| 2 | 自动周报/月报 | 定期生成业务报告 |
| 3 | Dify/n8n工作流 | 可视化Agent编排 |
| 4 | 智能推荐引擎 | 产品/市场/价格推荐 |
| 5 | 完整文档体系 | 用户指南、API文档、部署文档 |

---

## 十三、MVP vs Phase 2 vs Phase 3 对比

| 维度 | MVP (Phase 1) | Phase 2 | Phase 3 |
|------|---------------|---------|---------|
| 核心能力 | 数据管理 + 内容生成 | Agent化 + 市场/客户分析 | 数据运营 + 智能工作流 |
| 产品数据库 | SQLite + 搜索/导入导出 | + AI补全 | + 推荐引擎 |
| 内容生成 | SEO + Catalog + 社交媒体 | + 市场定制版 | + 自动更新 |
| 客户管理 | 基础CRM (CRUD) | + AI分析 + 评级 | + 智能推荐 |
| 市场研究 | ❌ | ✅ 自动生成报告 | ✅ + 定时更新 |
| 开发信 | 基础模板 + AI生成 | + 多场景/多渠道 | + 效果追踪 |
| 报价 | 基础计算 + 模板 | + Agent化 | + 价格优化建议 |
| 数据分析 | ❌ | 基础统计 | ✅ 完整仪表盘 |
| 用户界面 | CLI | CLI + Streamlit基础 | Streamlit完整仪表盘 |
| 自动化 | 手动触发 | 部分自动化 | 完整pipeline + 定时 |
| 外部集成 | LLM API | + Web搜索 | + Dify/n8n |
| 适用场景 | 个人日常使用 | 个人 + 辅助决策 | 个人 → 团队可扩展 |

---

## 十四、关键技术决策

### 14.1 为什么选SQLite而不是MySQL/PostgreSQL？

| 因素 | SQLite | MySQL/PostgreSQL |
|------|--------|------------------|
| 部署 | 零配置，单文件 | 需要安装和配置服务 |
| 维护 | 无运维成本 | 需要备份、监控 |
| 性能 | 10万行以下足够 | 大数据量更优 |
| 并发 | 单写多读 | 高并发支持 |
| 迁移 | 随时可升级 | 一开始就重 |

**决策**: MVP用SQLite。如果未来数据量超过10万行或需要多人并发，迁移到PostgreSQL（SQL语法兼容，迁移成本低）。

### 14.2 为什么选Streamlit而不是React/Vue？

| 因素 | Streamlit | React/Vue |
|------|-----------|-----------|
| 开发速度 | 1天可出原型 | 1周起步 |
| Python生态 | 直接复用Pandas等 | 需要API层 |
| 数据可视化 | 内置Plotly支持 | 需要额外库 |
| 维护成本 | 纯Python，1人可维护 | 需要前后端分离 |

**决策**: Streamlit适合个人数据工具。如果未来需要多用户、权限管理、移动端，再考虑前后端分离。

### 14.3 为什么先做Python CLI再接Dify/n8n？

1. **CLI是验证业务逻辑最快的方式** — 不需要搭UI，直接写Python
2. **Dify/n8n需要API** — 先把逻辑封装成函数，后续轻松暴露为API
3. **成本控制** — Dify/n8n有学习和配置成本，MVP阶段不需要
4. **渐进式** — CLI → API → Streamlit → Dify/n8n，每步都有产出

### 14.4 LLM Provider策略

```yaml
llm:
  providers:
    primary: qwen           # 日常内容生成（成本低、中文好）
    research: openai        # 市场研究（英文搜索和理解强）
    analysis: claude        # 客户分析（长文本处理能力强）
    fallback: gemini        # 备用（免费额度）
  
  # 按场景自动路由
  routing:
    seo_content: qwen
    market_research: openai
    client_analysis: claude
    outreach: qwen
    quotation: qwen
```

---

## 十五、数据流转全景

### 15.1 核心业务流程

```
[新SKU] ──→ CSV/Excel导入 ──→ 数据清洗 ──→ SQLite产品库
                                                    │
                                    ┌───────────────┼───────────────┐
                                    ↓               ↓               ↓
                              [SEO内容生成]    [Catalog生成]    [社交媒体文案]
                                    │               │               │
                                    ↓               ↓               ↓
                              阿里国际站上架    客户邮件附件     FB/LinkedIn发布
                                    │
                                    ↓
                              [市场研究Agent] ← 输入: 国家+产品
                                    │
                                    ↓
                              市场报告 ──→ 指导市场策略
                                    │
                                    ↓
                              [客户开发] ← 输入: 目标国家+产品
                                    │
                                    ↓
                              开发信/WhatsApp ──→ 发送客户
                                    │
                                    ↓
                              [CRM记录] ← 自动记录联系历史
                                    │
                                    ↓
                              [报价Agent] ← 客户询价
                                    │
                                    ↓
                              报价单 ──→ 发送客户
                                    │
                                    ↓
                              [成交记录] ──→ 订单管理
                                    │
                                    ↓
                              [数据运营中心] ← 聚合所有数据
                                    │
                                    ↓
                              业务仪表盘 + 决策建议
```

### 15.2 数据关系链

```
Product ──1:N──→ Content (SEO/Detail/Social)
Product ──1:N──→ Inquiry (询盘)
Product ──1:N──→ Quotation (报价)

Client ──1:N──→ Activity (联系记录)
Client ──1:N──→ Inquiry
Client ──1:N──→ Quotation
Client ──1:N──→ Order (订单)
Client ──M:N──→ Tag (标签)

Country ──1:N──→ Market Report (市场报告)
Country ──1:N──→ Market Knowledge (市场知识)
Country ──1:N──→ Client (客户)
```

---

## 十六、API设计 (内部函数接口)

### 16.1 产品模块 API

```python
# 导入
product_import_csv(filepath: str) -> dict      # {imported: N, errors: [...]}
product_import_excel(filepath: str) -> dict

# CRUD
product_get(code: str) -> Product
product_list(filters: dict) -> list[Product]
product_create(product: Product) -> Product
product_update(code: str, updates: dict) -> Product
product_delete(code: str) -> bool

# 搜索
product_search(query: str, filters: dict) -> list[Product]

# AI
product_ai_complete(code: str, fields: list) -> dict  # AI补全缺失字段

# 导出
product_export_csv(filepath: str, filters: dict) -> str
product_export_excel(filepath: str, filters: dict) -> str
```

### 16.2 内容生成 API

```python
# SEO
generate_seo_titles(product_code: str, count: int = 3) -> list[str]
generate_detail_page(product_code: str, platform: str) -> str
generate_meta_tags(product_code: str) -> dict

# 社交媒体
generate_facebook_post(product_code: str, market: str) -> str
generate_linkedin_post(product_code: str, market: str) -> str
generate_whatsapp_message(product_code: str, market: str) -> str

# 营销资料
generate_catalog(product_codes: list[str], market: str, format: str) -> file_path
generate_product_sheet(product_code: str, format: str) -> file_path
```

### 16.3 市场研究 API

```python
generate_market_report(country: str, product: str, depth: str = "basic") -> dict
# Returns: {report_md: str, report_pdf: path, knowledge: list}

get_market_knowledge(country: str, category: str) -> list[dict]
```

### 16.4 客户分析 API

```python
analyze_client(company_name: str, website: str = None) -> dict
# Returns: {profile, grade, score, recommendations, matched_products}

grade_client(client_id: int, criteria: dict) -> dict
# Returns: {grade: "B+", score: 72, dimensions: {...}}
```

### 16.5 开发信 API

```python
generate_outreach(client_id: int, scenario: str, channel: str, style: str) -> dict
# Returns: {subject, body, body_html, follow_up_date}

get_outreach_templates(scenario: str, channel: str) -> list[dict]
save_outreach_template(template: dict) -> int
```

### 16.6 报价 API

```python
calculate_quotation(product_code: str, quantity: int, incoterm: str) -> dict
# Returns: {unit_price, total, loading_qty_20ft, loading_qty_40ft, ...}

generate_quotation(client_id: int, product_code: str, quantity: int, **kwargs) -> dict
# Returns: {quotation_no, file_path, email_body, record_id}
```

### 16.7 CRM API

```python
client_create(client: dict) -> int
client_get(client_id: int) -> dict
client_list(filters: dict) -> list[dict]
client_search(query: str, filters: dict) -> list[dict]
client_update(client_id: int, updates: dict) -> bool
client_add_tag(client_id: int, tag_name: str) -> bool

activity_log(client_id: int, activity: dict) -> int
activity_list(client_id: int, filters: dict) -> list[dict]

set_follow_up(client_id: int, date: str, notes: str) -> int
get_due_follow_ups(date: str = None) -> list[dict]
```

### 16.8 数据分析 API

```python
product_stats() -> dict
# Returns: {top_inquiry_products, top_conversion_products, category_distribution}

client_stats() -> dict
# Returns: {country_distribution, grade_distribution, conversion_rates}

market_opportunity() -> dict
# Returns: {country_scores, product_demand_trends, recommendations}
```

---

## 十七、配置示例

### 17.1 settings.yaml

```yaml
# config/settings.yaml

app:
  name: "FT Workspace"
  version: "2.0.0"
  language: "en"

database:
  path: "data/ft_workspace.db"
  backup_dir: "data/backups"
  backup_frequency: "daily"

llm:
  providers:
    qwen:
      api_key: "${QWEN_API_KEY}"
      model: "qwen3.6-plus"
      base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    openai:
      api_key: "${OPENAI_API_KEY}"
      model: "gpt-4o"
    claude:
      api_key: "${ANTHROPIC_API_KEY}"
      model: "claude-sonnet-4-20250514"
  default_provider: "qwen"
  routing:
    seo_content: "qwen"
    market_research: "openai"
    client_analysis: "claude"
    outreach: "qwen"
    quotation: "qwen"

search:
  serper_api_key: "${SERPER_API_KEY}"

paths:
  imports: "data/imports"
  output: "output"
  assets: "assets"
  templates: "templates"
  prompts: "prompts"

defaults:
  currency: "USD"
  incoterm: "FOB"
  port: "Tianjin"
  language: "en"
```

### 17.2 .env

```bash
# config/.env (不要提交到Git)
QWEN_API_KEY=sk-xxx
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
SERPER_API_KEY=xxx
```

---

## 十八、requirements.txt

```
# Core
pandas>=2.0
openpyxl>=3.1
jinja2>=3.1
pydantic>=2.0
pyyaml>=6.0
python-dotenv>=1.0

# LLM
openai>=1.0
anthropic>=0.18
google-generativeai>=0.3

# Document Generation
python-docx>=0.8
fpdf2>=2.7
python-pptx>=0.6
weasyprint>=60

# Web Scraping
requests>=2.31
beautifulsoup4>=4.12
lxml>=4.9

# UI
streamlit>=1.30
plotly>=5.18
altair>=5.2

# Scheduler
apscheduler>=3.10

# Testing
pytest>=7.4
pytest-cov>=4.1
```

---

## 十九、风险与挑战

### 19.1 技术风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| LLM输出不稳定 | 内容质量波动 | Prompt优化 + 质量检查 + 人工审核流程 |
| Web搜索数据质量 | 市场报告准确性 | 多数据源交叉验证 + 置信度标记 |
| SQLite并发限制 | 多人使用时冲突 | MVP单用户，后续迁移PostgreSQL |
| 文档生成格式 | PDF/PPTX排版问题 | 模板预定义 + 占位符替换 |

### 19.2 业务风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 市场数据过时 | 决策偏差 | 定期更新机制 + 手动校正入口 |
| 客户评级不准 | 资源错配 | AI评级 + 人工调整 + 持续优化评分模型 |
| 开发信回复率低 | 效果不佳 | A/B测试标题 + 追踪回复率 + 优化模板 |

### 19.3 个人时间风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 每天2小时学习+开发 | 进度慢 | MVP优先砍功能，每阶段有明确产出 |
| 功能太多做不完 | 项目烂尾 | 严格按MVP→Phase2→Phase3节奏 |
| 维护成本高 | 放弃使用 | 自动化 > 手动，减少日常维护负担 |

---

## 二十、成功标准

### MVP成功标准（Phase 1结束）

- [ ] 215个产品完整迁移到SQLite
- [ ] 产品搜索/筛选/导入/导出可用
- [ ] 选1个产品，能生成：SEO标题(3) + 详情页 + FB文案 + WhatsApp消息 + Catalog PDF
- [ ] 客户CRUD可用，能记录联系历史
- [ ] 报价计算准确，能生成报价邮件 + 报价单
- [ ] 开发信生成可用（至少2个场景）
- [ ] 全流程端到端测试通过

### Phase 2成功标准

- [ ] 市场研究Agent：输入国家+产品，10分钟内生成完整报告
- [ ] 客户分析Agent：输入公司信息，自动评级+建议
- [ ] Streamlit UI：能完成主要操作
- [ ] 开发信Agent：支持4+场景、3+渠道
- [ ] 所有Agent端到端测试通过

### Phase 3成功标准

- [ ] 数据仪表盘：产品/客户/市场三维分析
- [ ] 自动周报/月报
- [ ] Dify/n8n工作流可用
- [ ] 智能推荐：产品推荐 + 市场推荐
- [ ] 完整文档体系

---

## 二十一、从v1.0到v2.0的核心变化

| 维度 | v1.0 | v2.0 |
|------|------|------|
| **定位** | AI文案生成工具 | AI外贸智能工作台 |
| **数据** | CSV文件 | SQLite数据库 |
| **架构** | 脚本堆叠 | 模块化 + Agent化 |
| **产品** | 215 SKU，手动管理 | 数据库管理，AI补全 |
| **内容** | SEO + 详情页 + WhatsApp | + Catalog + 社交媒体 + 市场定制 |
| **客户** | 无系统管理 | CRM + AI分析 + 评级 |
| **市场** | 4个大区粗略版本 | 按国家自动生成完整报告 |
| **报价** | 无 | 自动计算 + 报价单生成 |
| **开发** | 手动写开发信 | AI生成多场景开发信 |
| **分析** | 无 | 产品/客户/市场三维分析 |
| **界面** | 无 | CLI + Streamlit仪表盘 |
| **自动化** | 手动触发Hermes | Agent工作流 + 定时任务 |
| **扩展** | 紧耦合 | 插件化，可接Dify/n8n |

---

## 二十二、附录

### A. 术语表

| 术语 | 英文 | 说明 |
|------|------|------|
| SKU | Stock Keeping Unit | 单品，每个产品编码对应一个SKU |
| CRM | Customer Relationship Management | 客户关系管理 |
| RFQ | Request for Quotation | 询价请求 |
| MOQ | Minimum Order Quantity | 最小起订量 |
| FOB | Free on Board | 离岸价（贸易术语） |
| CIF | Cost, Insurance and Freight | 到岸价（贸易术语） |
| HS Code | Harmonized System Code | 海关编码 |
| 装柜量 | Loading Quantity | 一个集装箱能装多少件产品 |
| 开发信 | Outreach Email | 首次联系潜在客户的邮件 |

### B. 农具品类对照表

| 英文 | 中文 | 编码前缀 |
|------|------|----------|
| Garden Fork | 园林叉 | GF |
| Garden Spade | 园林铲 | GS |
| Garden Rake | 花园耙 | GR |
| Garden Hoe | 园林锄 | GH |
| Hoe Tool | 手锄 | HT |
| Shovel | 铲子 | SH |
| Pickaxe | 镐 | PA |
| Axe | 斧头 | AX |
| Pruning Shears | 修枝剪 | PR |
| Machete | 砍刀 | MC |
| Sickles | 镰刀 | SK |
| Lawn Rake | 草坪耙 | LR |
| Hand Rake | 手耙 | HR |
| Trowel | 小铲 | TW |
| Weeder | 除草器 | WD |
| Garden Knife | 园林刀 | GK |
| Bolo Knife | 弯刀 | BK |
| Cleaver | 菜刀 | CC |

### C. 参考资源

- Python-pptx文档: https://python-pptx.readthedocs.io/
- python-docx文档: https://python-docx.readthedocs.io/
- FPDF2文档: https://py-pdf.github.io/fpdf2/
- Streamlit文档: https://docs.streamlit.io/
- SQLite文档: https://www.sqlite.org/docs.html
- Dify: https://dify.ai/
- n8n: https://n8n.io/

---

*本文档是项目的核心蓝图，会随着开发进展持续更新。*
*最后更新: 2026-06-05 | 版本: v2.0 | 状态: 规划阶段*
