# Phase 2 实操冲刺计划：从"有系统"到"能产出"

> 周期：30天（P2-D1 ~ P2-D30）
> 每日时长：3~5小时
> 核心原则：每天必须有文件输出，每天必须有可见进度
> 禁止：纯理论学习、看教程、无输出型学习

---

## 阶段路线图

```
Week 1 (Day 1-7)   → 清理+单产品跑通 → 1个完整产品包+工作流文档
Week 2 (Day 8-14)  → 批量生产10个产品 → 10个产品×4类内容
Week 3 (Day 15-21) → 自动化管道建设 → Cron定时任务+批量脚本
Week 4 (Day 22-28) → 市场扩展+高级内容 → 3个国家报告+RFQ批量
Week 5 (Day 29-30) → 作品集整理 → GitHub作品集+简历更新
```

---

# P2-D1：环境检查 + 选定标杆产品

## 今日目标

- 确认项目所有文件状态正常
- 选定1个标杆产品作为"全流程跑通"对象
- 生成该产品的完整内容包

## 主任务

### 任务1：项目状态检查

* 内容：检查04-database/excel/product_database_filled.xlsx是否可打开，确认215条数据完整；检查02-prompts/下所有prompt文件是否存在且可读
* 步骤：
  1. 打开Excel确认数据行数=215
  2. 列出02-prompts/下所有文件，确认6个prompt都存在
  3. 列出05-output/export_files/下已有5个产品的输出，标记哪些文件是空壳（<100字节）
* 输出：检查报告写入 07-docs/SOP/daily_tasks/phase2_audit.md
* 耗时：45分钟

### 任务2：选定标杆产品并生成完整内容

* 内容：从215个产品中选1个（建议选GS-001 garden spade，已有基础输出），用AI重新生成完整内容包
* 步骤：
  1. 从Excel中找到GS-001的完整参数
  2. 用seo_title_prompt生成3个SEO标题
  3. 用selling_points_prompt生成5-8条卖点
  4. 用alibaba_detail_prompt生成完整详情页
  5. 用rfq_reply_prompt生成RFQ回复
  6. 用whatsapp_script_prompt生成WhatsApp话术
  7. 所有输出写入 05-output/export_files/GS-001/ 对应文件
* 输出：GS-001/ 目录下6个文件全部有实质内容（每个>500字节）
* 耗时：90分钟

### 任务3：记录完整工作流

* 内容：把今天跑通的完整流程记录下来，作为后续批量生产的SOP
* 步骤：将每个步骤的输入、prompt、输出格式、保存路径写入文档
* 输出：03-workflows/batch_processing/single_product_workflow.md
* 耗时：30分钟

## 辅助学习任务

* 复习00-config/field_mapping.md，确认31个字段的含义
* 阅读02-prompts/prompt_index.md，理解各prompt之间的关系
* 耗时：30分钟

## 英语口语任务

* 用英语口头描述GS-001这个产品的5个卖点（录音或打字）
* 重点词汇：ergonomic, durability, corrosion-resistant, leverage, heat-treated
* 耗时：15分钟

## 今日验收标准

- [ ] Excel数据库可打开，215条数据确认
- [ ] 6个prompt文件全部存在
- [ ] GS-001的6个输出文件全部有实质内容
- [ ] 单产品工作流文档已创建
- [ ] 英语口语任务完成

## 今日复盘问题

1. 今天哪个prompt生成的效果最好？哪个最差？
2. 哪个步骤最耗时？如何优化？
3. 明天的批量生产计划是否需要调整？

---

# P2-D2：批量生产第1批（5个产品-除草工具类）

## 今日目标

- 用D1跑通的工作流，批量生成5个除草工具类产品内容
- 建立批量生成的节奏

## 主任务

### 任务1：从Excel筛选5个除草工具产品

* 内容：从product_database_filled.xlsx中筛选category=Weeding Tools且AI字段为pending的5个产品
* 步骤：
  1. 打开Excel，筛选Weeding Tools类别
  2. 选出前5个AI字段为pending的产品编码
  3. 记录编码到 03-workflows/batch_processing/batch_01_list.txt
* 输出：batch_01_list.txt（5个产品编码）
* 耗时：20分钟

### 任务2：批量生成SEO标题（5个产品×3版本=15条）

* 内容：对5个产品分别调用seo_title_prompt
* 步骤：逐个产品调用AI，输出写入对应产品的seo_titles.json
* 输出：5个产品的seo_titles.json文件
* 耗时：60分钟

### 任务3：批量生成产品卖点（5个产品×5-8条）

* 内容：对5个产品分别调用selling_points_prompt
* 步骤：逐个产品调用AI，输出写入对应产品的selling_points.json
* 输出：5个产品的selling_points.json文件
* 耗时：60分钟

### 任务4：批量生成详情页（5个产品）

* 内容：对5个产品分别调用alibaba_detail_prompt
* 步骤：逐个产品调用AI，输出写入对应产品的alibaba_detail.md
* 输出：5个产品的alibaba_detail.md文件
* 耗时：90分钟

## 辅助学习任务

* 观察不同产品生成的质量差异，记录在 07-docs/project_notes/batch_quality_notes.md
* 耗时：20分钟

## 英语口语任务

* 用英语描述这5个产品的共同卖点和差异点
* 练习句式：Compared to X, this product offers... / What sets this apart is...
* 耗时：15分钟

## 今日验收标准

- [ ] 5个产品编码列表已创建
- [ ] 5个seo_titles.json（每个至少3个标题）
- [ ] 5个selling_points.json（每个至少5条卖点）
- [ ] 5个alibaba_detail.md（每个>2KB）
- [ ] 质量笔记已记录

## 今日复盘问题

1. 批量生成时，哪些产品信息不足导致AI输出质量差？
2. 是否需要先补全Excel中的某些字段？
3. 今天的节奏是否合理？明天是否需要减少产品数量？

---

# P2-D3：批量生产第1批续 + RFQ+WhatsApp

## 今日目标

- 完成D1批次剩余内容（RFQ+WhatsApp）
- 汇总第1批成果到CSV

