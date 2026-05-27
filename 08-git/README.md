# AI Foreign Trade Automation System

## Purpose
Automated product content generation for foreign trade operations.
Uses AI (Hermes + Qwen) to generate SEO titles, detail pages, RFQ replies, and WhatsApp scripts from product database.

## Directory Structure
```
00-config/          Project config, field mapping, workflow rules
01-input/           Input data: PDFs, Excel, raw data, images
02-prompts/         AI prompt templates (SEO, detail, RFQ, WhatsApp, batch)
03-workflows/       Hermes automation, batch processing, scripts
04-database/        Product database templates, knowledge base, output
05-output/          Generated content: SEO, detail pages, RFQ, WhatsApp
06-assets/          Product images, icons, banners
07-docs/            SOPs, project notes, testing reports, daily tasks
08-git/             Git config, README, version log
archive/            Archived/unclassified files
```

## Workflow
1. **Input** (01-input/): PDF catalogs, raw product data
2. **Database** (04-database/): Extracted & structured product data in Excel templates
3. **Prompts** (02-prompts/): AI prompt templates for each output type
4. **Workflows** (03-workflows/): Hermes automation scripts for batch processing
5. **Output** (05-output/): Generated SEO titles, detail pages, RFQ replies, WhatsApp scripts

## Prompt Management
All prompts centralized in 02-prompts/:
- `seo/`           SEO title generation prompts
- `detail_page/`   Product detail page content prompts
- `rfq/`           RFQ reply templates
- `whatsapp/`      WhatsApp message scripts
- `batch_workflow/` Batch processing & market localization prompts

## Git Sync
```bash
git add .
git commit -m "update: [description]"
git push
```

## Daily Tasks
See 07-docs/SOP/daily_tasks/ for day-by-day learning and execution tasks.
