-- FT Workspace v2.0 Database Schema
-- SQLite database initialization script
-- Usage: sqlite3 ft_workspace.db < schema.sql

-- ============================================================
-- M1: Product Database
-- ============================================================

CREATE TABLE IF NOT EXISTS products (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    product_code        TEXT UNIQUE NOT NULL,        -- GF-001, GR-001, etc.
    product_name_en     TEXT NOT NULL,               -- Garden Rake
    product_name_cn     TEXT,                        -- 园林耙
    category            TEXT NOT NULL,               -- Digging Tools
    sub_category        TEXT,                        -- Rakes
    material            TEXT,                        -- Carbon Steel + Wooden Handle
    handle_material     TEXT,                        -- Wooden Handle
    color               TEXT,                        -- Red, Blue, Black
    weight_kg           REAL,                        -- 0.52
    head_width_cm       REAL,                        -- (nullable)
    tine_count          INTEGER,                     -- 14
    hardness            TEXT,                        -- HRC 40-45
    surface_treatment   TEXT,                        -- Polished
    moq                 INTEGER,                     -- 1200
    packaging_type      TEXT,                        -- Blister Card
    qty_per_carton      INTEGER,                     -- 50
    carton_size_cm      TEXT,                        -- 43x43x18
    gw_per_carton_kg    REAL,                        -- 26.0
    lead_time_days      INTEGER,                     -- 60
    certification       TEXT,                        -- CE
    target_keywords     TEXT,                        -- garden rake, leaf rake
    use_scenario        TEXT,                        -- Leaf gathering, lawn cleanup
    target_markets      TEXT,                        -- USA, UK, Germany
    selling_angle       TEXT,                        -- Heat-treated steel tines
    competitor_ref      TEXT,                        -- Ames, Corona, Fiskars
    seo_title_1         TEXT,
    seo_title_2         TEXT,
    seo_title_3         TEXT,
    selling_points      TEXT,                        -- Full text selling points
    whatsapp_script     TEXT,
    specifications      TEXT,                        -- Detailed dimensions: head size, handle, total length, etc.
    dimensions_image    TEXT,                        -- Path to dimensions diagram image
    alibaba_detail_status TEXT DEFAULT 'not_started',-- not_started / generated
    image_urls          TEXT,                        -- JSON array of URLs
    image_paths         TEXT,                        -- JSON array of local paths
    -- v2.0 additional fields
    hs_code             TEXT,                        -- Harmonized System code
    loading_qty_20ft    INTEGER,                     -- 20ft container loading qty
    loading_qty_40ft    INTEGER,                     -- 40ft container loading qty
    loading_qty_40hq    INTEGER,                     -- 40HQ container loading qty
    created_at          TEXT DEFAULT (datetime('now')),
    updated_at          TEXT DEFAULT (datetime('now')),
    status              TEXT DEFAULT 'active',       -- active / discontinued / pending
    source              TEXT DEFAULT 'csv_import',   -- csv_import / excel_import / manual / api
    source_file         TEXT                         -- original import file name
);

-- ============================================================
-- M8: CRM - Clients
-- ============================================================

