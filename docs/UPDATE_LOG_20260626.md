# FT Workspace 更新日志

## 版本演进

| 版本 | 技术栈 | 状态 |
|------|--------|------|
| V0.1 | Python 脚本 + CSV | 已归档 |
| V2.0 | SQLite + Streamlit | 已归档 |
| V3.0 | FastAPI + Jinja2 + HTMX + Tailwind | 已归档 |
| **V4.0** | **FastAPI + Vue 3 + Vite + Tailwind** | **当前版本** |

---

## V4.0 更新内容 (2026-06-26)

### 一、框架升级：从 HTMX 迁移到 Vue 3

**改动范围：** 前端完全重写，后端改造为纯 API 服务

**新增文件：**
```
frontend/                    ← Vue 3 项目
├── src/
│   ├── main.js             ← Vue 入口 (Pinia + Router)
│   ├── App.vue             ← 根组件
│   ├── router/index.js     ← 路由配置
│   ├── api/index.js        ← Axios API 封装 (40+ 接口)
│   ├── components/
│   │   ├── Sidebar.vue     ← 侧边栏导航
│   │   ├── Toast.vue       ← 消息通知
│   │   └── Modal.vue       ← 通用弹窗
│   └── views/
│       ├── DashboardView.vue   ← 数据概览
│       ├── ProductsView.vue    ← 产品管理
│       ├── ClientsView.vue     ← 客户 CRM
│       ├── QuotationView.vue   ← 报价助手
│       ├── MarketView.vue      ← 市场研究
│       ├── OutreachView.vue    ← 开发信
│       └── AnalyticsView.vue   ← 数据分析
├── vite.config.js          ← Vite 配置 + API 代理
├── tailwind.config.js      ← Tailwind 主题
└── package.json

web/main_api.py             ← 纯 API 服务器 (FastAPI + CORS)
```

**技术栈对比：**

| 组件 | V3.0 | V4.0 |
|------|------|------|
| 前端框架 | Jinja2 模板 | Vue 3 Composition API |
| 动态交互 | HTMX | Vue 响应式 + Axios |
| 构建工具 | 无 | Vite |
| 样式 | Tailwind CDN | Tailwind PostCSS 构建 |
| 图表 | Chart.js (直接引入) | Chart.js (npm 包) |
| 路由 | FastAPI 页面路由 | Vue Router (SPA) |
| API | 混合 (HTML + JSON) | 纯 JSON API |

---

### 二、产品管理模块优化

**字段调整：**
- 表格列：`颜色` → `使用场景` (use_scenario)
- 移除：`头宽` (head_width_cm) — 对农具无意义
- 编辑表单：29 个可编辑字段（完整保留）

**AI 生成优化：**
- 生成超时：30s → 120s（LLM 调用需要时间）
- 结果展示：新增全屏查看模式（卖点内容）
- 卖点格式化：
  - `**粗体**` → 加粗标题
  - 纯文本标题 → 自动识别为标题
  - `Feature:` → 蓝色左边框
  - `Benefit:` → 绿色左边框
  - `|` 分隔符 → 分段线

**新增功能：**
- 卖点「全屏查看」按钮
- 复制功能（一键复制卖点内容）

---

### 三、提示词优化

**修改的提示词文件：**

| 文件 | 改动 |
|------|------|
| `prompts/seo/selling_points.md` | 去掉 color，新增 use_scenario/target_markets/competitor_ref/selling_angle |
| `prompts/seo/alibaba_title.md` | 去掉 color，新增 hardness/certification/target_markets/competitor_ref |
| `prompts/seo/alibaba_detail.md` | 去掉 color，新增 loading_qty，清理示例代码 |
| `prompts/social/whatsapp.md` | 去掉 customer_type，新增 use_scenario/target_markets/competitor_ref |
| `prompts/outreach/generate_potential_client.md` | v4.0 优化：强调只推荐真实公司，减少幻觉 |

**核心改动：**
- 移除无意义字段：`color`（大部分产品为空）、`head_width_cm`
- 新增有数据字段：`use_scenario` (215/215)、`target_markets` (215/215)、`competitor_ref` (215/215)
- 清理提示词：去掉「使用示例」和「使用技巧」（不应发送给 LLM）

**build_product_data() 更新：**
- 移除：`color`
- 新增：`head_width_cm`、`certification`

---

### 四、客户 CRM 模块优化

**页面重写：**
- 详情面板：滑出式（从右侧滑入）
  - 联系信息卡片（可点击链接）
  - 业务信息卡片
  - 跟进记录时间线 + 新增记录
  - AI 背调分析 + 运行按钮