## 主任务

### 任务1：批量生成RFQ回复（5个产品）

* 内容：对D1的5个产品调用rfq_reply_prompt
* 步骤：逐个产品调用AI，输出写入对应产品的rfq_template.txt（或rfq_reply.md）
* 输出：5个rfq回复文件（每个>500字节）
* 耗时：60分钟

### 任务2：批量生成WhatsApp话术（5个产品）

* 内容：对D1的5个产品调用whatsapp_script_prompt
* 步骤：逐个产品调用AI，输出写入对应产品的whatsapp.txt
* 输出：5个whatsapp话术文件（每个>500字节）
* 耗时：60分钟

### 任务3：创建第1批汇总CSV

* 内容：将5个产品的SEO标题和卖点汇总到CSV
* 步骤：
  1. 读取5个产品的seo_titles.json和selling_points.json
  2. 合并为两行CSV：batch_01_seo_summary.csv 和 batch_01_selling_points_summary.csv
  3. 存入 05-output/export_files/
* 输出：2个汇总CSV文件
* 耗时：45分钟

### 任务4：Git提交

* 内容：将D1-D3的所有产出提交到Git
* 步骤：git add → git commit → git push
* 输出：Git提交记录
* 耗时：15分钟

## 辅助学习任务

* 回顾05-output/export_files/下所有产品的输出质量，找出共性问题
* 耗时：20分钟

## 英语口语任务

* 模拟：用英语给一个非洲客户写一段WhatsApp首次联系消息
* 场景：你发现他在阿里国际站浏览了你的garden hoe产品
* 耗时：15分钟

## 今日验收标准

- [ ] 5个RFQ回复文件（每个>500字节）
- [ ] 5个WhatsApp话术文件（每个>500字节）
- [ ] 2个汇总CSV
- [ ] Git提交完成
- [ ] Week 1成果：6个产品（GS-001+5个新）有完整内容

## 今日复盘问题

1. RFQ和WhatsApp生成的质量如何？是否需要调整prompt？
2. 汇总CSV的格式是否方便后续使用？
3. Week 1结束，你对整个流程的熟练度如何？

---

# P2-D4：第2批-挖掘工具类（5个产品-SEO+卖点）

## 今日目标

- 开始第2批：5个挖掘工具类产品
- 只生成SEO标题和卖点（分步批量，避免过载）

## 主任务

### 任务1：筛选5个挖掘工具产品

* 内容：从Excel筛选category=Digging Tools且AI字段为pending的5个产品
* 输出：batch_02_list.txt
* 耗时：15分钟

### 任务2：批量生成SEO标题（5个产品）

* 内容：调用seo_title_prompt
* 输出：5个seo_titles.json
* 耗时：60分钟

### 任务3：批量生成卖点（5个产品）

* 内容：调用selling_points_prompt
* 输出：5个selling_points.json
* 耗时：60分钟

### 任务4：市场本地化-Africa版本（3个产品）

* 内容：选3个产品，用market_localization_prompt生成非洲市场版本
* 输出：3个产品的market_versions/africa.txt
* 耗时：60分钟

## 辅助学习任务

* 对比D2（除草工具）和D4（挖掘工具）的SEO标题差异，记录关键词模式
* 耗时：20分钟

## 英语口语任务

* 练习：用英语介绍一个garden fork的3个核心卖点
* 录音，回听改进发音
* 耗时：15分钟

## 今日验收标准

- [ ] batch_02_list.txt
- [ ] 5个seo_titles.json
- [ ] 5个selling_points.json
- [ ] 3个africa.txt市场版本
- [ ] 累计：11个产品有内容

---

# P2-D5：第2批续-详情页+RFQ+WhatsApp

## 今日目标

- 完成第2批剩余内容
- 开始尝试用脚本辅助生成

## 主任务

### 任务1：批量生成详情页（5个产品）

* 内容：调用alibaba_detail_prompt
* 输出：5个alibaba_detail.md
* 耗时：90分钟

### 任务2：批量生成RFQ+WhatsApp（5个产品）

* 内容：调用rfq_reply_prompt和whatsapp_script_prompt
* 输出：5个rfq文件 + 5个whatsapp文件
* 耗时：60分钟

### 任务3：尝试写一个Python辅助脚本

* 内容：写一个简单的Python脚本，自动从Excel读取产品参数并格式化prompt输入
* 步骤：
  1. 用pandas读取product_database_filled.xlsx
  2. 提取指定产品的参数
  3. 格式化为prompt所需的输入格式
  4. 输出到 03-workflows/batch_processing/prompt_input_helper.py
* 输出：prompt_input_helper.py
* 耗时：45分钟

## 辅助学习任务

* 学习pandas的iloc和loc用法，用于精确提取产品数据
* 耗时：20分钟

## 英语口语任务

* 模拟电话沟通：用英语回复一个欧洲客户的询价
* 场景：客户问MOQ、lead time、付款方式
* 耗时：15分钟

## 今日验收标准

- [ ] 5个alibaba_detail.md
- [ ] 5个rfq文件
- [ ] 5个whatsapp文件
- [ ] prompt_input_helper.py脚本
- [ ] 累计：16个产品有内容

---

# P2-D6：第3批-切割工具类（5个产品-全量）

## 今日目标

- 第3批：5个切割工具类产品，尝试一天完成全量生成
- 检验熟练度提升

## 主任务

### 任务1：筛选+全量生成（5个切割工具产品）

* 内容：5个产品的SEO+卖点+详情页+RFQ+WhatsApp
* 步骤：按D1-D5的节奏，一天内完成全部5类内容
* 输出：5个产品×5类内容=25个文件
* 耗时：180分钟

### 任务2：创建产品内容质量评分表

* 内容：对已生成的16个产品的内容质量打分（1-5分）
* 步骤：
  1. 创建 07-docs/testing_reports/content_quality_scores.csv
  2. 列：product_code, seo_score, selling_points_score, detail_page_score, rfq_score, whatsapp_score, notes
  3. 对每个产品的每类内容打分并备注
* 输出：content_quality_scores.csv
* 耗时：30分钟