CREATE TABLE IF NOT EXISTS clients (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name        TEXT NOT NULL,
    country             TEXT,
    website             TEXT,
    contact_person      TEXT,
    email               TEXT,
    phone               TEXT,
    whatsapp            TEXT,
    linkedin            TEXT,
    business_type       TEXT,                        -- wholesaler / retailer / distributor / importer
    main_products       TEXT,                        -- JSON array
    market_regions      TEXT,                        -- JSON array
    estimated_volume    TEXT,                        -- small / medium / large
    grade               TEXT,                        -- A / B / C (+/- suffix)
    grade_score         INTEGER,                     -- 0-100
    source              TEXT,                        -- google / alibaba / exhibition / referral / linkedin
    notes               TEXT,
    status              TEXT DEFAULT 'prospect',     -- prospect / contacted / negotiating / customer / lost
    created_at          TEXT DEFAULT (datetime('now')),
    updated_at          TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS activities (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id           INTEGER REFERENCES clients(id),
    activity_type       TEXT NOT NULL,               -- email / whatsapp / linkedin / call / meeting
    direction           TEXT,                        -- outbound / inbound
    subject             TEXT,
    content             TEXT,
    status              TEXT,                        -- sent / replied / no_reply / meeting_scheduled
    scheduled_date      TEXT,
    actual_date         TEXT,
    follow_up_date      TEXT,
    notes               TEXT,
    created_at          TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS inquiries (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id           INTEGER REFERENCES clients(id),
    product_code        TEXT,
    inquiry_source      TEXT,                        -- alibaba / email / whatsapp / website / exhibition
    inquiry_content     TEXT,
    quantity_requested  INTEGER,
    target_price        REAL,
    status              TEXT DEFAULT 'new',          -- new / quoted / negotiating / closed
    created_at          TEXT DEFAULT (datetime('now')),
    updated_at          TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS quotations (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    quotation_no        TEXT UNIQUE,                 -- QT-2026-0001
    client_id           INTEGER REFERENCES clients(id),
    product_code        TEXT,
    quantity            INTEGER,
    unit_price          REAL,
    currency            TEXT DEFAULT 'USD',
    incoterm            TEXT,                        -- FOB / CIF / EXW
    port                TEXT,                        -- Tianjin / Shanghai
    payment_terms       TEXT,
    lead_time_days      INTEGER,
    validity_days       INTEGER,
    total_amount        REAL,
    email_body          TEXT,
    quotation_file      TEXT,                        -- file path
    status              TEXT DEFAULT 'draft',        -- draft / sent / negotiated / accepted / rejected / expired
    -- ---- v4.0 报价模块扩展字段（原 data/quotation_upgrade.sql，已合并至此）----
    contact_person      TEXT,                        -- 联系人（从客户自动带出）
    country             TEXT,                        -- 客户国家（自动带出）
    loading_port        TEXT,                        -- 装运港
    destination_port    TEXT,                        -- 目的港
    valid_until         TEXT,                        -- 报价有效期（日期）
    sales_person        TEXT,                        -- 业务员
    discount_pct        REAL DEFAULT 0,              -- 整单折扣(%)
    shipping_cost       REAL DEFAULT 0,              -- 运费
    insurance_cost      REAL DEFAULT 0,              -- 保险费
    packing_cost        REAL DEFAULT 0,              -- 包装费
    other_charges       REAL DEFAULT 0,              -- 其他费用
    cost_total          REAL DEFAULT 0,              -- 成本合计
    profit_amount       REAL DEFAULT 0,              -- 利润额
    profit_margin       REAL DEFAULT 0,              -- 利润率(%)
    warranty            TEXT,                        -- 质保条款
    oem_odm             TEXT,                        -- OEM/ODM 说明
    sample_policy       TEXT,                        -- 样品政策
    packing_details     TEXT,                        -- 包装详情
    remarks             TEXT,                        -- 备注
    template_type       TEXT DEFAULT 'standard',     -- 模板类型
    revision            INTEGER DEFAULT 1,           -- 版本号
    parent_quotation_id INTEGER,                     -- 关联原始报价（用于修订版）
    created_at          TEXT DEFAULT (datetime('now')),
    updated_at          TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- Quotation Items (v4.0 报价产品明细)
-- ============================================================

CREATE TABLE IF NOT EXISTS quotation_items (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    quotation_id        INTEGER NOT NULL,            -- 关联 quotations.id
    product_code        TEXT NOT NULL,               -- 产品编码
    product_name_en     TEXT,                        -- 英文名（快照）
    sku                 TEXT,                        -- SKU
    model               TEXT,                        -- 型号
    material            TEXT,                        -- 材质
    unit                TEXT DEFAULT 'PCS',          -- 单位
    quantity            INTEGER DEFAULT 1,           -- 数量
    unit_price          REAL DEFAULT 0,              -- 单价
    discount_pct        REAL DEFAULT 0,              -- 行折扣(%)
    amount              REAL DEFAULT 0,              -- 金额 = qty * price * (1 - discount%)
    weight_kg           REAL,                        -- 单件重量
    moq                 INTEGER,                     -- MOQ
    packaging           TEXT,                        -- 包装方式
    lead_time_days      INTEGER,                     -- 交期
    ai_highlights       TEXT,                        -- AI 产品亮点
    sort_order          INTEGER DEFAULT 0,           -- 排序
    created_at          TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (quotation_id) REFERENCES quotations(id) ON DELETE CASCADE
);

-- ============================================================
-- Quotation Versions (v4.0 报价版本历史)
-- ============================================================

CREATE TABLE IF NOT EXISTS quotation_versions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    quotation_id        INTEGER NOT NULL,            -- 关联 quotations.id
    revision            INTEGER NOT NULL,            -- 版本号
    snapshot_json       TEXT NOT NULL,               -- 完整快照（JSON）
    change_summary      TEXT,                        -- 变更说明
    created_at          TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (quotation_id) REFERENCES quotations(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS orders (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id           INTEGER REFERENCES clients(id),
    order_no            TEXT UNIQUE,
    products            TEXT,                        -- JSON: [{product_code, quantity, price}]
    total_amount        REAL,
    currency            TEXT DEFAULT 'USD',
    order_date          TEXT,
    delivery_date       TEXT,
    status              TEXT DEFAULT 'pending',      -- pending / confirmed / shipped / delivered
    notes               TEXT,
    created_at          TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS client_tags (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    name                TEXT UNIQUE NOT NULL,
    color               TEXT,
    description         TEXT,
    created_at          TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS client_tag_mapping (
    client_id           INTEGER REFERENCES clients(id),
    tag_id              INTEGER REFERENCES client_tags(id),
    PRIMARY KEY (client_id, tag_id)
);

-- ============================================================
-- M4: Market Research
-- ============================================================

CREATE TABLE IF NOT EXISTS market_reports (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    country             TEXT NOT NULL,
    product_category    TEXT,
    report_title        TEXT,
    summary             TEXT,                        -- 200 char summary
    full_report         TEXT,                        -- full markdown
    report_file         TEXT,                        -- PDF file path
    data_sources        TEXT,                        -- JSON: source list
    confidence          TEXT,                        -- high / medium / low
    created_at          TEXT DEFAULT (datetime('now')),
    updated_at          TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS market_knowledge (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    country             TEXT NOT NULL,
    category            TEXT,                        -- agriculture / import / competitor / pricing
    knowledge           TEXT,
    source              TEXT,
    verified            INTEGER DEFAULT 0,           -- 0 or 1
    created_at          TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- M5: Client Analysis
-- ============================================================

CREATE TABLE IF NOT EXISTS client_analyses (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id           INTEGER REFERENCES clients(id),
    analysis_type       TEXT,                        -- initial / update
    summary             TEXT,
    full_analysis       TEXT,
    grade_suggested     TEXT,
    recommendations     TEXT,
    created_at          TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- M3: Content Records
-- ============================================================

CREATE TABLE IF NOT EXISTS content_records (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    product_code        TEXT,
    content_type        TEXT NOT NULL,               -- seo_title / detail_page / facebook / linkedin / whatsapp
    platform            TEXT,                        -- alibaba / website / facebook / linkedin / whatsapp
    target_market       TEXT,                        -- global / nigeria / kenya / ...
    content             TEXT,
    version             INTEGER DEFAULT 1,
    status              TEXT DEFAULT 'draft',        -- draft / reviewed / published
    created_at          TEXT DEFAULT (datetime('now')),
    reviewed_at         TEXT
);

-- ============================================================
-- M6: Outreach Templates
-- ============================================================

CREATE TABLE IF NOT EXISTS outreach_templates (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    name                TEXT NOT NULL,
    scenario            TEXT,                        -- initial / follow_up / post_exhibition / quotation_followup
    channel             TEXT,                        -- email / whatsapp / linkedin
    style               TEXT,                        -- professional / casual / relationship
    template_body       TEXT,
    subject_line        TEXT,
    usage_count         INTEGER DEFAULT 0,
    success_rate        REAL,
    created_at          TEXT DEFAULT (datetime('now')),
    updated_at          TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- M7: Price Records
-- ============================================================

CREATE TABLE IF NOT EXISTS price_records (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    product_code        TEXT,
    base_price_usd      REAL,
    min_price_usd       REAL,
    target_market       TEXT,
    effective_date      TEXT,
    notes               TEXT,
    created_at          TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- Product Images (auxiliary)
-- ============================================================

CREATE TABLE IF NOT EXISTS product_images (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    product_code        TEXT,
    image_type          TEXT,                        -- main / detail / packaging / scene
    file_path           TEXT,
    url                 TEXT,
    description         TEXT,
    created_at          TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- Indexes
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_products_code ON products(product_code);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_status ON products(status);
CREATE INDEX IF NOT EXISTS idx_clients_country ON clients(country);
CREATE INDEX IF NOT EXISTS idx_clients_grade ON clients(grade);
CREATE INDEX IF NOT EXISTS idx_clients_status ON clients(status);
CREATE INDEX IF NOT EXISTS idx_activities_client ON activities(client_id);
CREATE INDEX IF NOT EXISTS idx_inquiries_client ON inquiries(client_id);
CREATE INDEX IF NOT EXISTS idx_quotations_client ON quotations(client_id);
CREATE INDEX IF NOT EXISTS idx_quotations_status ON quotations(status);
CREATE INDEX IF NOT EXISTS idx_quotations_quotation_no ON quotations(quotation_no);
CREATE INDEX IF NOT EXISTS idx_quotation_items_quotation_id ON quotation_items(quotation_id);
CREATE INDEX IF NOT EXISTS idx_quotation_items_product_code ON quotation_items(product_code);
CREATE INDEX IF NOT EXISTS idx_quotation_versions_quotation_id ON quotation_versions(quotation_id);
CREATE INDEX IF NOT EXISTS idx_market_reports_country ON market_reports(country);
CREATE INDEX IF NOT EXISTS idx_content_product ON content_records(product_code);
CREATE INDEX IF NOT EXISTS idx_content_type ON content_records(content_type);
