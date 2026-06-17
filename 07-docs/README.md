# 🔨 Foreign Trade AI Workspace V0.1

> AI-powered content generation platform for manual farm tool exporters.
> Generate SEO titles, selling points, and WhatsApp scripts for 215+ products with one click.

---

## Features

- **Product Database** — 215 products across 3 categories (Weeding, Digging, Cutting), SQLite-backed with 43 fields per product
- **AI Content Generation** — One-click generation of SEO titles, product selling points, and WhatsApp outreach scripts via DeepSeek API
- **Streamlit Web Interface** — Search products, view details, and generate AI content in a clean web UI
- **CLI Tool** — Full command-line interface for batch operations, data management, and automation
- **Batch Processing** — Generate content for all products at once with retry logic and progress logging

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | Python 3.10+ |
| Database | SQLite (WAL mode) |
| AI Provider | DeepSeek API (OpenAI-compatible) |
| CLI Framework | Custom argument parser |
| Version Control | Git + GitHub |

---

## Project Structure

```
05_ai-foreign-trade-automation/
├── app.py                    # Streamlit web interface
├── config.py                 # Project config loader
├── ft_workspace.db           # SQLite database (215 products)
├── data/
│   └── ft_workspace.db       # Database file
├── scripts/
│   └── ft_cli.py             # CLI entry point
├── src/
│   ├── core/
│   │   ├── config.py         # Settings & env loader
│   │   ├── database.py       # SQLite wrapper (FTDatabase)
│   │   └── llm_client.py     # DeepSeek API client
│   ├── utils/
│   │   └── prompts.py        # Prompt template loader
│   ├── m1_product_db/        # Module 1: Product database
│   ├── m2_marketing/         # Module 2: Marketing materials
│   ├── m3_seo/               # Module 3: SEO content
│   ├── m4_market_research/   # Module 4: Market research
│   ├── m5_client_analysis/   # Module 5: Client analysis
│   ├── m6_outreach/          # Module 6: Outreach agent
│   ├── m7_quotation/         # Module 7: Quotation assistant
│   ├── m8_crm/               # Module 8: CRM
│   └── m9_analytics/         # Module 9: Data analytics
├── prompts/
│   ├── seo/                  # SEO title prompt templates
│   └── social/               # WhatsApp script templates
├── output/
│   └── generate_log.txt      # Batch generation log
├── config/
│   ├── settings.yaml         # App settings
│   └── .env                  # API keys (git-ignored)
└── .venv/                    # Python virtual environment
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- A DeepSeek API key

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/rileymskcnctools-oss/05_ai-foreign-trade-automation.git
cd 05_ai-foreign-trade-automation

# 2. Create virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 3. Install dependencies
pip install streamlit openai requests pyyaml

# 4. Configure API key
# Create config/.env and add your DeepSeek API key:
echo 'DEEPSEEK_API_KEY="your-key-here"' > config/.env
```

### Launch Web Interface

```bash
streamlit run app.py
```

Opens at http://localhost:8501

### Use CLI

```bash
# Search products
python scripts/ft_cli.py search "hoe"

# View statistics
python scripts/ft_cli.py stats

# Generate SEO title for one product
python scripts/ft_cli.py generate GF-001 --type seo

# Generate all content types for one product
python scripts/ft_cli.py generate GF-001 --type all

# Batch generate for all products
python scripts/ft_cli.py generate all --type all

# Batch with limit
python scripts/ft_cli.py generate all --type seo --limit 10

# Check missing fields
python scripts/ft_cli.py missing
```

---

## How It Works

```
User selects product → Clicks "Generate" button
        ↓
Streamlit calls generate_ai_content()
        ↓
System loads prompt template (SEO / Selling Points / WhatsApp)
        ↓
Fills template with product data (name, material, specs, keywords)
        ↓
Sends to DeepSeek API → Receives generated content
        ↓
Saves result back to SQLite database
        ↓
Displays content on the page
```

---

## Database Schema

The database stores 215 manual farm tool products with 43 fields per product:

| Category | Fields |
|----------|--------|
| Identity | product_code, product_name_en, product_name_cn |
| Classification | category, sub_category |
| Specs | material, handle_material, length_cm, weight_kg, hardness, surface_treatment |
| Packaging | packaging_type, qty_per_carton, carton_size_cm, gw_per_carton_kg |
| Trade | moq, lead_time_days, certification, hs_code |
| SEO | target_keywords, use_scenario, target_markets, selling_angle |
| AI Content | seo_title_1/2/3, selling_points, whatsapp_script |
| Metadata | status, source, created_at, updated_at |

---

## Sample Products

| Code | Name | Category | Material |
|------|------|----------|----------|
| GF-001 | Garden Fork | Digging Tools | Carbon Steel + Ash Wood |
| HE-001 | Garden Hoe | Weeding Tools | Carbon Steel + Wooden Handle |
| RK-001 | Garden Rake | Digging Tools | Carbon Steel + Ash Wood |
| SH-001 | Shovel | Digging Tools | Carbon Steel + Ash Wood |
| AX-001 | Axe | Cutting Tools | High Carbon Steel + Hickory |

---

## AI Generation Examples

### SEO Title (before → after)

**Before:** (empty)
**After:** "Garden Fork 4 Tine Digging Fork Carbon Steel Ash Wood Handle 30cm"

### Selling Points (excerpt)

> **1. Material & Durability**
> Feature: The tines are forged from high-carbon steel...
> Benefit: Resists bending under heavy loads, lasts 3x longer than standard garden forks...

### WhatsApp Script (excerpt)

> 你好，遵照您的指示，作为一名有10年经验的Garden Tools外贸业务员...

---

## Development Timeline

| Week | Milestone | Status |
|------|-----------|--------|
| 1-2 | Project setup + SQLite database + CSV import | ✅ Complete |
| 3-4 | DeepSeek AI integration + Prompt templates | ✅ Complete |
| 5 | Batch processing + Retry + Logging | ✅ Complete |
| 6 | Streamlit web interface + Product search | ✅ Complete |
| 7 | AI workspace: Generate → Save → Display | ✅ Complete |
| 8 | Testing (30 products) + README + Release | ✅ Complete |

---

## Known Limitations

- hs_code and loading quantities are not yet populated for all products
- No user authentication (internal tool only)
- AI content quality depends on product data completeness
- Single-user Streamlit server (not production-grade)

---

## Future Improvements

- [ ] Alibaba product listing generator
- [ ] Multi-language support (English / French / Arabic)
- [ ] Product image management
- [ ] Client CRM integration
- [ ] Quotation auto-generation
- [ ] Market research agent

---

## License

Internal project for portfolio demonstration.

---

Built with ❤️ by a foreign trade professional transitioning to AI data operations.