## 辅助学习任务

* 分析质量评分表，找出得分最低的prompt，确定优化优先级
* 耗时：20分钟

## 英语口语任务

* 用英语描述3个不同品类工具的应用场景差异
* 重点：weeding vs digging vs cutting的使用场景区别
* 耗时：15分钟

## 今日验收标准

- [ ] 5个切割工具产品的完整内容包
- [ ] content_quality_scores.csv
- [ ] 累计：21个产品有内容
- [ ] Week 2成果可见

---

# P2-D7：Week 2总结 + Prompt优化日

## 今日目标

- 回顾前6天产出，优化得分最低的2个prompt
- 不生成新内容，只优化系统

## 主任务

### 任务1：内容质量回顾

* 内容：分析content_quality_scores.csv，找出得分<3的prompt
* 步骤：
  1. 统计每个prompt的平均分
  2. 找出得分最低的2个
  3. 分析原因（prompt太长？信息不足？格式问题？）
* 输出：07-docs/project_notes/prompt_audit_report.md
* 耗时：45分钟

### 任务2：优化低分Prompt

* 内容：修改得分最低的2个prompt文件
* 步骤：
  1. 打开对应prompt文件
  2. 根据问题调整结构（更清晰的指令、更好的示例、更明确的输出格式）
  3. 用GS-001测试新prompt
  4. 对比新旧输出质量
* 输出：更新后的prompt文件 + 对比结果
* 耗时：90分钟

### 任务3：更新工作流SOP

* 内容：根据6天的实操经验，更新single_product_workflow.md
* 步骤：补充踩过的坑、优化后的步骤、注意事项
* 输出：更新后的single_product_workflow.md
* 耗时：45分钟

### 任务4：Git提交 + Week 2总结

* 内容：提交所有改动，写周总结
* 输出：Git提交 + week2_summary.md
* 耗时：30分钟

## 辅助学习任务

* 阅读优化后的prompt，思考：什么样的prompt指令最有效？
* 耗时：20分钟

## 英语口语任务

* 自由话题：用英语描述你这一周的工作内容和成果
* 当作周汇报来练习
* 耗时：15分钟

## 今日验收标准

- [ ] prompt_audit_report.md
- [ ] 2个prompt已优化
- [ ] single_product_workflow.md已更新
- [ ] week2_summary.md
- [ ] Git提交完成

## 今日复盘问题

1. 优化后的prompt生成质量有明显提升吗？
2. 目前最耗时的步骤是什么？
3. Week 3要开始自动化建设，准备好了吗？

---

# P2-D8：自动化基础-Python批量读取+格式化

## 今日目标

- 完善Python脚本：能批量读取Excel产品并格式化prompt输入
- 测试脚本的准确性

## 主任务

### 任务1：编写产品读取脚本

* 内容：写 03-workflows/batch_processing/batch_reader.py
* 步骤：
  1. 用pandas读取product_database_filled.xlsx
  2. 支持按category筛选
  3. 支持按product_code列表读取
  4. 输出格式：JSON或Markdown，可直接喂给prompt
  5. 支持只读取AI字段为pending的产品
* 输出：batch_reader.py
* 耗时：90分钟

### 任务2：测试脚本

* 内容：用batch_reader.py读取之前生成过内容的3个产品，验证数据准确性
* 步骤：
  1. 运行脚本读取GF-001, GS-001, GR-001
  2. 对比脚本输出与Excel原始数据
  3. 修复任何数据不一致
* 输出：测试报告 07-docs/testing_reports/batch_reader_test.md
* 耗时：45分钟

### 任务3：编写输出整理脚本

* 内容：写 03-workflows/batch_processing/output_organizer.py
* 步骤：
  1. 接收AI生成的内容
  2. 自动创建产品文件夹
  3. 按类型写入对应文件
  4. 支持批量处理
* 输出：output_organizer.py
* 耗时：60分钟

## 辅助学习任务

* 学习Python的os.path和pathlib模块，理解文件路径操作
* 耗时：20分钟

## 英语口语任务

* 用英语解释batch_reader.py的功能和工作流程
* 假装在给同事做code review
* 耗时：15分钟

## 今日验收标准

- [ ] batch_reader.py可运行
- [ ] 测试通过，数据准确
- [ ] output_organizer.py可运行
- [ ] 自动化基础脚本完成

---

# P2-D9：自动化进阶-Prompt模板引擎

## 今日目标

- 编写Prompt模板引擎：自动将产品数据填入prompt
- 减少手动复制粘贴

## 主任务

### 任务1：编写Prompt模板引擎

* 内容：写 03-workflows/batch_processing/prompt_engine.py
* 步骤：
  1. 读取02-prompts/下的prompt模板
  2. 用{product_name}、{material}等占位符替换硬编码内容
  3. 从batch_reader.py获取产品数据
  4. 填入prompt并输出完整prompt文本
* 输出：prompt_engine.py
* 耗时：90分钟

### 任务2：转换现有prompt为模板格式

* 内容：将seo_title_prompt.md和selling_points_prompt.md改为模板格式
* 步骤：
  1. 将硬编码的产品示例替换为{product_name}等占位符
  2. 保留示例结构但去除具体产品数据
  3. 保存为 02-prompts/seo/seo_title_template.md
* 输出：2个模板文件
* 耗时：45分钟

### 任务3：端到端测试

* 内容：用新脚本+新模板为1个新产品生成SEO标题
* 步骤：batch_reader → prompt_engine → AI调用 → output_organizer
* 输出：1个产品的完整SEO标题文件
* 耗时：45分钟

## 辅助学习任务

* 学习Python的string.Template或f-string模板机制
* 耗时：20分钟

## 英语口语任务

* 练习：用英语描述"template engine"的概念和工作原理
* 关键词：placeholder, substitution, input, output, pipeline
* 耗时：15分钟

## 今日验收标准

- [ ] prompt_engine.py可运行
- [ ] 2个prompt已转为模板格式
- [ ] 端到端测试通过
- [ ] 自动化管道雏形完成

---

# P2-D10：第4批-用自动化脚本批量生成

