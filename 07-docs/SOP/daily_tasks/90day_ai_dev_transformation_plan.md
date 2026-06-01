# 90天 AI应用开发转型计划

> 总教练模式 | 项目驱动 | 拒绝空泛学习
> 起点：外贸业务员（有Excel/Prompt/Hermes/Git基础）
> 终点：可独立交付AI自动化项目的实施人才
> 锚定项目：05_AI-外贸自动化系统（215个手动农具产品）

---

# 第一部分：90天总体路线图

---

## 阶段1（Day 1-30）：单产品跑通 + Python基础

**目标：** 用 Python 完成"读取产品数据 -> 调AI生成内容 -> 自动保存文件"的完整闭环

**核心成果：**

- 1个可运行的单产品自动化脚本（输入产品编码，输出全套营销内容）
- Python 基础能力：变量/循环/函数/文件读写/pandas读取CSV
- 产品数据库 SQLite 化，支持 SQL 查询
- SEO/详情页/RFQ/WhatsApp 四个流程全部自动化

**交付成果：**

1. `03-workflows/python/single_product_pipeline.py` -- 单产品自动化脚本
2. `04-database/sqlite/products.db` -- SQLite 产品数据库
3. 5个产品（GS-001, GF-001, GR-001, HT-001, SH-001）的完整内容包验证
4. 项目 README 更新，包含安装和运行说明

**需要补充的知识：**

- Python 基础语法（变量、循环、函数、文件操作）
- pandas 读取 CSV/Excel
- requests 或 Hermes CLI 调用 AI
- SQLite 基础（导入CSV、简单查询）
- 相对路径 vs 绝对路径、项目目录结构

---

## 阶段2（Day 31-60）：批量处理 + 数据驱动

**目标：** 从"一次处理1个"升级为"一次处理50个"，建立数据驱动的工作流

**核心成果：**

- 批量处理脚本（按品类/按市场筛选，批量生成）
- 自动生成汇总报表（CSV/Excel）
- 质量检查自动化（内容长度、格式验证、空值检测）
- Prompt 模板引擎（占位符替换，支持任意产品）

**交付成果：**

1. `03-workflows/python/batch_pipeline.py` -- 批量处理脚本
2. `03-workflows/python/prompt_template_engine.py` -- Prompt模板引擎
3. `03-workflows/python/quality_checker.py` -- 质量检查脚本
4. `05-output/reports/batch_summary.xlsx` -- 批量生产汇总报表
5. 至少50个产品的完整内容包
6. 批量处理SOP文档

**需要补充的知识：**

- pandas 高级操作（groupby、merge、apply、条件过滤）
- Python 异常处理（try/except）
- 日志记录（logging模块）
- 配置文件管理（JSON/YAML配置）
- 进度条和批量任务管理
- Excel 自动化生成（openpyxl）

---

## 阶段3（Day 61-90）：系统集成 + 作品集交付

**目标：** 将所有模块整合为可交付系统，完成作品集包装

**核心成果：**

- 完整的自动化系统（一键运行全量产品）
- 定时任务（cron / Windows Task Scheduler）
- 项目文档齐全（架构图、使用说明、API文档）
- GitHub 作品集完善（README、演示截图、项目说明）
- 简历项目描述（STAR格式，中英文）
- 模拟面试准备

**交付成果：**

1. `03-workflows/python/run_all.py` -- 一键运行入口
2. `config.json` -- 系统配置文件
3. 完整项目文档（架构图、使用说明、Troubleshooting）
4. GitHub 仓库完善（含演示截图、使用视频/GIF）
5. 简历项目描述（中英文 STAR 格式）
6. 项目演示PPT或文档
7. 215个产品的完整内容包（或至少100个+）

**需要补充的知识：**

- 项目文档编写规范
- 配置文件设计（config.json）
- Windows 定时任务设置
- Git 分支管理（feature/release分支）
- 项目演示技巧
- 简历 STAR 写法
- 面试常见问题准备

---

# 第二部分：12周详细执行计划

---

## Week 1（Day 1-7）：Python环境 + 单产品手动流程跑通

**本周目标：** 搭建 Python 环境，用 Python 脚本完成 1 个产品的完整内容生成

**本周项目任务：**

1. 安装 Python 和依赖库（pandas, openpyxl）
2. 写脚本读取产品数据库中 1 个产品的参数
3. 手动调用 AI 生成 4 类内容（SEO/详情/RFQ/WhatsApp）
4. 用 Python 自动保存结果到对应文件
5. 验证 2 个产品（GS-001, GF-001）

**本周需要补的知识：**

- Python 安装和 pip 使用
- 变量、字符串格式化（f-string）
- 函数定义和调用
- pandas.read_csv() 和 DataFrame 基本操作
- 文件读写（open/write）
- 项目路径管理（os.path）

