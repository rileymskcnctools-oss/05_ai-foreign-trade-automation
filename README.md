# FT Workspace — Foreign Trade AI Workspace

外贸AI工作台：手工农具外贸业务全流程自动化

## 版本

| 版本 | 技术栈 | 状态 | 入口 |
|------|--------|------|------|
| V0.1 | CSV + Python脚本 | 归档 | `archive/v0.1/` |
| V2.0 | SQLite + Streamlit | 归档(可用) | `streamlit run v2_streamlit/app.py` |
| **V3.0** | **SQLite + FastAPI + HTMX** | **当前活跃** | `python run_web.py` |

详细演进路径: [UPGRADE_PATH.md](UPGRADE_PATH.md)

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动V3.0 Web服务
python run_web.py

# 3. 打开浏览器
# http://localhost:8001
# API文档: http://localhost:8001/docs
```

## 功能模块

| 模块 | 页面 | API端点数 | 说明 |
|------|------|----------|------|
| 数据概览 | /dashboard | 4 | KPI卡片 + 图表 + 快速搜索 |
| 产品管理 | /products | 6 | 215产品 + 分类筛选 + CSV导出 |
| 客户CRM | /clients | 6 | 客户档案 + 状态管理 + 跟进记录 |
| 市场研究 | /market | 3 | AI生成目标市场报告 |
| 开发信 | /outreach | 3 | 邮件/WhatsApp/LinkedIn三渠道 |
| 报价助手 | /quotation | 2 | 价格计算 + 装柜量 + 报价邮件 |
| 数据分析 | /analytics | 4 | 产品/客户/市场/漏斗四维度 |

## 项目结构

```
├── src/              业务逻辑层(V2/V3共用)
│   ├── core/         数据库 + 配置 + AI客户端
│   ├── m1~m9/        9个功能模块
│   └── utils/        提示词模板引擎
├── web/              V3 Web界面
│   ├── routes/       7个路由模块
│   ├── templates/    Jinja2模板 + 组件
│   └── static/       CSS/JS
├── prompts/          AI提示词模板(19个)
├── config/           全局配置
├── data/             SQLite数据库
├── scripts/          工具脚本
├── docs/             文档
├── v2_streamlit/     V2归档
├── archive/v0.1/     V0.1归档
└── run_web.py        V3启动入口
```

## 文档

- [系统使用指南](docs/USER_GUIDE.md) — 产品/客户/提示词管理详解
- [版本演进路径](UPGRADE_PATH.md) — V0.1→V2.0→V3.0 升级对照
- [API文档](http://localhost:8001/docs) — 运行后自动可用

## 技术栈

- **后端**: Python 3.13 + FastAPI + SQLite
- **前端**: HTMX + Tailwind CSS + Jinja2
- **AI**: DeepSeek API (兼容OpenAI SDK)
- **部署**: uvicorn (localhost:8001)
