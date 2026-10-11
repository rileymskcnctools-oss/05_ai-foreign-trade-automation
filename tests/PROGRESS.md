# 测试进度 — FT Workspace

> 最后更新：2026-10-11
> 用途：接续测试工作。下次开始前先读这份；命令在项目根目录执行。

## 一句话状态

**环境和数据全部就绪，测试用例还没开始写。** 可以直接进入写用例阶段。

## 已完成（不用重做）

| 项 | 状态 | 说明 |
|----|------|------|
| 依赖固化 | ✅ | `pyproject.toml` + `uv.lock`，Python 3.12.13；`uv sync --extra dev` 可复现 |
| 数据库复现 | ✅ | `python scripts/seed_db.py --reset` → 215 产品 + 8 客户 + 5 报价 + 3 报告 + 4 知识 + 16 活动 |
| 产品数据恢复 | ✅ | `data/seed/products.csv`（215 条，UTF-8 BOM，源自 git 历史） |
| 测试脚手架 | ✅ | `tests/{api,ui,unit,data}` + `conftest.py`；pytest markers 已注册 |
| 项目文档 | ✅ | `docs/项目说明与测试指南.md`（架构/数据模型/47 API/测试指引） |
| 用例模板 | ✅ | `docs/测试用例模板.csv`（14 列 + 1 行示例，UTF-8 BOM，Excel 可读） |
| 旧版本清理 | ✅ | 只保留 V4；后端目录 `web/` → `api/`，入口 `api/app.py` |
| 环境验证 | ✅ | 47 个端点全在；真实启动 uvicorn，7 个接口 200；数据 215 条 |

## 下一步：逐模块写用例

建议顺序（由易到难、依赖关系顺）

1. **客户 CRM**（数据现成，有 404 分支，适合热身）
   `/clients/api/list`、`/{client_id}`(GET/PUT/DELETE)、`/{id}/activities`、`reminders/summary`、`export/csv`、`batch-insert`
2. **产品管理**（215 条真实数据，主打搜索/筛选/分页）
   `/products/api/search`、`/categories`、`/{code}`、`create`、`export/csv`
3. **报价助手**（逻辑最密；`calculate` 是**纯计算不调 LLM**，可放心断言）
   `/quotation/api/calculate`、`list`、`{no}`、`create`、`stats`、`revision`/`versions`
4. **数据分析**（聚合结果要跟数据库实际值对账）
   `/analytics/api/products`、`/analytics/api/clients`、`/api/dashboard/stats`
5. **市场研究**（部分需 mock）/ **开发信**（全部需 mock LLM）
   `/market/api/*`、`/outreach/api/generate-*`
6. **单元测试**（穿插着做，最快见效）
   `PriceCalculator.calculate_price / calculate_loading / estimate_freight`、`cleaner.clean_product`、`ClientManager.list_all`
7. **UI 冒烟**（最后做，只做 1~2 条主流程，别铺开）
   Playwright：打开 → 查产品 → 建报价 → 看结果

## 明天从这条命令开始

```bash
# 1. 环境（若刚 clone 或换电脑）
uv sync --extra dev
python scripts/seed_db.py --reset

# 2. 起服务（调试用例期望值时用）
python run_web.py                # 或只起后端：python -m uvicorn api.app:app --port 8020

# 3. 写第一条用例（第一题：/clients/api/{client_id}，5 个用例）
#    参考 docs/测试用例模板.csv 的列格式
.venv\Scripts\python -m pytest tests/ -v -m api
```

## 写用例时必须注意的坑

- **不要直接在开发库上跑写操作测试** → 用 `python scripts/seed_db.py --db <临时路径> --reset` 造独立库
- **TestClient 默认 `raise_server_exceptions=True`** → 服务端 500 会以异常抛出而非返回 500；
  要断言状态码请传 `raise_server_exceptions=False`
- **调 LLM 的接口必须先 mock** → 全部收敛在 `LLMClient.chat` / `LLMClient.generate_json`
  （需 mock 的：`/clients/api/{id}/analyze`、`generate-potential`、`search-real-clients`、
   `/market/api/generate-report`、`/outreach/api/generate-*`、`/quotation/api/ai-optimize`、
   `/products/api/{code}/generate/{type}`）
- **POST 请求体在 `/docs` 里看不到字段** → FastAPI 声明为普通 dict，字段名要查 `api/routes/*.py`
- **断言要分三层**：协议层(状态码/Content-Type) + 结构层(字段存在/类型) + 业务层(字段值符合语义)
- **marker 已启用 `--strict-markers`** → 用未注册的 marker 会**收集报错**（可用：smoke/api/ui/unit/slow）

## 已知的真实缺陷（可作为参考用例）

| # | 位置 | 现象 | 状态 |
|---|------|------|------|
| 1 | `/analytics/api/products` | 500 `no such column: color`（schema 漂移） | 已修 |
| 2 | `/quotation/api/stats` | 500 `no such column: profit_amount`（schema 有两个真相源） | 已修 |
| 3 | `src/m7_quotation/calculator.py` | **体积计算恒为 0**（length_m 硬编码 0.5、height_m 硬编码 0）→ CIF 运费估算失真 | **未修** |
| 4 | 依赖 | `google-generativeai` 已停止维护，启动抛 FutureWarning | 未修 |

## 参考资料

- `docs/项目说明与测试指南.md` — **写测试前的第一份读物**（架构/数据模型/47 API/测试分层/检查清单）
- `docs/测试用例模板.csv` — 用例表头与示例行
- `README.md` — 环境搭建、启动、数据复现
- 运行时 `/docs`（http://localhost:8020/docs）— 接口的机器可读定义
- `data/schema.sql` — 表结构的唯一真相源