**本周交付成果：**

- `03-workflows/python/single_product_pipeline.py`（v1）
- GS-001 和 GF-001 的完整内容包验证
- 项目 README 更新运行说明

**本周验收标准：**

- [ ] Python 脚本可独立运行
- [ ] 输入产品编码 -> 输出 4 类内容文件
- [ ] 所有文件保存到正确目录
- [ ] 每个文件 > 500 字节（非空壳）
- [ ] README 中包含运行命令和预期输出

---

## Week 2（Day 8-14）：SQLite导入 + 提示词模板化

**本周目标：** 产品数据库 SQLite 化，Prompt 从硬编码改为模板引擎

**本周项目任务：**

1. 将 CSV 导入 SQLite，建立 products.db
2. 写脚本用 SQL 查询获取产品数据
3. 将 6 个 Prompt 改为模板格式（占位符替换）
4. 编写 Prompt 模板引擎
5. 测试模板引擎对 3 个产品的适用性

**本周需要补的知识：**

- SQLite 基础（sqlite3模块、CREATE TABLE、SELECT）
- CSV 导入 SQLite 的方法
- 字符串模板替换（str.format 或 Template）
- JSON 读写
- SQL WHERE/JOIN 基础

**本周交付成果：**

- `04-database/sqlite/products.db`
- `03-workflows/python/prompt_template_engine.py`
- 6 个 Prompt 模板文件
- 3 个产品的模板生成验证

**本周验收标准：**

- [ ] products.db 包含 215 条记录
- [ ] 能用 SQL 查询任意产品
- [ ] 模板引擎输入产品数据 -> 输出完整 Prompt
- [ ] 3 个产品生成内容质量不劣于手动版
- [ ] 新增一个产品只需加数据，不需改代码

---

## Week 3（Day 15-21）：AI调用自动化 + 完整闭环

**本周目标：** 去掉"手动调AI"环节，实现脚本自动调AI并保存结果

**本周项目任务：**

1. 用 Hermes CLI 或 requests 实现脚本内自动调用 AI
2. 解析 AI 返回结果（JSON/Markdown）
3. 自动保存到正确目录和文件
4. 错误处理（API失败重试、空结果处理）
5. 完整跑通 5 个产品

**本周需要补的知识：**

- subprocess 调用命令行工具
- 或 requests 库调用 API
- JSON 解析（json.loads）
- try/except 异常处理
- 重试机制（简单循环）

**本周交付成果：**

- `03-workflows/python/single_product_pipeline.py`（v2，全自动版）
- 5 个产品的完整内容包（一键生成）
- `03-workflows/python/` 目录下 error_handling.md

**本周验收标准：**

- [ ] 一条命令跑完 1 个产品的全流程
- [ ] 中间无需人工干预
- [ ] API 失败时有错误提示和重试
- [ ] 5 个产品全部验证通过
- [ ] 运行日志输出清晰

---

## Week 4（Day 22-28）：批量处理 v1 + 品类批量生成

**本周目标：** 从"1个"升级到"一批"，按品类批量生成

**本周项目任务：**

1. 编写批量处理脚本（按 category 筛选）
2. 支持批量生成 10-20 个产品
3. 生成进度报告（成功/失败统计）
4. 生成汇总 CSV（product_code, seo_status, detail_status, rfq_status, whatsapp_status）
5. 批量生成 Digging Tools 品类（约100个产品）

**本周需要补的知识：**

- for 循环批量处理
- pandas groupby 和 filter
- 进度显示（简单 print 或 tqdm）
- CSV 汇总写入
- 批量任务失败跳过机制

**本周交付成果：**

- `03-workflows/python/batch_pipeline.py`
- `05-output/reports/batch_status.csv`
- Digging Tools 品类批量生成完成
- `03-workflows/python/batch_processing_sop.md`

**本周验收标准：**

- [ ] 一条命令批量处理一个品类
- [ ] 进度实时可见
- [ ] 失败产品自动跳过并记录
- [ ] 汇总 CSV 反映所有产品状态
- [ ] 至少 50 个产品有完整内容

---

## Week 5（Day 29-35）：批量处理 v2 + 多条件筛选 + 报表

**本周目标：** 批量处理支持多条件筛选，自动生成 Excel 报表

**本周项目任务：**

1. 支持多条件筛选（品类 + 市场 + 认证）
2. 用 openpyxl 生成格式化 Excel 报表
3. 报表包含：产品参数、SEO标题、卖点、状态
4. 批量生成剩余品类（Weeding/Cutting 等）
5. 质量检查：内容长度、格式验证

**本周需要补的知识：**

- openpyxl 基础（创建 workbook、写单元格、设置格式）
- pandas to_excel
- 条件过滤组合
- 数据验证逻辑