- 编辑弹窗：完整字段（13 个）
- AI 客户开发：
  - Tab 1：真实搜索（Google/Bing + AI 分析）
  - Tab 2：AI 虚构（练习用）
  - 一键录入 CRM
- 删除确认：提示级联删除

---

### 五、报价模块重构

**数据库升级：**
```sql
-- quotations 表新增 22 个字段
contact_person, country, loading_port, destination_port,
valid_until, sales_person, discount_pct, shipping_cost,
insurance_cost, packing_cost, other_charges, cost_total,
profit_amount, profit_margin, warranty, oem_odm,
sample_policy, packing_details, remarks, template_type,
revision, parent_quotation_id

-- 新增 quotation_items 表 (19 列)
-- 新增 quotation_versions 表 (6 列)
```

**后端 API（12 个端点）：**

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | /quotation/api/list | 列表（搜索/筛选） |
| GET | /quotation/api/{no} | 详情 + 产品行 |
| POST | /quotation/api/create | 创建（自动生成编号） |
| PUT | /quotation/api/{no} | 更新 |
| DELETE | /quotation/api/{no} | 删除 |
| GET | /quotation/api/{no}/versions | 版本历史 |
| POST | /quotation/api/{no}/revision | 创建修订版 |
| POST | /quotation/api/calculate | 定价计算 |
| POST | /quotation/api/ai-optimize | AI 价格建议 |
| GET | /quotation/api/templates | 模板列表 |
| GET | /quotation/api/stats | 统计 |

**前端（ERP 风格）：**
- 表头：客户、币种、贸易术语、港口、有效期
- 产品行：下拉选择产品，自动填充 SKU/材质
- 费用明细：产品总计、运费、保险、包装费
- 利润分析：成本、售价、利润额、利润率（颜色提示）
- 贸易条款：付款方式、交期、质保、OEM/ODM
- 固定底部：总计 + 利润率 + 保存按钮

---

### 六、数据概览优化

**图表调整：**
- 产品分类：按子类显示（14 个子类 vs 3 个大类）
- 客户国家分布：横向柱状图（真实国家数据）
- Pipeline 阶段：饼图（按状态分布）
- 三个图并排显示（更紧凑）

---

### 七、开发信模块优化

**布局调整：**
- 旧：三列并排（Email/WhatsApp/LinkedIn）
- 新：Tab 切换 + 左右分栏（设置 + 结果）

**新增功能：**
- 编辑：修改生成内容
- 删除：清除结果
- 复制：一键复制到剪贴板
- 历史记录：保存已生成内容
- 格式化：
  - Email：琥珀色主题框
  - WhatsApp：绿色聊天气泡
  - LinkedIn：蓝色渐变卡片

---

### 八、启动方式

```bash
# V4.0 一键启动
cd C:\Users\Administrator\Desktop\code\05_ai-foreign-trade-automation
python run_web.py

# 浏览器打开
http://localhost:8020
```

---

## 已知问题

1. **真实客户搜索**：代理 (SOCKS5) 与 Python requests 兼容性问题，Google/Bing 搜索暂时不可用
2. **AI 生成耗时**：LLM 调用需要 30-60 秒，属正常现象
3. **报价模块**：AI 助手和版本管理功能开发中

---

## 文件变更清单

### 新增文件
- `frontend/` — Vue 3 项目（完整目录）
- `web/main_api.py` — 纯 API 服务器
- `data/quotation_upgrade.sql` — 报价模块数据库迁移
- `src/m8_crm/browser_searcher.py` — Playwright 浏览器搜索
- `src/m8_crm/real_client_finder.py` — 真实客户搜索器
- `prompts/outreach/analyze_real_company.md` — 公司分析提示词

### 修改文件
- `run_web.py` — 改为启动 Vue + FastAPI
- `src/utils/prompts.py` — 更新 build_product_data()
- `web/routes/quotation.py` — 报价 API 重写
- `web/routes/clients.py` — 客户 API 增强
- `web/main_api.py` — 新增路由注册
- `prompts/seo/*.md` — 提示词优化
- `prompts/social/whatsapp.md` — 提示词优化
- `prompts/outreach/generate_potential_client.md` — v4.0 优化

---

## V3.0 → V4.0 迁移说明

旧版 HTMX 代码保留在 `web/templates/` 目录，可随时回退：
- `web/main.py` — V3.0 入口（HTMX 版）
- `web/templates/*.html` — V3.0 模板

新版 Vue 代码在 `frontend/` 目录：
- `web/main_api.py` — V4.0 入口（纯 API）
- `frontend/dist/` — Vue 构建产物

两个版本可并存，通过不同端口访问。