## 今日目标

- 用D8-D9写的脚本，批量生成5个产品的SEO+卖点
- 验证自动化流程

## 主任务

### 任务1：用脚本批量生成SEO标题（5个产品）

* 内容：选5个新产品的编码，用自动化脚本生成
* 步骤：
  1. 运行batch_reader读取5个产品
  2. 运行prompt_engine生成prompt
  3. 调用AI
  4. 运行output_organizer保存
* 输出：5个seo_titles.json
* 耗时：60分钟

### 任务2：用脚本批量生成卖点（5个产品）

* 内容：同上流程，生成卖点
* 输出：5个selling_points.json
* 耗时：60分钟

### 任务3：记录自动化流程的问题和bug

* 内容：记录脚本运行中的任何问题
* 输出：07-docs/testing_reports/automation_bug_log.md
* 耗时：20分钟

### 任务4：修复发现的bug

* 内容：修复bug_log中的问题
* 输出：修复后的脚本
* 耗时：40分钟

## 辅助学习任务

* 对比手动生成和脚本生成的耗时差异，计算效率提升
* 耗时：15分钟

## 英语口语任务

* 用英语写一段"自动化流程说明"文档开头
* 目标：能用英语写技术文档
* 耗时：15分钟

## 今日验收标准

- [ ] 5个seo_titles.json（通过脚本生成）
- [ ] 5个selling_points.json（通过脚本生成）
- [ ] automation_bug_log.md
- [ ] Bug已修复
- [ ] 累计：26个产品有内容

---

# P2-D11：国家市场数据库-非洲市场报告

## 今日目标

- 为非洲市场编写第一份详细的市场分析报告
- 追加到market_knowledge.md

## 主任务

### 任务1：收集非洲农具市场数据

* 内容：调研非洲主要农业国家的农具市场需求
* 步骤：
  1. 确定3-5个重点非洲国家（如尼日利亚、肯尼亚、埃塞俄比亚）
  2. 收集：农业规模、主要作物、工具偏好、价格敏感度、进口政策
  3. 记录关键数据点
* 输出：数据笔记
* 耗时：60分钟

### 任务2：撰写非洲市场报告

* 内容：将数据整理为结构化报告
* 步骤：
  1. 按国家分段
  2. 包含：市场规模、需求品类、价格区间、竞争对手、进入策略
  3. 追加到 04-database/output/market_knowledge.md
* 输出：更新后的market_knowledge.md
* 耗时：60分钟

### 任务3：同步更新CSV

* 内容：将市场关键数据写入CSV格式
* 输出：04-database/csv/market_africa_summary.csv
* 耗时：30分钟

## 辅助学习任务

* 学习如何从市场数据中提取"可行动洞察"（actionable insights）
* 耗时：20分钟

## 英语口语任务

* 用英语介绍非洲农具市场的3个关键发现
* 关键词：market size, import duty, distribution channel, end user
* 耗时：15分钟

## 今日验收标准

- [ ] 非洲市场报告已追加到market_knowledge.md
- [ ] market_africa_summary.csv已创建
- [ ] 至少3个非洲国家的详细数据

---

# P2-D12：国家市场数据库-欧洲市场报告

## 今日目标

- 编写欧洲市场报告
- 对比非洲和欧洲市场差异

## 主任务

### 任务1：收集欧洲农具市场数据

* 内容：调研欧洲主要国家的农具市场需求
* 步骤：关注欧盟标准、CE认证、环保要求、品牌偏好
* 输出：数据笔记
* 耗时：60分钟

### 任务2：撰写欧洲市场报告

* 内容：结构化报告追加到market_knowledge.md
* 步骤：包含认证要求、质量标准、主流品牌、价格区间
* 输出：更新后的market_knowledge.md
* 耗时：60分钟

### 任务3：对比分析

* 内容：写一份非洲vs欧洲市场的对比分析
* 输出：04-database/output/africa_vs_europe_comparison.md
* 耗时：30分钟

## 辅助学习任务

* 了解CE认证和GS认证对外贸工具出口的具体要求
* 耗时：20分钟

## 英语口语任务

* 练习：用英语向客户解释为什么你的产品符合欧洲标准
* 关键词：CE marking, compliance, quality assurance, testing standards
* 耗时：15分钟

## 今日验收标准

- [ ] 欧洲市场报告已追加
- [ ] africa_vs_europe_comparison.md已创建
- [ ] 累计：2个国家市场报告

---

# P2-D13：国家市场数据库-北美市场报告 + Cron入门

## 今日目标

- 编写北美市场报告
- 学习设置Cron定时任务

## 主任务

### 任务1：收集并撰写北美市场报告

* 内容：美国/加拿大市场，关注DIY文化、Home Depot/Lowe's渠道、UL认证
* 输出：更新market_knowledge.md + market_north_america_summary.csv
* 耗时：90分钟

### 任务2：设置第一个Cron任务-每日提醒

* 内容：用Hermes的cronjob功能设置一个每日执行提醒
* 步骤：
  1. 创建cron任务：每天早上9点提醒今日任务
  2. 任务内容：读取当天的phase2_plan.md对应天数
  3. 输出到当前对话
* 输出：Cron任务已创建
* 耗时：30分钟

### 任务3：三市场对比总结

* 内容：写非洲vs欧洲vs北美的三市场对比
* 输出：04-database/output/three_market_comparison.md
* 耗时：30分钟

## 辅助学习任务

* 理解Cron表达式语法（分 时 日 月 星期）
* 耗时：15分钟

## 英语口语任务

* 用英语描述北美市场和中国供应商的合作模式
* 关键词：OEM, private label, distributor, retail chain
* 耗时：15分钟

## 今日验收标准

- [ ] 北美市场报告已追加
- [ ] Cron每日提醒任务已设置
- [ ] three_market_comparison.md已创建
- [ ] Week 3成果可见

---

# P2-D14：Week 3总结 + 市场本地化内容批量生成

## 今日目标

- 用3个市场报告，为已生成内容的产品创建市场本地化版本
- 周总结

## 主任务

### 任务1：市场本地化-为5个产品生成非洲版本