**本周交付成果：**

- `03-workflows/python/report_generator.py`
- `05-output/reports/full_batch_report.xlsx`
- 质量检查脚本
- 100+ 个产品的完整内容包

**本周验收标准：**

- [ ] 支持任意组合条件筛选
- [ ] Excel 报表格式清晰，可直接给客户看
- [ ] 质量检查自动标记不合格内容
- [ ] 100+ 产品完成

---

## Week 6（Day 36-42）：Prompt优化 + 市场本地化自动化

**本周目标：** 优化 Prompt 质量，增加市场本地化自动化

**本周项目任务：**

1. 审计已有 Prompt 的生成质量
2. 优化得分最低的 2 个 Prompt
3. 自动化市场本地化（africa/europe/north_america/south_america 四个版本）
4. 批量生成市场版本
5. 对比不同市场版本的差异

**本周需要补的知识：**

- 数据对比分析
- 多文件批量处理
- 文本差异比较（difflib 基础）

**本周交付成果：**

- 优化后的 6 个 Prompt 模板
- `03-workflows/python/market_localization.py`
- 市场版本批量生成完成
- `07-docs/testing_reports/prompt_audit_report.md`

**本周验收标准：**

- [ ] 每个产品有 4 个市场版本
- [ ] 市场版本质量通过人工抽查
- [ ] Prompt 审计报告完成
- [ ] 市场本地化可一键运行

---

## Week 7（Day 43-49）：配置系统 + 日志系统

**本周目标：** 建立配置文件和日志系统，提升工程化水平

**本周项目任务：**

1. 创建 config.json 配置文件（API设置、路径、批量大小等）
2. 添加 logging 日志系统（info/warning/error）
3. 日志输出到文件
4. 脚本从配置文件读取参数
5. 支持命令行参数覆盖配置

**本周需要补的知识：**

- JSON 配置文件设计
- Python logging 模块
- argparse 命令行参数
- 配置文件优先级（默认 < 配置 < 命令行）

**本周交付成果：**

- `config.json`
- `03-workflows/python/` 下所有脚本更新为读取配置
- 日志文件输出
- `07-docs/configuration_guide.md`

**本周验收标准：**

- [ ] 修改配置无需改代码
- [ ] 日志文件记录完整运行过程
- [ ] 命令行参数可覆盖配置
- [ ] 配置文档清晰

---

## Week 8（Day 50-56）：定时任务 + 一键运行

**本周目标：** 实现定时自动运行和一键全量处理

**本周项目任务：**

1. 编写 run_all.py 一键运行入口
2. 设置 Windows 定时任务（每天/每周自动运行）
3. 定时任务自动生成日报
4. 异常邮件/文件通知
5. 全量 215 个产品跑通

**本周需要补的知识：**

- Windows Task Scheduler
- 或 cron（WSL环境）
- 定时任务调试
- 日报自动生成

**本周交付成果：**

- `03-workflows/python/run_all.py`
- Windows 定时任务配置好
- 日报自动生成
- 215 个产品完整内容包

**本周验收标准：**

- [ ] 一条命令跑完全部 215 个产品
- [ ] 定时任务可自动触发
- [ ] 日报包含成功/失败统计
- [ ] 215 个产品全覆盖

---

## Week 9（Day 57-63）：项目文档 + 架构图

**本周目标：** 完善项目文档，让外人能看懂和使用

**本周项目任务：**

1. 编写项目架构图（ASCII 或 Markdown）
2. 编写完整使用说明
3. 编写安装部署文档
4. 编写 Troubleshooting 文档
5. 更新所有模块的 README

**本周需要补的知识：**

- 技术文档写作规范
- ASCII 图表或 Markdown 图表
- README 最佳实践

**本周交付成果：**

- `README.md`（完整版）
- `07-docs/architecture.md`
- `07-docs/installation.md`
- `07-docs/troubleshooting.md`
- `07-docs/user_guide.md`

**本周验收标准：**

- [ ] 新人能根据文档独立安装和运行
- [ ] 架构图清晰展示数据流
- [ ] Troubleshooting 覆盖常见问题
- [ ] 所有文档格式统一

---

## Week 10（Day 64-70）：GitHub作品集 + 演示材料

**本周目标：** 将项目包装为可展示的 GitHub 作品集

**本周项目任务：**

1. 清理 Git 仓库（删除测试文件、整理目录）
2. 编写精美的 README（含截图、功能列表、架构图）
3. 生成演示截图和 GIF
4. 创建 demo/ 目录放示例输出
5. 推送到 GitHub

**本周需要补的知识：**

- GitHub README 最佳实践
- 截图/GIF 制作
- .gitignore 规范
- Git tag 和 release

**本周交付成果：**

