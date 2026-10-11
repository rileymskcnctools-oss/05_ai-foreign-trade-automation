# FT Workspace — Foreign Trade AI Workspace

外贸 AI 工作台：手工农具外贸业务全流程自动化。

## 版本

| 版本 | 技术栈 | 状态 | 入口 |
|------|--------|------|------|
| V0.1 | CSV + Python 脚本 | 归档 | — |
| V2.0 | SQLite + Streamlit | 归档（可用） | `streamlit run v2_streamlit/app.py` |
| V3.0 | SQLite + FastAPI + HTMX | 归档（保留） | `python -m uvicorn web.main:app` |
| **V4.0** | **SQLite + FastAPI + Vue 3** | **当前活跃** | `python run_web.py` |

详细演进路径见 [UPGRADE_PATH.md](UPGRADE_PATH.md)。

## 快速开始

```bash
# 1. 后端依赖（依据 pyproject.toml，自动创建 .venv；Python 3.12）
uv sync --extra dev

# 2. 初始化数据库（建表 + 导入 215 条产品 + 演示数据）
python scripts/seed_db.py --reset

# 3. 前端依赖并构建
cd frontend
npm install
npm run build
cd ..

# 4. 启动（V4.0）
python run_web.py
```

启动后：

- 应用入口：http://localhost:8020
- API 文档：http://localhost:8020/docs

> `run_web.py` 会在检测到 `frontend/dist` 缺失时自动执行一次前端构建；
> 端口 8020 被占用时自动清理或顺延。

### 环境变量

```bash
cp config/.env.example config/.env   # 填入 LLM / 搜索服务的 API Key
```

API Key 一律放 `config/.env`（已被 .gitignore 排除），不要写进 `config/settings.yaml`。

### 前端开发模式

```bash
cd frontend && npm run dev       # Vite 开发服务器，默认 http://localhost:5173
```

后端已为 `localhost:5173` 配置 CORS 白名单。

## 功能模块

| 模块 | 前端视图 | API 前缀 | 说明 |
|------|----------|----------|------|
| 数据概览 | `DashboardView.vue` | `/api/dashboard` | KPI 卡片 + 图表 + 快速搜索 |
| 产品管理 | `ProductsView.vue` | `/products/api` | 215 产品 + 分类筛选 + CSV 导出 |
| 客户 CRM | `ClientsView.vue` | `/clients/api` | 客户档案 + 状态管理 + 跟进记录 + 真实客户搜索 |
| 市场研究 | `MarketView.vue` | `/market/api` | 市场报告 + 知识库 + 国家对比 + PDF 导出 |
| 开发信 | `OutreachView.vue` | `/outreach/api` | 邮件 / WhatsApp / LinkedIn 三渠道 |
| 报价助手 | `QuotationView.vue` | `/quotation/api` | 多产品报价单 + 成本利润 + 版本修订 |
| 数据分析 | `AnalyticsView.vue` | `/analytics/api` | 产品 / 客户 / 市场 / 漏斗四维度 |

V4.0 共 47 个 API 路径，完整清单见运行时 `/docs`。

## 项目结构

```
├── src/              业务逻辑层（各版本共用）
│   ├── core/         数据库 + 配置 + LLM 客户端
│   ├── m1~m9/        9 个功能模块
│   └── utils/        提示词模板引擎
├── web/              V4 API 服务
│   ├── main_api.py   V4 入口（纯 API，供 Vue 调用）
│   ├── main.py       V3 入口（HTMX 版，保留）
│   └── routes/       7 个路由模块
├── frontend/         Vue 3 前端（Vite + Pinia + Tailwind + Chart.js）
│   └── src/views/    7 个页面视图
├── tests/            自动化测试（api / ui / unit / data）
├── prompts/          AI 提示词模板
├── config/           配置（settings.yaml + .env）
├── data/             SQLite 数据库 + schema.sql + seed/ 种子数据
├── scripts/          工具脚本（见下）
├── docs/             文档
├── reports_deai/     市场报告与 PDF 转换
├── v2_streamlit/     V2 归档
└── run_web.py        V4 一键启动
```

## 数据库与数据复现

数据库文件 `data/*.db` **不进版本控制**（已在 .gitignore 中排除），
复现完全依赖 `data/schema.sql` + `data/seed/` 中的种子数据。

```bash
python scripts/seed_db.py                  # 幂等：已有数据的表不重复灌
python scripts/seed_db.py --reset          # 重建表结构并重新灌数据
python scripts/seed_db.py --db <path>      # 指定数据库文件（测试用临时库）
python scripts/seed_db.py --products-only  # 只灌产品
```

种子数据：

| 数据 | 位置 | 条数 |
|------|------|------|
| 产品主数据 | `data/seed/products.csv` | 215 |
| 客户 | `scripts/seed_db.py` 内置 | 8 |
| 市场报告 / 知识库 | 同上 | 3 / 4 |
| 活动 / 报价 / 价格记录 | 同上 | 16 / 5 / 5 |

> `schema.sql` 是表结构的**唯一真相源**。新增字段请直接改 `schema.sql`，
> 不要再外挂独立的 ALTER 补丁脚本——否则新环境建出的库会缺列，
> 接口报 `no such column`。

## 主要脚本

| 脚本 | 用途 |
|------|------|
| `scripts/seed_db.py` | 数据库初始化 / 种子数据（推荐入口） |
| `scripts/ft_cli.py` | 命令行工具 |
| `scripts/verify_setup.py` | 环境自检 |
| `scripts/inject_test_data.py` | 早期业务演示数据脚本（功能已并入 seed_db.py） |
| `scripts/migrate_length_to_color.py` | 历史迁移（products: length_cm → color） |

## 测试

```bash
.venv\Scripts\python -m pytest              # 全部
.venv\Scripts\python -m pytest -m smoke     # 只跑冒烟
```

测试目录分工见 `tests/__init__.py`；共享 fixture 写在 `tests/conftest.py`。

## 技术栈

- **后端**：Python 3.12 + FastAPI + SQLite（WAL）
- **前端**：Vue 3 + Vite + Pinia + Vue Router + Tailwind CSS + Chart.js
- **AI**：DeepSeek / OpenAI / Anthropic / Gemini（按场景路由）
- **采集**：requests + BeautifulSoup + Playwright
- **测试**：pytest + httpx（TestClient）
- **部署**：uvicorn（localhost:8020）

## 文档

- [项目说明与测试指南](docs/项目说明与测试指南.md) — **架构 / 数据模型 / 47 个 API / 测试指引（写测试先看这份）**
- [测试用例模板](docs/测试用例模板.csv) — 用例表头与示例行
- [系统使用指南](docs/USER_GUIDE.md) — 产品 / 客户 / 提示词管理
- [版本演进路径](UPGRADE_PATH.md) — V0.1 → V4.0 升级对照
- [API 文档](http://localhost:8020/docs) — 运行后自动可用