* 内容：用market_localization_prompt+非洲市场数据，生成5个产品的非洲市场版本
* 输出：5个产品的market_versions/africa.txt（实质内容，>500字节）
* 耗时：90分钟

### 任务2：市场本地化-为5个产品生成欧洲版本

* 内容：同上，生成欧洲市场版本
* 输出：5个产品的market_versions/europe.txt
* 耗时：90分钟

### 任务3：Week 3总结

* 内容：总结本周成果，更新进度追踪
* 输出：07-docs/SOP/daily_tasks/week3_summary.md
* 耗时：30分钟

## 辅助学习任务

* 回顾market_localization_prompt的效果，思考如何改进
* 耗时：15分钟

## 英语口语任务

* 用英语写一段针对非洲客户的产品推荐邮件
* 场景：推荐garden hoe给尼日利亚的农业经销商
* 耗时：15分钟

## 今日验收标准

- [ ] 5个africa.txt市场版本
- [ ] 5个europe.txt市场版本
- [ ] week3_summary.md
- [ ] 累计：26个产品有内容，其中10个有市场本地化版本

---

# P2-D15：自动化管道-半自动批量生成脚本

## 今日目标

- 编写一个半自动脚本：读取产品列表→生成prompt→调用AI→保存输出
- 目标：5个产品一键生成SEO+卖点

## 主任务

### 任务1：编写半自动生成脚本

* 内容：写 03-workflows/batch_processing/semi_auto_generator.py
* 步骤：
  1. 读取产品编码列表（从txt文件）
  2. 调用batch_reader获取产品数据
  3. 调用prompt_engine生成prompt
  4. 输出prompt到终端（供AI调用）
  5. 接收AI输出
  6. 调用output_organizer保存
* 输出：semi_auto_generator.py
* 耗时：120分钟

### 任务2：测试脚本-生成3个产品的SEO标题

* 内容：用脚本测试3个产品
* 输出：3个seo_titles.json
* 耗时：45分钟

### 任务3：记录脚本使用说明

* 内容：写脚本的README
* 输出：03-workflows/batch_processing/README.md
* 耗时：30分钟

## 辅助学习任务

* 学习Python的subprocess模块，理解如何调用外部命令
* 耗时：20分钟

## 英语口语任务

* 用英语解释semi_auto_generator.py的工作流程
* 练习技术演讲能力
* 耗时：15分钟

## 今日验收标准

- [ ] semi_auto_generator.py可运行
- [ ] 3个产品测试通过
- [ ] README.md已创建
- [ ] 自动化程度提升

---

# P2-D16：批量生成-第5批（5个产品-用半自动脚本）

## 今日目标

- 用D15的脚本批量生成5个产品的SEO+卖点+详情页

## 主任务

### 任务1：用脚本批量生成SEO+卖点（5个产品）

* 内容：运行semi_auto_generator.py
* 输出：5个seo_titles.json + 5个selling_points.json
* 耗时：90分钟

### 任务2：用脚本批量生成详情页（5个产品）

* 内容：同上流程，生成详情页
* 输出：5个alibaba_detail.md
* 耗时：90分钟

### 任务3：补充RFQ+WhatsApp（5个产品）

* 内容：手动或脚本生成
* 输出：5个rfq文件 + 5个whatsapp文件
* 耗时：60分钟

## 辅助学习任务

* 评估脚本的效率提升：对比D2（手动）和D16（半自动）的耗时
* 耗时：15分钟

## 英语口语任务

* 模拟：用英语回复一封RFQ询价邮件
* 场景：英国客户询问garden fork的批量报价
* 耗时：15分钟

## 今日验收标准

- [ ] 5个产品的SEO标题
- [ ] 5个产品的卖点
- [ ] 5个产品的详情页
- [ ] 5个产品的RFQ+WhatsApp
- [ ] 累计：31个产品有内容

---

# P2-D17：批量生成-第6批（5个产品）

## 今日目标

- 继续用脚本批量生成5个产品
- 开始关注内容一致性

## 主任务

### 任务1：批量生成5个产品的全量内容

* 内容：SEO+卖点+详情页+RFQ+WhatsApp
* 输出：5个产品×5类内容=25个文件
* 耗时：180分钟

### 任务2：内容一致性检查

* 内容：检查不同产品的SEO标题是否有过度重复的模式
* 步骤：
  1. 读取所有已生成的seo_titles.json
  2. 分析标题结构的多样性
  3. 记录发现的问题
* 输出：07-docs/testing_reports/seo_diversity_check.md
* 耗时：30分钟

## 辅助学习任务

* 学习SEO标题的多样化策略（长尾关键词、场景描述、规格突出等）
* 耗时：20分钟

## 英语口语任务

* 用英语描述你的产品相比竞争对手的3个差异化优势
* 练习"差异化定位"的英语表达
* 耗时：15分钟

## 今日验收标准

- [ ] 5个产品全量内容
- [ ] seo_diversity_check.md
- [ ] 累计：36个产品有内容

---

# P2-D18：批量生成-第7批（5个产品）+ SEO汇总优化

## 今日目标

- 继续批量生成
- 优化SEO标题汇总CSV

## 主任务

### 任务1：批量生成5个产品全量内容

* 输出：5个产品×5类内容
* 耗时：180分钟

### 任务2：优化SEO汇总CSV

* 内容：更新05-output/export_files/seo_titles.csv，包含所有已生成产品的SEO标题
* 步骤：
  1. 读取所有seo_titles.json
  2. 合并为统一的CSV
  3. 列：product_code, product_name, category, seo_v1, seo_v2, seo_v3
* 输出：更新后的seo_titles.csv
* 耗时：30分钟

### 任务3：优化卖点汇总CSV

* 内容：同上，更新selling_points.csv
* 输出：更新后的selling_points.csv
* 耗时：20分钟

## 辅助学习任务

* 分析SEO汇总CSV，找出出现频率最高的关键词
* 耗时：15分钟

## 英语口语任务

* 用英语做一个2分钟的产品推介（elevator pitch）
* 场景：在展会上向路过的买家介绍你的产品
* 耗时：15分钟