- GitHub 仓库完善
- 演示截图和 GIF
- `demo/` 目录
- Git release tag

**本周验收标准：**

- [ ] README 有吸引力（功能列表、截图、架构图）
- [ ] 仓库结构清晰
- [ ] demo 目录有可预览的输出
- [ ] Git 历史整洁

---

## Week 11（Day 71-77）：简历包装 + 面试准备

**本周目标：** 完成简历项目描述，准备面试

**本周项目任务：**

1. 用 STAR 格式写中文简历项目描述
2. 用 STAR 格式写英文简历项目描述
3. 准备 5 个面试常见问题及答案
4. 模拟技术面试（SQL/Python/自动化）
5. 准备项目演示脚本（3分钟介绍）

**本周需要补的知识：**

- STAR 简历写法
- 面试常见问题
- 项目演示技巧

**本周交付成果：**

- `07-docs/portfolio/resume_cn.md`
- `07-docs/portfolio/resume_en.md`
- `07-docs/portfolio/interview_qa.md`
- `07-docs/portfolio/demo_script.md`

**本周验收标准：**

- [ ] 中英文简历项目描述完成
- [ ] 5 个面试问题有准备好的答案
- [ ] 3 分钟项目演示熟练
- [ ] 所有成果可量化

---

## Week 12（Day 78-90）：查漏补缺 + 最终交付

**本周目标：** 补齐遗漏，完成最终交付

**本周项目任务：**

1. 回顾所有交付物，查漏补缺
2. 运行完整测试（215 个产品全量）
3. 最终 Git 提交
4. 写 90 天总结
5. 制定投递计划

**本周交付成果：**

- 最终版完整项目
- 90 天总结报告
- 求职投递计划

**本周验收标准：**

- [ ] 所有交付物清单核对完毕
- [ ] 215 个产品全量测试通过
- [ ] Git 仓库最终版
- [ ] 可以开始投递

---

# 第三部分：Day 1 - Day 14 详细每日任务

---

## Day 1：Python环境搭建 + 读取第一个产品

### 今日目标

安装 Python 环境，用 Python 成功读取 product_database_filled.csv 中 GS-001 的完整参数并打印。

### 主任务

任务名称：Python环境验证 + CSV读取

执行步骤：

1. 确认 Python 已安装：终端运行 `python --version`
2. 如未安装，下载 Python 3.12+（https://python.org），安装时勾选"Add to PATH"
3. 安装依赖：`pip install pandas openpyxl`
4. 创建文件 `03-workflows/python/day01_read_product.py`
5. 在脚本中读取 CSV 并打印 GS-001 的所有字段：

```python
import pandas as pd
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

csv_path = os.path.join(PROJECT_ROOT, '04-database', 'csv', 'product_database_filled.csv')
df = pd.read_csv(csv_path, encoding='utf-8-sig')

product = df[df['product_id'] == 'GS-001']
if len(product) > 0:
    for col in product.columns:
        print(f"{col}: {product[col].values[0]}")
else:
    print("ERROR: GS-001 not found")

print(f"\nTotal products in CSV: {len(df)}")
print(f"Columns: {list(df.columns)}")
```

6. 运行验证：`python 03-workflows/python/day01_read_product.py`

输出文件：`day01_read_product.py`
所属目录：`03-workflows/python/`
预计耗时：60分钟

### 知识补充

- `os.path.dirname()` 和 `os.path.abspath()` 的作用：获取脚本所在目录的上级目录，用于构建相对路径
- `pandas.read_csv()` 返回一个 DataFrame（类似 Excel 表格的 Python 对象）
- `df[df['col'] == 'value']` 是条件过滤，返回匹配的行
- 如果 CSV 中文显示乱码，尝试 `pd.read_csv(csv_path, encoding='utf-8-sig')`

### 项目文档

- 更新 `08-git/README.md`：在"环境要求"部分添加 Python 版本和依赖库列表

### Git任务

```bash
git add 03-workflows/python/day01_read_product.py
git add 08-git/README.md
git commit -m "feat: Python环境验证 + CSV读取脚本 (Day 1)"
```

### 今日验收标准

- [ ] `python --version` 输出 3.10+
- [ ] `pip list` 显示 pandas 和 openpyxl 已安装
- [ ] 脚本运行成功，打印出 GS-001 的 31 个字段
- [ ] 打印出总产品数 = 215
- [ ] 路径使用相对路径（非硬编码绝对路径）

---

## Day 2：函数封装 + 多产品读取

### 今日目标

将 Day 1 的代码封装为函数，支持输入任意产品编码返回完整参数。

### 主任务

任务名称：产品读取函数封装

执行步骤：

