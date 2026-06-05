# AI Foreign Trade Intelligent Workspace

> v2.0 — From "AI Content Generator" to "AI + Foreign Trade + Data Operations" Workspace
> Industry: Manual Farm Tools (Shovel / Hoe / Rake / Pickaxe / Garden Tools)

## Overview

A comprehensive AI-powered foreign trade operations system for the manual farm tools industry.
Handles product data management, marketing material generation, market research, client analysis,
outreach automation, quotation assistance, CRM, and data analytics — all powered by AI.

## v2.0 vs v1.0

| Dimension | v1.0 | v2.0 |
|-----------|------|------|
| Positioning | AI content generation tool | AI foreign trade intelligent workspace |
| Data | CSV files | SQLite database |
| Architecture | Script pile | Modular + Agent-based |
| Products | 215 SKUs, manual management | Database management, AI completion |
| Content | SEO + detail page + WhatsApp | + Catalog + social media + market-localized |
| Clients | No system | CRM + AI analysis + grading |
| Market | 4 broad region versions | Per-country auto-generated reports |
| Quotation | None | Auto calculation + quotation generation |
| Outreach | Manual | AI multi-scenario generation |
| Analytics | None | Product/client/market 3D analysis |
| UI | None | CLI + Streamlit dashboard |
| Automation | Manual Hermes trigger | Agent workflows + scheduled tasks |

## Quick Start

### Phase 1 (MVP) — Weeks 1-3
Product database (SQLite) + Content generation + CRM basics + Quotation + Outreach

### Phase 2 (Enhanced) — Weeks 4-6
Market Research Agent + Client Analysis Agent + Streamlit UI + Agent workflows

### Phase 3 (Intelligent) — Weeks 7-10
Data analytics dashboard + Dify/n8n integration + Smart recommendations

## Documentation

Full project documentation: `docs/PROJECT_DOCUMENTATION_v2.md`

## Directory Structure (v2.0)

```
ai-foreign-trade-automation/
├── config/            Settings, .env, field mapping
├── data/              SQLite database, imports, backups
├── src/               Source code (9 modules + agents + utils)
├── prompts/           AI prompt templates (reorganized)
├── templates/         Document templates (catalog, quotation, reports)
├── output/            Generated files
├── assets/            Product images, logos, fonts
├── ui/                Streamlit dashboard
├── scripts/           Migration, init, backup scripts
├── tests/             Unit and integration tests
├── docs/              Project documentation
├── legacy/            v1.0 files (preserved for reference)
├── requirements.txt   Python dependencies
└── README.md          This file
```

## Tech Stack

- **Language**: Python 3.11+
- **Database**: SQLite
- **Data**: Pandas
- **LLM**: OpenAI / Claude / Gemini / Qwen (multi-provider, scenario-based routing)
- **UI**: Streamlit
- **Docs**: python-docx, FPDF2, python-pptx
- **Workflow**: Dify / n8n (Phase 3)
- **Search**: Serper API

## 9 Modules

| Module | Name | Core Function |
|--------|------|---------------|
| M1 | Product Database | Import, clean, search, AI-complete, export |
| M2 | Marketing Generator | Catalog, product sheet, market-localized versions |
| M3 | SEO Center | Alibaba, website, Facebook, LinkedIn, WhatsApp content |
| M4 | Market Research Agent | Country + product → auto report |
| M5 | Client Analysis Agent | Company info → grading + recommendations |
| M6 | Outreach Agent | Multi-scenario, multi-channel outreach generation |
| M7 | Quotation Agent | Price calculation + quotation + email |
| M8 | CRM Database | Client management, activities, tags, reminders |
| M9 | Data Analytics | Product/client/market analysis, dashboard |

## Legacy (v1.0)

v1.0 files are preserved in `legacy/` for reference.
See `legacy/项目说明文档.md` for the original project documentation.

## Migration

Run `python scripts/migrate_v1_to_v2.py` to migrate v1.0 CSV data to v2.0 SQLite.

## Setup on Another Computer

1. Clone the repo
2. Run migration: `python scripts/migrate_v1_to_v2.py`
3. Verify: `python scripts/verify_setup.py`
4. (Optional) Create your own `config/.env` from `config/.env.example`

The SQLite database is NOT tracked in Git. Run the migration script to recreate it
from the v1.0 CSV data (which IS tracked).

## License

MIT