## 今日验收标准

- [ ] 5个产品全量内容
- [ ] seo_titles.csv已更新（包含所有产品）
- [ ] selling_points.csv已更新
- [ ] 累计：41个产品有内容

---

# P2-D19：内容质量审查 + Prompt微调

## 今日目标

- 审查已生成的41个产品的质量
- 针对性优化prompt

## 主任务

### 任务1：随机抽样审查

* 内容：随机抽取10个产品，审查每类内容的质量
* 步骤：
  1. 更新content_quality_scores.csv（新增评分）
  2. 计算每个prompt类别的平均分
  3. 找出持续低分的prompt
* 输出：更新的content_quality_scores.csv
* 耗时：60分钟

### 任务2：优化低分Prompt

* 内容：修改得分最低的1-2个prompt
* 步骤：调整指令、增加示例、优化输出格式要求
* 输出：更新后的prompt文件
* 耗时：60分钟

### 任务3：用新prompt重新生成3个产品

* 内容：选3个之前得分低的产品，用新prompt重新生成
* 输出：3个产品的更新内容
* 耗时：60分钟

## 辅助学习任务

* 总结prompt优化的规律：什么样的修改最有效？
* 耗时：15分钟

## 英语口语任务

* 用英语描述prompt优化的过程和结果
* 练习技术写作的英语表达
* 耗时：15分钟

## 今日验收标准

- [ ] content_quality_scores.csv已更新
- [ ] 1-2个prompt已优化
- [ ] 3个产品内容已重新生成
- [ ] 质量提升有数据支撑

---

# P2-D20：自动化管道-Cron定时任务设置

## 今日目标

- 设置Cron定时任务，实现每日自动批量生成
- 目标：每天自动生成5个产品的SEO标题

## 主任务

### 任务1：设置Cron批量生成任务

* 内容：用Hermes的cronjob创建每日定时任务
* 步骤：
  1. 创建cron任务：每天运行一次
  2. 任务内容：读取5个pending产品→生成SEO标题→保存
  3. 设置输出交付
* 输出：Cron任务已创建并测试
* 耗时：90分钟

### 任务2：测试Cron任务

* 内容：手动触发一次Cron任务，验证端到端流程
* 步骤：cronjob action='run' → 检查输出
* 输出：测试结果记录
* 耗时：30分钟

### 任务3：设置第二个Cron任务-每日市场数据更新提醒

* 内容：每天提醒收集市场数据
* 输出：Cron任务已创建
* 耗时：20分钟

## 辅助学习任务

* 理解Cron任务的限制和最佳实践
* 耗时：15分钟

## 英语口语任务

* 用英语写一段Cron任务的配置说明
* 练习技术文档英语写作
* 耗时：15分钟

## 今日验收标准

- [ ] 每日自动生成Cron任务已设置
- [ ] 手动触发测试通过
- [ ] 市场数据提醒Cron已设置
- [ ] Week 4自动化成果可见

---

# P2-D21：第8批-用Cron自动生成

## 今日目标

- 让Cron任务自动生成5个产品的内容
- 人工只做审核和修复

## 主任务

### 任务1：触发Cron自动生成任务

* 内容：手动触发Cron任务，生成5个产品的SEO+卖点
* 输出：5个产品的seo_titles.json + selling_points.json
* 耗时：30分钟（主要是等待）

### 任务2：审核Cron生成结果

* 内容：检查生成质量，修复问题
* 输出：质量审核记录
* 耗时：60分钟

### 任务3：手动生成详情页+RFQ+WhatsApp（5个产品）

* 内容：Cron暂时只生成SEO+卖点，其余手动
* 输出：5个alibaba_detail.md + 5个rfq + 5个whatsapp
* 耗时：120分钟

## 辅助学习任务

* 评估Cron生成 vs 手动生成的质量差异
* 耗时：15分钟

## 英语口语任务

* 自由练习：选一个话题用英语描述1分钟
* 话题：你的项目进展 / 农具产品 / AI自动化
* 耗时：15分钟

## 今日验收标准

- [ ] Cron任务成功运行
- [ ] 5个产品SEO+卖点已生成
- [ ] 5个产品详情页+RFQ+WhatsApp已完成
- [ ] 累计：46个产品有内容

---

# P2-D22：RFQ批量优化

## 今日目标

- 优化RFQ回复prompt，提升回复质量
- 批量生成10个产品的RFQ回复

## 主任务

### 任务1：分析现有RFQ回复质量

* 内容：检查已生成的RFQ回复，找出共性问题
* 输出：rfq_quality_analysis.md
* 耗时：45分钟

### 任务2：优化RFQ Prompt

* 内容：根据分析结果优化rfq_reply_prompt.md
* 步骤：增加场景分类（首次询价、追问、议价）、增加回复模板、优化语气
* 输出：更新后的rfq_reply_prompt.md
* 耗时：60分钟

### 任务3：批量生成RFQ回复（10个产品）

* 内容：用新prompt批量生成10个产品的RFQ回复
* 输出：10个rfq文件
* 耗时：60分钟

## 辅助学习任务

* 学习B2B RFQ回复的最佳实践
* 耗时：15分钟

## 英语口语任务

* 模拟：用英语处理客户的议价请求
* 场景：客户说"your price is too high, can you give 10% discount?"
* 耗时：15分钟

## 今日验收标准

- [ ] rfq_quality_analysis.md
- [ ] rfq_reply_prompt.md已优化
- [ ] 10个RFQ回复已生成
- [ ] RFQ质量有提升

---

# P2-D23：WhatsApp话术批量优化

## 今日目标

- 优化WhatsApp话术prompt
- 批量生成10个产品的WhatsApp话术

## 主任务

### 任务1：分析现有WhatsApp话术质量

* 内容：检查已生成的话术
* 输出：whatsapp_quality_analysis.md
* 耗时：30分钟

### 任务2：优化WhatsApp Prompt

* 内容：优化whatsapp_script_prompt.md
* 步骤：增加场景（首次联系、产品推荐、跟进、节日问候）、优化语气（友好但专业）
* 输出：更新后的whatsapp_script_prompt.md
* 耗时：60分钟