1. 创建 `03-workflows/python/product_reader.py`
2. 编写 `load_products()` 函数：读取 CSV 返回 DataFrame
3. 编写 `get_product(product_id)` 函数：输入编码，返回产品字典
4. 编写 `get_products_by_category(category)` 函数：按品类筛选
5. 测试：读取 GS-001, GF-001, GR-001 三个产品并打印
6. 编写 `list_categories()` 函数：列出所有品类及产品数

```python
import pandas as pd
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_products():
    csv_path = os.path.join(PROJECT_ROOT, '04-database', 'csv', 'product_database_filled.csv')
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    return df

def get_product(product_id):
    df = load_products()
    row = df[df['product_id'] == product_id]
    if len(row) == 0:
        return None
    return row.iloc[0].to_dict()

def get_products_by_category(category):
    df = load_products()
    return df[df['category'] == category]

def list_categories():
    df = load_products()
    return df.groupby('category').size().to_dict()

if __name__ == '__main__':
    p = get_product('GS-001')
    print(f"Product: {p['product_name_en']}")
    print(f"Category: {p['category']}")
    print(f"Material: {p['material']}")

    cats = list_categories()
    print(f"\nCategories: {cats}")
```

输出文件：`product_reader.py`
所属目录：`03-workflows/python/`
预计耗时：60分钟

### 知识补充

- 函数定义：`def 函数名(参数):`
- 返回值：`return 值`，没有 return 默认返回 None
- `if __name__ == '__main__':` 的作用：只在直接运行脚本时执行，被 import 时不执行
- DataFrame 转字典：`row.iloc[0].to_dict()`
- groupby + size：按列分组并计数

### 项目文档

无

### Git任务

```bash
git add 03-workflows/python/product_reader.py
git commit -m "feat: 产品读取模块（函数封装）(Day 2)"
```

### 今日验收标准

- [ ] `get_product('GS-001')` 返回包含 31 个字段的字典
- [ ] `get_product('NOTEXIST')` 返回 None
- [ ] `get_products_by_category('Digging Tools')` 返回正确数量
- [ ] `list_categories()` 输出所有品类和产品数
- [ ] 其他脚本可以 `from product_reader import get_product` 导入使用

---

## Day 3：Prompt模板引擎 v1

### 今日目标

编写 Prompt 模板引擎，将 SEO Prompt 从硬编码改为占位符替换。

### 主任务

任务名称：SEO Prompt模板化

执行步骤：

1. 读取 `02-prompts/seo/seo_title_prompt.md`，分析其中需要替换的产品字段
2. 创建 `03-workflows/python/prompt_templates/seo_title_template.txt`，将硬编码产品数据替换为 `{product_name_en}`, `{material}`, `{category}` 等占位符
3. 创建 `03-workflows/python/prompt_engine.py`
4. 测试：`python 03-workflows/python/prompt_engine.py`
5. 验证生成的 Prompt 中产品数据是否正确替换

输出文件：

- `prompt_templates/seo_title_template.txt`
- `prompt_engine.py`

所属目录：`03-workflows/python/`
预计耗时：90分钟

### 知识补充

- 字符串 `.replace(old, new)` 替换
- f-string 中的 `{}` 是 Python 语法，模板中的 `{product_name_en}` 是自定义占位符
- 模板引擎原理：读取模板文本 -> 遍历产品数据 -> 逐个替换占位符
- pandas 中的空值表现为 `nan`，需要替换为 N/A

### 项目文档

无

### Git任务

```bash
git add 03-workflows/python/prompt_engine.py
git add 03-workflows/python/prompt_templates/
git commit -m "feat: SEO Prompt模板引擎 v1 (Day 3)"
```

### 今日验收标准

- [ ] `seo_title_template.txt` 中所有硬编码产品数据已替换为占位符
- [ ] 生成的 Prompt 包含 GS-001 的真实数据
- [ ] 不存在的编码返回错误信息
- [ ] 占位符被正确替换
- [ ] Prompt 长度 > 200 字符

---

## Day 4：Prompt模板扩充 + 4类内容模板

### 今日目标

将 selling_points、alibaba_detail、rfq_reply、whatsapp_script 四个 Prompt 也模板化。

### 主任务

任务名称：4类Prompt模板化

执行步骤：

1. 为每个 Prompt 创建模板文件：
   - `prompt_templates/selling_points_template.txt`
   - `prompt_templates/alibaba_detail_template.txt`
   - `prompt_templates/rfq_reply_template.txt`
   - `prompt_templates/whatsapp_script_template.txt`
2. 将每个原始 Prompt 中的产品示例数据替换为占位符
3. 在 `prompt_engine.py` 中添加对应的生成函数
4. 测试每个函数，确认占位符替换正确

输出文件：4个模板文件 + 更新的 prompt_engine.py
所属目录：`03-workflows/python/prompt_templates/` 和 `03-workflows/python/`
预计耗时：90分钟

