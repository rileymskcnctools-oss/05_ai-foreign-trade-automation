# FT Workspace 版本演进路径

## 演进时间线

```
V0.1 (学习阶段)          V2.0 (模块化)              V3.0 (当前版本)
2026年5-6月              2026年6月                  2026年6月25日
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CSV + 独立脚本    →     SQLite + 模块化      →    FastAPI + HTMX
无Web界面              Streamlit 8页              32个API + HTMX
手动运行每个脚本         按钮点击操作               局域网多人访问
```


## V0.1 → V2.0 关键升级

### 数据层: CSV → SQLite

```
V0.1: product_database_filled.csv (GBK编码)
  ↓ scripts/migrate_v1_to_v2.py 自动迁移
V2.0: data/ft_workspace.db (SQLite + WAL模式)
```

核心变化:
- CSV平面文件 → SQLite关系数据库
- 手动Excel编辑 → SQL查询 + API操作
- 无数据验证 → 外键约束 + 唯一索引
- 无备份 → 自动热备份 `data/backups/`

### 代码层: 独立脚本 → 模块化

```
V0.1: 03-workflows/python/day01_xxx.py, day02_xxx.py ...
  ↓ 重构为9个业务模块
V2.0: src/m1_product_db/ ... src/m9_analytics/
```

核心变化:
- 按天递进的学习脚本 → 按业务功能划分的模块
- 每个脚本独立运行 → 统一数据库入口 + 模块间可调用
- 硬编码配置 → `config/settings.yaml` + `.env`

### 提示词: txt模板 → md模板 + 引擎

```
V0.1: 02-prompts/seo/seo_title_prompt.txt (简单文本替换)
  ↓ 结构化模板 + 占位符引擎
V2.0: prompts/seo/alibaba_title.md ({{key}} + ${key} 双格式)
      src/utils/prompts.py (load_prompt + fill_prompt + fill_and_send)
```


## V2.0 → V3.0 关键升级

### 界面层: Streamlit → FastAPI + HTMX

```
V2.0: app.py (769行单文件Streamlit)
  ↓ 拆分为路由+模板+组件
V3.0: web/ (7个路由模块 + 8个页面 + HTMX组件)
```

核心变化:

| 对比项 | V2.0 Streamlit | V3.0 FastAPI+HTMX |
|--------|---------------|-------------------|
| 架构 | 单文件769行 | 7模块+8模板+组件 |
| 前后端 | 耦合 | 分离(REST API) |
| 交互 | 全量重跑 | HTMX局部刷新 |
| API | 无 | 32个端点 |
| 样式 | Streamlit默认 | Tailwind CSS |
| 启动 | `streamlit run app.py` | `python run_web.py` |
| 端口 | 8501 | 8001 |

### 新增API端点 (V3.0独有)

```
GET  /api/dashboard/stats      ← KPI数据
GET  /api/dashboard/home       ← 首页仪表盘
GET  /products/api/search?q=   ← 产品搜索
GET  /products/api/categories  ← 分类列表
GET  /products/api/export/csv  ← CSV导出
POST /clients/api/create       ← 新建客户
GET  /clients/api/export/csv   ← 客户导出
POST /quotation/api/calculate  ← 报价计算
POST /outreach/api/generate-email    ← 生成邮件
POST /market/api/generate-report     ← 生成报告
... 共32个
```


## 三个版本的文件对照

```
文件/目录               V0.1    V2.0    V3.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
01-input/              ✓ 归档
02-prompts/            ✓ 归档
03-workflows/          ✓ 归档
04-database/           ✓ 归档(含CSV源数据)
05-output/             ✓ 归档
07-docs/               ✓ 归档
08-git/                ✓ 归档
src/core/database.py           ✓       ✓ 共用
src/m1~m9/                     ✓       ✓ 共用
prompts/                       ✓       ✓ 共用
config/                        ✓       ✓ 共用
data/                          ✓       ✓ 共用
scripts/                       ✓       ✓ 共用
app.py(Streamlit)              ✓ 归档
web/(FastAPI)                          ✓ 活跃
run_web.py                           ✓ 活跃
```


## 迁移指南

### 从V0.1升级到V2.0

```bash
# 1. 确保CSV文件在正确位置
# 2. 运行迁移脚本
python scripts/migrate_v1_to_v2.py

# 3. 验证数据
python scripts/verify_setup.py
```

### 从V2.0升级到V3.0

```bash
# 无需迁移数据! V2和V3共享同一个SQLite数据库
# 直接启动V3.0
python run_web.py

# V2.0 Streamlit仍可使用(备用)
streamlit run v2_streamlit/app.py
```


## 技术栈演进

```
V0.1: Python + CSV + OpenAI API + 脚本
V2.0: Python + SQLite + DeepSeek API + Streamlit + CLI
V3.0: Python + SQLite + DeepSeek API + FastAPI + HTMX + Tailwind CSS
```