### 任务3：批量生成WhatsApp话术（10个产品）

* 输出：10个whatsapp文件
* 耗时：60分钟

### 任务4：创建WhatsApp话术场景模板

* 内容：将不同场景的话术整理为可复用模板
* 输出：02-prompts/whatsapp/script_templates.md
* 耗时：30分钟

## 辅助学习任务

* 学习WhatsApp Business营销的最佳实践
* 耗时：15分钟

## 英语口语任务

* 用英语写3条不同场景的WhatsApp消息：
  1. 首次联系（cold outreach）
  2. 产品跟进（follow-up）
  3. 节日问候（relationship building）
* 耗时：20分钟

## 今日验收标准

- [ ] whatsapp_quality_analysis.md
- [ ] whatsapp_script_prompt.md已优化
- [ ] 10个WhatsApp话术已生成
- [ ] script_templates.md已创建

---

# P2-D24：国家市场数据库-南美市场报告

## 今日目标

- 编写南美市场报告
- 更新market_knowledge.md

## 主任务

### 任务1：收集南美农具市场数据

* 内容：巴西、阿根廷、智利等国家的市场数据
* 关注点：农业规模、进口关税、语言（西语/葡语）、分销渠道
* 输出：数据笔记
* 耗时：60分钟

### 任务2：撰写南美市场报告

* 内容：追加到market_knowledge.md
* 输出：更新后的market_knowledge.md + market_south_america_summary.csv
* 耗时：60分钟

### 任务3：四市场对比总结

* 内容：非洲+欧洲+北美+南美的综合对比
* 输出：04-database/output/four_market_comparison.md
* 耗时：30分钟

## 辅助学习任务

* 了解南美国家的进口认证要求（如巴西INMETRO）
* 耗时：15分钟

## 英语口语任务

* 用英语介绍南美市场的特点和进入策略
* 关键词：import tariff, certification, distribution, language barrier
* 耗时：15分钟

## 今日验收标准

- [ ] 南美市场报告已追加
- [ ] four_market_comparison.md已创建
- [ ] 累计：4个国家市场报告

---

# P2-D25：SEO批量优化 + 关键词分析

## 今日目标

- 基于已生成的SEO标题，分析关键词分布
- 优化SEO策略

## 主任务

### 任务1：关键词频率分析

* 内容：写一个Python脚本分析所有SEO标题中的关键词频率
* 步骤：
  1. 读取所有seo_titles.json
  2. 提取关键词（去除停用词）
  3. 统计频率，输出top 30关键词
* 输出：05-output/export_files/keyword_frequency_analysis.csv
* 耗时：60分钟

### 任务2：长尾关键词挖掘

* 内容：分析现有标题的长尾关键词覆盖度
* 步骤：检查是否包含场景词、规格词、认证词等
* 输出：07-docs/project_notes/longtail_keyword_gap.md
* 耗时：45分钟

### 任务3：优化SEO Prompt

* 内容：根据分析结果优化seo_title_prompt.md
* 步骤：增加长尾关键词要求、场景多样性要求
* 输出：更新后的seo_title_prompt.md
* 耗时：45分钟

### 任务4：重新生成5个产品的SEO标题

* 内容：用优化后的prompt重新生成
* 输出：5个更新的seo_titles.json
* 耗时：45分钟

## 辅助学习任务

* 学习SEO长尾关键词策略
* 耗时：15分钟

## 英语口语任务

* 用英语描述你的SEO关键词策略
* 练习市场营销英语
* 耗时：15分钟

## 今日验收标准

- [ ] keyword_frequency_analysis.csv
- [ ] longtail_keyword_gap.md
- [ ] seo_title_prompt.md已优化
- [ ] 5个产品SEO标题已更新

---

# P2-D26：作品集整理-GitHub仓库准备

## 今日目标

- 整理GitHub仓库，准备作为求职作品集
- 更新README

## 主任务

### 任务1：清理项目目录

* 内容：删除临时文件、归档旧文件、整理目录
* 步骤：
  1. 删除01-产品数据库模板/（旧版遗留）
  2. 确认archive/下的文件都是正确的旧文件
  3. 检查所有目录是否整洁
* 输出：整洁的项目目录
* 耗时：45分钟

### 任务2：更新GitHub README

* 内容：写一个专业的README.md，展示项目价值
* 步骤：
  1. 项目简介（1段）
  2. 核心功能（ bullet list）
  3. 项目结构
  4. 已生成的内容统计
  5. 技术栈
  6. 如何使用
* 输出：更新后的08-git/README.md
* 耗时：60分钟

### 任务3：创建项目成果统计

* 内容：统计项目的量化成果
* 步骤：
  1. 产品数据库：215个产品
  2. 已生成内容：XX个产品×5类内容=XX个文件
  3. Prompt模板：6个
  4. 自动化脚本：X个
  5. 市场报告：4个国家
  6. 代码行数：Python脚本X行
* 输出：07-docs/project_notes/project_achievements.md
* 耗时：30分钟

## 辅助学习任务

* 学习如何写一个吸引招聘者的GitHub README
* 耗时：15分钟

## 英语口语任务

* 用英语写一段项目的"电梯演讲"（30秒介绍）
* 用于面试时快速介绍项目
* 耗时：15分钟

## 今日验收标准

- [ ] 项目目录已清理
- [ ] README.md已更新（专业、有吸引力）
- [ ] project_achievements.md已创建
- [ ] GitHub仓库可对外展示

---

# P2-D27：简历更新 + 项目描述优化

## 今日目标

- 用项目成果更新简历
- 优化项目描述的英语表达

## 主任务

### 任务1：用英语写项目描述

* 内容：为简历写一段专业的项目描述（英文版）
* 步骤：
  1. 项目名称
  2. 你的角色
  3. 技术栈
  4. 核心成果（量化）
  5. 关键贡献
* 输出：resume_project_description_en.md
* 耗时：60分钟

### 任务2：用中文写项目描述

* 内容：同上，中文版
* 输出：resume_project_description_cn.md
* 耗时：30分钟