### 知识补充

- 模板复用的关键：原始 Prompt 中的"指令部分"保持不变，只替换"数据部分"
- 不同 Prompt 需要的字段不同（SEO 需要 keywords，WhatsApp 不需要）
- 占位符在产品数据中不存在时应替换为 N/A 而不是留空

### 项目文档

- 更新 `02-prompts/prompt_index.md`：标记哪些 Prompt 已有模板版本

### Git任务

```bash
git add 03-workflows/python/prompt_templates/
git add 03-workflows/python/prompt_engine.py
git commit -m "feat: 4类Prompt全部模板化 (Day 4)"
```

### 今日验收标准

- [ ] 4 个模板文件全部创建
- [ ] 每个生成函数输出正确
- [ ] 每个 Prompt 包含对应产品的真实数据

---

## Day 5：AI调用 + 内容生成

### 今日目标

在脚本中集成 AI 调用，用生成的 Prompt 调 AI 并获取结果。

### 主任务

任务名称：AI调用集成

执行步骤：

1. 确定 AI 调用方式：使用 Hermes CLI 或通过当前 Agent 调用
2. 创建 `03-workflows/python/ai_client.py`，封装 AI 调用逻辑
3. 创建 `03-workflows/python/content_generator.py`，组合 prompt_engine + ai_client
4. 测试：运行脚本 -> 生成 Prompt -> 调 AI -> 获取结果

输出文件：

- `ai_client.py`
- `content_generator.py`

所属目录：`03-workflows/python/`
预计耗时：90分钟

### 知识补充

- `subprocess.run()` 用于在 Python 中执行命令行命令
- `capture_output=True` 捕获标准输出
- `timeout=120` 设置超时时间（秒）
- 根据实际 AI 调用方式调整实现

### 项目文档

- 创建 `03-workflows/python/AI_INTEGRATION.md` 记录 AI 调用方式配置

### Git任务

```bash
git add 03-workflows/python/ai_client.py
git add 03-workflows/python/content_generator.py
git add 03-workflows/python/AI_INTEGRATION.md
git commit -m "feat: AI调用集成 (Day 5)"
```

### 今日验收标准

- [ ] `ai_client.py` 可成功调用 AI 并获取返回
- [ ] `content_generator.py` 可生成 SEO 内容
- [ ] 返回内容非空且包含产品信息
- [ ] AI 调用过程有日志输出

---

## Day 6：内容自动保存

### 今日目标

将 AI 生成的内容自动保存到正确的文件和目录。

### 主任务

任务名称：内容自动保存

执行步骤：

1. 创建 `03-workflows/python/file_manager.py`，包含：
   - `ensure_dir(dir_path)` - 确保目录存在
   - `get_product_dir(product_id)` - 获取产品输出目录
   - `save_content(product_id, content_type, content)` - 保存内容到文件
   - `save_seo_as_json(product_id, seo_text)` - SEO 内容转 JSON 保存
2. 创建 `03-workflows/python/single_product_pipeline.py`，串联全流程
3. 测试：`python 03-workflows/python/single_product_pipeline.py GS-001`

输出文件：`file_manager.py`, `single_product_pipeline.py`
所属目录：`03-workflows/python/`
预计耗时：90分钟

### 知识补充

- `os.makedirs(path, exist_ok=True)` 创建多级目录
- `json.dump()` 将 Python 对象写入 JSON 文件
- `sys.argv` 获取命令行参数
- 文件写入模式 'w' 会覆盖已有文件

### 项目文档

- 更新 `08-git/README.md` 添加"运行单个产品"的说明

### Git任务

```bash
git add 03-workflows/python/file_manager.py
git add 03-workflows/python/single_product_pipeline.py
git commit -m "feat: 内容自动保存 + 单产品完整流水线 (Day 6)"
```

### 今日验收标准

- [ ] 输入产品编码，一键生成 5 类内容文件
- [ ] `05-output/export_files/GS-001/` 下生成所有文件
- [ ] 每个文件 > 200 字节
- [ ] 支持命令行参数指定产品编码
- [ ] 文件保存路径正确

---

## Day 7：Week 1 验证 + 第二产品测试

### 今日目标

用 GS-001 以外的产品（GF-001, GR-001）验证流水线通用性，修复发现的问题。

### 主任务

任务名称：多产品验证 + Bug修复

执行步骤：

1. 运行 `python single_product_pipeline.py GF-001`
2. 运行 `python single_product_pipeline.py GR-001`
3. 检查每个产品的输出文件是否完整
4. 记录发现的问题（空值处理、字段缺失、路径错误等）
5. 修复所有发现的问题
6. 编写 Week 1 总结文档

输出文件：

- `07-docs/SOP/daily_tasks/week1_summary.md`
- 修复后的所有脚本

