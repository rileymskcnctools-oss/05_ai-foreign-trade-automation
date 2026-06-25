# FT Workspace v3.0 系统使用完整指南

## 一、系统架构总览

```
项目根目录: 05_ai-foreign-trade-automation/
│
├── data/
│   ├── ft_workspace.db          ← 核心数据库(SQLite)
│   ├── schema.sql               ← 数据库表结构定义
│   └── backups/                 ← 自动备份目录
│
├── config/
│   └── settings.yaml            ← 全局配置(LLM/数据库/路径)
│
├── prompts/                     ← AI提示词模板(19个.md文件)
│   ├── outreach/                ← 开发信提示词
│   ├── seo/                     ← SEO内容提示词
│   ├── market_research/         ← 市场报告提示词
│   ├── quotation/               ← 报价邮件提示词
│   ├── client_analysis/         ← 客户分析提示词
│   ├── social/                  ← 社交媒体提示词
│   └── system/                  ← 系统级提示词
│
├── src/                         ← 业务逻辑层(V2/V3共用)
│   ├── core/                    ← database.py + config.py + llm_client.py
│   ├── m1_product_db/           ← 产品数据清洗
│   ├── m2_marketing/            ← 产品目录生成
│   ├── m3_seo/                  ← SEO内容生成
│   ├── m4_market_research/      ← 市场研究
│   ├── m5_client_analysis/      ← 客户分析
│   ├── m6_outreach/             ← 开发信生成
│   ├── m7_quotation/            ← 报价计算
│   ├── m8_crm/                  ← 客户管理
│   ├── m9_analytics/            ← 数据分析
│   └── utils/                   ← prompts.py 模板引擎
│
├── web/                         ← V3 Web界面(FastAPI+HTMX+Tailwind)
│   ├── routes/                  ← 7个路由模块
│   ├── templates/               ← 8个Jinja2页面 + 组件
│   └── static/                  ← CSS/JS静态资源
│
├── v2_streamlit/                ← V2旧版(Streamlit) → 已归档
│   └── app.py                   ← 启动: streamlit run v2_streamlit/app.py
│
├── archive/v0.1/                ← V0.1学习阶段代码 → 已归档
│
├── scripts/                     ← 工具脚本
│   ├── ft_cli.py                ← CLI命令行工具
│   ├── migrate_v1_to_v2.py      ← V1→V2数据迁移
│   ├── inject_test_data.py      ← 测试数据注入
│   └── verify_setup.py          ← 环境检查
│
├── output/                      ← AI生成的输出文件
├── assets/                      ← 静态资源(图片/字体/图标)
│
└── run_web.py                   ← V3一键启动入口
```


## 二、产品数据管理

### 入口1: CSV批量导入（初次大批量录入）

- 文件位置: `archive/v0.1/04-database/csv/product_database_filled.csv`
- 编码格式: **GBK**（不是UTF-8!）
- 当前数据: 215个产品
- 31列字段，核心列:

| 列名 | 说明 |
|------|------|
| product_id | 产品编码，如 GF-001 |
| product_name_cn | 中文名: 园林耙 |
| product_name_en | 英文名: Garden Fork |
| category | 分类: Digging/Cutting/Weeding |
| material | 材质: Carbon Steel |
| length_cm | 长度(厘米) |
| weight_kg | 重量(千克) |
| moq | 最小起订量 |
| packaging_type | 包装方式 |
| qty_per_carton | 每箱装量 |
| carton_size_cm | 箱规: 43x43x18 |
| target_keywords | SEO关键词 |
| selling_points | 卖点文案 |

修改方式: 用Excel打开CSV → 编辑 → 保存为CSV(GBK) → 重新导入

### 入口2: 网页界面（日常使用）

- 访问: `http://localhost:8001/products`
- 搜索框: 输入编码或名称快速查找
- 分类筛选: Digging Tools / Cutting Tools / Weeding Tools
- 详情按钮: 查看单个产品完整信息
- 导出CSV: 把当前产品列表导出

### 入口3: 数据库直接操作（批量更新）

- 数据库文件: `data/ft_workspace.db`
- 工具: DB Browser for SQLite (免费软件)
- 表名: `products`

