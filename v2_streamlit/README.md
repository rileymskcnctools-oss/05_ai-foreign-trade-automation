# V2.0 Streamlit 版本归档

这是 FT Workspace 的 **V2.0 版本**，使用 Streamlit 构建的 Web 界面。

## 启动方式

```bash
streamlit run v2_streamlit/app.py
```

## V2.0 架构

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Streamlit   │────▶│  FTDatabase  │────▶│   SQLite    │
│  Web 界面    │     │  (Python)    │     │  215产品    │
└──────┬──────┘     └──────┬───────┘     └─────────────┘
       │                   │
       ▼                   ▼
┌─────────────┐     ┌──────────────┐
│  ft_cli.py  │────▶│  LLMClient   │
│  CLI 命令行  │     │  DeepSeek API│
└─────────────┘     └──────────────┘
```

## 8个功能页面

1. 数据概览 (Dashboard)
2. 产品管理 (Products)
3. 市场研究 (Market Research)
4. 客户CRM (Clients)
5. 客户分析 (Client Analysis)
6. 开发信 (Outreach)
7. 报价助手 (Quotation)
8. 数据分析 (Analytics)

## 为什么升级到V3.0

| 对比项 | V2.0 Streamlit | V3.0 FastAPI+HTMX |
|--------|---------------|-------------------|
| 前后端 | 耦合（Streamlit全包） | 分离（API + 模板） |
| 页面刷新 | 每次交互全量重跑 | HTMX局部刷新 |
| 样式定制 | 受限于Streamlit组件 | 完全自由Tailwind CSS |
| API接口 | 无独立API | 32个REST API端点 |
| 性能 | 每次交互重载状态 | 按需请求，响应更快 |
| 部署 | 需要Streamlit服务器 | 标准uvicorn，易容器化 |

## 升级到V3.0

- V3.0 入口: `python run_web.py`（端口8001）
- V3.0 代码: `web/` 目录
- 共享核心: `src/` 目录不变，V2和V3共用同一套业务逻辑