### 任务3：准备10个技术面试问答

* 内容：针对这个项目，准备10个可能被问到的技术问题及答案
* 步骤：
  1. 列出可能的技术问题
  2. 用中英文各写一份答案
  3. 保存到 07-docs/SOP/interview_qa.md
* 输出：interview_qa.md（10个问答）
* 耗时：60分钟

## 辅助学习任务

* 学习STAR法则（Situation, Task, Action, Result）写项目经历
* 耗时：15分钟

## 英语口语任务

* 用STAR法则口头描述这个项目（录音）
* 限时3分钟
* 耗时：20分钟

## 今日验收标准

- [ ] resume_project_description_en.md
- [ ] resume_project_description_cn.md
- [ ] interview_qa.md（10个问答）
- [ ] STAR法则练习完成

---

# P2-D28：自动化管道扩展-Cron全量生成

## 今日目标

- 扩展Cron任务，实现全量内容自动生成
- 测试端到端自动化

## 主任务

### 任务1：扩展Cron任务为全量生成

* 内容：修改Cron任务，使其能生成SEO+卖点+详情页+RFQ+WhatsApp
* 步骤：更新Cron任务的prompt或脚本
* 输出：更新后的Cron任务配置
* 耗时：60分钟

### 任务2：端到端测试

* 内容：手动触发Cron，生成2个产品的全量内容
* 步骤：触发→等待→检查输出质量
* 输出：2个产品的完整内容包
* 耗时：60分钟

### 任务3：编写自动化使用手册

* 内容：写一份Cron自动化系统的使用手册
* 输出：03-workflows/automation/cron_user_guide.md
* 耗时：45分钟

## 辅助学习任务

* 评估自动化系统的稳定性
* 耗时：15分钟

## 英语口语任务

* 用英语解释你的自动化系统如何工作
* 练习：假装在给技术面试官讲解
* 耗时：15分钟

## 今日验收标准

- [ ] Cron全量生成任务已配置
- [ ] 端到端测试通过
- [ ] cron_user_guide.md已创建
- [ ] 自动化管道完整可用

---

# P2-D29：最终内容冲刺-补全剩余产品

## 今日目标

- 用自动化管道，尽可能多地生成剩余产品的内容
- 目标：累计达到50个产品有内容

## 主任务

### 任务1：批量生成剩余产品（目标14个产品）

* 内容：用Cron或半自动脚本批量生成
* 优先级：SEO+卖点（核心）→详情页→RFQ+WhatsApp
* 输出：尽可能多的产品内容文件
* 耗时：180分钟

### 任务2：最终质量检查

* 内容：随机抽查10个产品，确保质量达标
* 输出：final_quality_check.md
* 耗时：30分钟

### 任务3：更新项目统计

* 内容：更新project_achievements.md
* 输出：最新的统计数据
* 耗时：15分钟

## 辅助学习任务

* 回顾整个Phase 2，总结最大的收获
* 耗时：15分钟

## 英语口语任务

* 用英语做一个5分钟的项目展示
* 涵盖：项目背景、技术实现、成果数据、个人成长
* 耗时：20分钟

## 今日验收标准

- [ ] 累计50+个产品有内容（或尽可能多）
- [ ] final_quality_check.md
- [ ] project_achievements.md已更新

---

# P2-D30：Phase 2总结 + Phase 3规划

## 今日目标

- 总结Phase 2全部成果
- 制定Phase 3计划

## 主任务

### 任务1：Phase 2成果总结

* 内容：写一份完整的Phase 2总结报告
* 包括：
  1. 目标达成情况
  2. 量化数据（产品数、内容数、代码行数等）
  3. 技术成长
  4. 英语提升
  5. 遇到的问题和解决方案
  6. 下一步计划
* 输出：07-docs/SOP/daily_tasks/phase2_summary.md
* 耗时：90分钟

### 任务2：GitHub最终提交

* 内容：将所有Phase 2的成果提交到GitHub
* 步骤：git add → git commit → git push
* 输出：Git提交记录
* 耗时：15分钟

### 任务3：Phase 3规划

* 内容：制定Phase 3的计划（独立站建设、邮件营销自动化、数据分析看板等）
* 输出：phase3_plan.md（大纲即可，详细计划后续展开）
* 耗时：45分钟

### 任务4：写一封给自己的信

* 内容：记录这30天的变化和成长
* 输出：personal_reflection.md
* 耗时：30分钟

## 辅助学习任务

* 回顾Phase 2的所有复盘记录，提取通用经验
* 耗时：20分钟

## 英语口语任务

* 用英语写一段Phase 2的总结（300词）
* 当作项目复盘报告来练习
* 耗时：20分钟

## 今日验收标准

- [ ] phase2_summary.md
- [ ] GitHub已提交
- [ ] phase3_plan.md（大纲）
- [ ] personal_reflection.md
- [ ] Phase 2完成！

---

## Phase 2 量化目标汇总

| 指标        | 起点      | Phase 2结束目标 |
| --------- | ------- | ----------- |
| 有内容的产品数   | 5       | 50+         |
| Prompt模板数 | 6       | 8+（含优化版）    |
| 自动化脚本数    | 0       | 4+          |
| Cron定时任务  | 0       | 2+          |
| 国家市场报告    | 1个（不完整） | 4个完整        |
| 汇总CSV文件   | 2个      | 5+          |
| GitHub提交  | 1次      | 15+次        |
| 英语练习次数    | 0（记录）   | 30次         |
| 项目文档      | 基础      | 完整SOP+QA+总结 |

---

## 执行纪律

1. **每天打开phase2_plan.md，找到当天的任务**
2. **按顺序执行，不跳天**
3. **完成后在对应任务打✓**
4. **复盘问题必须回答（哪怕简短）**
5. **英语口语任务必须做（打字也算）**
6. **遇到卡点，记录问题，继续下一个任务，不纠结**
7. **每天结束前5分钟，更新进度**

---

*Phase 2的核心不是"学更多"，而是"产出更多"。
每天3-5小时，30天后你会看到完全不同的项目状态。*
