# Phase 2 启动审计检查报告

> 执行日期：____
> 执行人：____

---

## 一、数据库检查

### 1.1 Excel数据库

- [ ] `04-database/excel/product_database_filled.xlsx` 可正常打开
- [ ] 数据行数：____（目标：215行）
- [ ] 列数：____（目标：31列）
- [ ] 是否存在乱码或空行：是 / 否
- [ ] AI字段（第21-31列）为pending的产品数：____

**问题记录：**


---

### 1.2 CSV数据库

- [ ] `04-database/csv/product_database_filled.csv` 存在且可读
- [ ] 与Excel数据一致：是 / 否

---

## 二、Prompt文件检查

### 2.1 文件存在性

| Prompt文件 | 存在 | 可读 | 大小(KB) | 备注 |
|-----------|------|------|----------|------|
| 02-prompts/seo/seo_title_prompt.md | ☐ | ☐ | | |
| 02-prompts/detail_page/selling_points_prompt.md | ☐ | ☐ | | |
| 02-prompts/detail_page/alibaba_detail_prompt.md | ☐ | ☐ | | |
| 02-prompts/rfq/rfq_reply_prompt.md | ☐ | ☐ | | |
| 02-prompts/whatsapp/whatsapp_script_prompt.md | ☐ | ☐ | | |
| 02-prompts/batch_workflow/market_localization_prompt.md | ☐ | ☐ | | |
| 02-prompts/prompt_index.md | ☐ | ☐ | | |

### 2.2 Prompt质量快速评估

| Prompt | 结构清晰度(1-5) | 示例充分性(1-5) | 输出格式明确(1-5) | 备注 |
|--------|-----------------|-----------------|-------------------|------|
| seo_title | | | | |
| selling_points | | | | |
| alibaba_detail | | | | |
| rfq_reply | | | | |
| whatsapp_script | | | | |
| market_localization | | | | |

**问题记录：**


---

## 三、已有输出检查

### 3.1 已生成内容的5个产品

| 产品编码 | alibaba_detail.md | selling_points.json | seo_titles.json | whatsapp.txt | rfq_template.txt | 市场版本/ |
|----------|-------------------|--------------------|--------------------|----|----|----|----|
| GF-001 | 大小:____ | 大小:____ | 大小:____ | 大小:____ | 大小:____ | 存在:☐ |
| GR-001 | 大小:____ | 大小:____ | 大小:____ | 大小:____ | 大小:____ | 存在:☐ |
| GS-001 | 大小:____ | 大小:____ | 大小:____ | 大小:____ | 大小:____ | 存在:☐ |
| HT-001 | 大小:____ | 大小:____ | 大小:____ | 大小:____ | 大小:____ | 存在:☐ |
| SH-001 | 大小:____ | 大小:____ | 大小:____ | 大小:____ | 大小:____ | 存在:☐ |

### 3.2 空壳文件标记（<100字节）

| 产品编码 | 空壳文件 | 当前大小 |
|----------|---------|---------|
| | | |
| | | |
| | | |

---

## 四、工作流脚本检查

| 脚本/文件 | 存在 | 可运行 | 备注 |
|-----------|------|--------|------|
| 03-workflows/hermes/Hermes工作流说明.md | ☐ | N/A | 文档 |
| 03-workflows/batch_processing/ | ☐ | N/A | 目录为空 |
| 03-workflows/automation/ | ☐ | N/A | 目录为空 |

---

## 五、配置文件检查

| 文件 | 存在 | 内容完整 | 备注 |
|------|------|---------|------|
| 00-config/field_mapping.md | ☐ | ☐ | |
| 00-config/project_config.md | ☐ | ☐ | |
| 00-config/workflow_rules.md | ☐ | ☐ | |

---

## 六、知识库文件检查

| 文件 | 存在 | 大小(KB) | 内容是否充实 |
|------|------|----------|-------------|
| 04-database/output/product_knowledge.md | ☐ | | |
| 04-database/output/keyword_database.md | ☐ | | |
| 04-database/output/customer_knowledge.md | ☐ | | |
| 04-database/output/market_knowledge.md | ☐ | | |
| 04-database/output/extraction_summary.json | ☐ | | |

---

## 七、目录整洁度检查

- [ ] `01-产品数据库模板/` 待清理（旧版遗留）
- [ ] `05-output/processed/` 内容检查：
- [ ] `archive/` 内容检查：
- [ ] 其他需要清理的目录或文件：

---

## 八、总结

### 可以开始批量生产的条件

- [ ] 数据库完整可用
- [ ] 6个Prompt文件全部存在且可读
- [ ] 至少1个产品的输出可作为质量参考
- [ ] 工作流文档可读

### 需要先修复的问题（按优先级排序）

1.
2.
3.

### 标杆产品选择

选择 ____ 作为首个全流程跑通的标杆产品。

选择理由：

---

*审计完成。将本报告保存后，进入 D1-任务2：标杆产品内容生成。*