所属目录：`03-workflows/python/` 和 `07-docs/SOP/daily_tasks/`
预计耗时：120分钟

### 知识补充

- 不同产品的数据差异可能导致 Prompt 填充异常
- pandas 中空值表现为 `nan`，需要特殊处理
- 测试多个用例是发现 Bug 的最有效方式

### 项目文档

- 创建 `07-docs/SOP/daily_tasks/week1_summary.md`
- 更新 `08-git/README.md`

### Git任务

```bash
git add 03-workflows/python/
git add 07-docs/SOP/daily_tasks/week1_summary.md
git commit -m "feat: 多产品验证通过 + Week 1总结 (Day 7)"
```

### 今日验收标准

- [ ] GS-001, GF-001, GR-001 三个产品全部验证通过
- [ ] 每个产品 5 个输出文件完整
- [ ] 所有发现的问题已修复
- [ ] Week 1 总结文档已创建
- [ ] `progress_tracker.md` 中 Week 1 已标记完成

---

## Day 8：WhatsApp自动化 + 4类内容全通

### 今日目标

补充 WhatsApp 脚本的自动化生成，完成 4 类内容的全自动流水线。

### 主任务

任务名称：WhatsApp内容自动化

执行步骤：

1. 确认 `generate_whatsapp_prompt()` 函数工作正常
2. 在 `single_product_pipeline.py` 中添加 WhatsApp 生成步骤
3. 测试 GS-001 的 WhatsApp 内容生成
4. 验证 3 个产品的 WhatsApp 内容质量

输出文件：更新的 `single_product_pipeline.py`
所属目录：`03-workflows/python/`
预计耗时：60分钟

### 知识补充

- WhatsApp 话术需要区分目标市场语气（正式 vs 随意）
- 可以复用已有的 prompt 模板机制

### 项目文档

无

### Git任务

```bash
git add 03-workflows/python/single_product_pipeline.py
git commit -m "feat: WhatsApp自动化 + 4类内容全通 (Day 8)"
```

### 今日验收标准

- [ ] 流水线输出 5 类内容（SEO/卖点/详情/RFQ/WhatsApp）
- [ ] 每个文件 > 300 字节
- [ ] WhatsApp 内容包含产品关键卖点
- [ ] 3 个产品验证通过

---

## Day 9：SQLite导入 + 基础查询

### 今日目标

将 CSV 导入 SQLite，支持 SQL 查询产品数据。

### 主任务

任务名称：SQLite数据库建立

执行步骤：

1. 创建 `03-workflows/python/setup_sqlite.py`
2. 运行：`python 03-workflows/python/setup_sqlite.py`
3. 验证：用 DB Browser for SQLite 打开 products.db 确认数据正确

输出文件：`setup_sqlite.py`, `04-database/sqlite/products.db`
所属目录：`03-workflows/python/` 和 `04-database/sqlite/`
预计耗时：60分钟

### 知识补充

- SQLite 是轻量级嵌入式数据库，无需安装服务器
- `df.to_sql()` 将 DataFrame 直接写入数据库表
- `sqlite3.connect()` 连接数据库
- `conn.execute().fetchall()` 执行 SQL 并获取结果

### 项目文档

- 更新 `04-database/knowledge_base_design.md` 添加 SQLite 说明

### Git任务

```bash
git add 03-workflows/python/setup_sqlite.py
git add 04-database/sqlite/products.db
git commit -m "feat: CSV导入SQLite + 基础查询 (Day 9)"
```

### 今日验收标准

- [ ] products.db 包含 215 条记录
- [ ] `SELECT COUNT(*) FROM products` 返回 215
- [ ] 表结构与 CSV 列名一致
- [ ] 可用 SQL 查询任意产品

---

## Day 10：SQL查询集成到产品读取模块

### 今日目标

修改 product_reader.py 支持从 SQLite 读取（替代 CSV），提升查询性能。

### 主任务

任务名称：SQLite集成到product_reader

执行步骤：

1. 修改 `product_reader.py`，添加 `get_product_sql(product_id)` 函数
2. 保持原有的 `get_product()` 函数作为 fallback
3. 测试查询性能对比（CSV vs SQLite）
4. 更新 `prompt_engine.py` 使用 SQL 版本

输出文件：更新的 `product_reader.py`
所属目录：`03-workflows/python/`
预计耗时：60分钟

### 知识补充

- SQLite 查询比 CSV 快，尤其在数据量大时
- 可以保留两种读取方式，通过配置切换

### 项目文档

无

### Git任务

```bash
git add 03-workflows/python/product_reader.py
git commit -m "feat: product_reader集成SQLite (Day 10)"
```

### 今日验收标准

- [ ] `get_product_sql('GS-001')` 返回与 `get_product()` 相同结果
- [ ] 查询响应时间 < 10ms
- [ ] 原有功能不受影响