```sql
-- 示例: 给所有Garden Fork加MOQ
UPDATE products SET moq=1000 WHERE category='Digging Tools';

-- 示例: 查看所有缺SEO标题的产品
SELECT product_code, product_name_en FROM products WHERE seo_title_1 IS NULL;
```


## 三、客户信息管理

### 入口1: 网页界面（推荐日常使用）

- 访问: `http://localhost:8001/clients`
- 功能:
  - **+ 新建客户** 按钮: 弹窗填写公司名/国家/邮箱等
  - 状态筛选: lead / prospect / negotiating / won / lost
  - 评级筛选: A / B / C / D
  - 导出CSV: 一键导出全部客户

### 入口2: 数据库直接操作

- 表名: `clients`

| 字段 | 说明 |
|------|------|
| company_name | 公司名(必填) |
| country | 国家 |
| contact_person | 联系人 |
| email / whatsapp | 联系方式 |
| status | lead→contacted→negotiating→won |
| grade | A(大客户) B(中) C(小) D(待开发) |
| source | alibaba/exhibition/referral等 |

```sql
-- 示例: 新增一个客户
INSERT INTO clients (company_name, country, email, status, grade)
VALUES ('ABC Trading', 'Nigeria', 'info@abc.com', 'lead', 'B');
```


## 四、提示词(Prompts)管理

位置: `prompts/` 目录下，共19个 `.md` 文件

```
prompts/
├── outreach/                    ← 开发信(最常用!)
│   ├── initial_email.md         ← 初次开发信
│   ├── follow_up_email.md       ← 跟进邮件
│   ├── whatsapp_outreach.md     ← WhatsApp话术
│   ├── linkedin_outreach.md     ← LinkedIn消息
│   └── rfq_reply.md            ← 询价回复
├── seo/                         ← SEO内容
│   ├── alibaba_title.md         ← 阿里巴巴标题
│   ├── alibaba_detail.md        ← 阿里巴巴详情
│   ├── selling_points.md        ← 卖点提炼
│   └── website_description.md   ← 官网描述
├── market_research/             ← 市场报告
├── quotation/                   ← 报价邮件
├── client_analysis/             ← 客户画像分析
├── social/                      ← 社交媒体内容
└── system/                      ← 系统知识注入
```

修改方式: 用任何文本编辑器(记事本/VS Code)直接编辑 `.md` 文件

占位符语法（系统会自动替换）:

```
{{client_company}}  → 客户公司名
{{client_country}}  → 客户国家
{{product_names}}   → 产品名称
{{selling_points}}  → 卖点
${product_name_en}  → 产品英文名(v1格式也兼容)
```


## 五、全局配置

文件: `config/settings.yaml`

| 配置项 | 说明 |
|--------|------|
| llm.default_provider | 默认AI模型(deepseek等) |
| defaults.currency | 默认货币(USD) |
| defaults.incoterm | 默认贸易术语(FOB) |
| defaults.port | 默认港口(Tianjin) |

API密钥实际存放: `.env` 文件（不在settings.yaml中）


## 六、日常使用流程

```
1. 启动系统:  python run_web.py
2. 打开浏览器: http://localhost:8001
3. 录入新客户: 客户CRM → +新建客户
4. 查看产品:   产品管理 → 搜索/筛选
5. 生成报价:   报价助手 → 选产品 → 填数量 → 计算
6. 写开发信:   开发信 → 选客户 → 选类型 → 生成
7. 查看分析:   数据分析 → 产品/客户/市场维度
```


## 七、数据备份

- 数据库文件: `data/ft_workspace.db`
- 建议: 定期复制这个文件到安全位置
- 代码支持: `db.backup()` 自动备份到 `data/backups/`


## 八、数据库表结构速查

| 表名 | 用途 | 关键字段 |
|------|------|---------|
| products | 产品目录 | product_code, category, material |
| clients | 客户档案 | company_name, country, grade, status |
| activities | 跟进记录 | client_id, activity_type, follow_up_date |
| quotations | 报价单 | quotation_no, client_id, total_amount |
| inquiries | 询盘 | client_id, product_code, status |
| price_records | 价格记录 | product_code, base_price_usd |
| market_reports | 市场报告 | country, report_title, confidence |
| content_records | AI内容 | product_code, content_type, content |
| outreach_templates | 开发信模板 | name, channel, template_body |