---

## Day 11：批量读取 + 品类筛选

### 今日目标

编写批量产品读取功能，支持按品类筛选并返回列表。

### 主任务

任务名称：批量产品读取

执行步骤：

1. 在 `product_reader.py` 中添加：
   - `get_products_by_category_sql(category)` -- SQL 版
   - `get_pending_products()` -- 获取所有 AI 字段为 pending 的产品
   - `get_product_codes()` -- 获取所有产品编码列表
2. 测试：
   - 列出 Digging Tools 所有产品
   - 统计各品类 pending 数量

输出文件：更新的 `product_reader.py`
所属目录：`03-workflows/python/`
预计耗时：60分钟

### 知识补充

- SQL: `SELECT * FROM products WHERE category = 'Digging Tools'`
- `cursor.fetchall()` 返回所有匹配行
- 批量操作前先确认筛选结果正确

### 项目文档

无

### Git任务

```bash
git add 03-workflows/python/product_reader.py
git commit -m "feat: 批量读取 + 品类筛选 (Day 11)"
```

### 今日验收标准

- [ ] `get_products_by_category_sql('Digging Tools')` 返回正确列表
- [ ] `get_pending_products()` 返回 pending 产品列表
- [ ] 结果与 Excel 数据一致

---

## Day 12：批量处理脚本 v1

### 今日目标

编写批量处理脚本 v1，对一个品类的产品逐个生成内容。

### 主任务

任务名称：批量处理脚本

执行步骤：

1. 创建 `03-workflows/python/batch_pipeline.py`
2. 测试：处理 Digging Tools 前 3 个产品
3. 验证输出

输出文件：`batch_pipeline.py`
所属目录：`03-workflows/python/`
预计耗时：90分钟

### 知识补充

- DataFrame.iterrows() 遍历行
- try/except 捕获单个产品失败不影响其他产品
- time.sleep() 控制请求频率

### 项目文档

- 创建 `03-workflows/python/BATCH_PROCESSING.md`

### Git任务

```bash
git add 03-workflows/python/batch_pipeline.py
git add 03-workflows/python/BATCH_PROCESSING.md
git commit -m "feat: 批量处理脚本 v1 (Day 12)"
```

### 今日验收标准

- [ ] 批量处理 3 个产品全部成功
- [ ] 单个失败不影响其他产品
- [ ] 输出成功/失败统计
- [ ] 所有文件正确保存

---

## Day 13：批量状态追踪

### 今日目标

为批量处理添加状态追踪，生成 CSV 报告。

### 主任务

任务名称：批量状态追踪

执行步骤：

1. 在 `batch_pipeline.py` 中添加状态记录和 CSV 输出
2. 创建 `05-output/reports/batch_status.csv`
3. 记录每个产品的处理状态和时间
4. 支持断点续传（跳过已处理的产品）

输出文件：更新的 `batch_pipeline.py`
所属目录：`03-workflows/python/`
预计耗时：60分钟

### 知识补充

- CSV 记录格式：product_id, content_type, status, timestamp
- 断点续传：处理前检查文件是否已存在

### 项目文档

无

### Git任务

```bash
git add 03-workflows/python/batch_pipeline.py
git commit -m "feat: 批量状态追踪 + 断点续传 (Day 13)"
```

### 今日验收标准

- [ ] batch_status.csv 正确记录处理状态
- [ ] 重复运行跳过已处理产品
- [ ] 状态文件格式清晰

---

## Day 14：Week 2 总结 + 批量处理5个产品

### 今日目标

完成 Week 2 总结，批量处理 5 个产品并验证。

### 主任务

任务名称：Week 2 验证 + 总结

执行步骤：

1. 批量处理 5 个产品（Digging Tools 前 5 个）
2. 验证所有输出文件
3. 生成 batch_status.csv
4. 写 Week 2 总结
5. 更新 progress_tracker.md
6. Git 提交

输出文件：

- `07-docs/SOP/daily_tasks/week2_summary.md`
- `05-output/reports/batch_status.csv`

所属目录：`07-docs/SOP/daily_tasks/` 和 `05-output/reports/`
预计耗时：120分钟

### 知识补充

无新知识，纯实操验证

### 项目文档

- 创建 `week2_summary.md`
- 更新 `progress_tracker.md`

### Git任务

```bash
git add .
git commit -m "feat: Week 2完成 - 批量处理5个产品验证通过 (Day 14)"
```

### 今日验收标准

- [ ] 5 个产品批量处理完成
- [ ] 每个产品 5 类内容完整
- [ ] batch_status.csv 已生成
- [ ] Week 2 总结文档完成
- [ ] progress_tracker.md 已更新
- [ ] Git 提交完成
