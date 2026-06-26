-- FT Workspace v4.0 — 报价模块 Schema 升级
-- 通用 B2B 外贸报价系统，不针对特定行业

-- ========================================
-- 1. 升级 quotations 表（报价头）
-- ========================================
-- 新增字段通过 ALTER TABLE 添加，保留原有数据

-- 报价头新增字段
ALTER TABLE quotations ADD COLUMN contact_person TEXT;        -- 联系人（从客户自动带出）
ALTER TABLE quotations ADD COLUMN country TEXT;                -- 客户国家（自动带出）
ALTER TABLE quotations ADD COLUMN loading_port TEXT;           -- 装运港
ALTER TABLE quotations ADD COLUMN destination_port TEXT;       -- 目的港
ALTER TABLE quotations ADD COLUMN valid_until TEXT;            -- 报价有效期（日期）
ALTER TABLE quotations ADD COLUMN sales_person TEXT;           -- 业务员
ALTER TABLE quotations ADD COLUMN discount_pct REAL DEFAULT 0; -- 整单折扣(%)
ALTER TABLE quotations ADD COLUMN shipping_cost REAL DEFAULT 0; -- 运费
ALTER TABLE quotations ADD COLUMN insurance_cost REAL DEFAULT 0; -- 保险费
ALTER TABLE quotations ADD COLUMN packing_cost REAL DEFAULT 0;  -- 包装费
ALTER TABLE quotations ADD COLUMN other_charges REAL DEFAULT 0;  -- 其他费用
ALTER TABLE quotations ADD COLUMN cost_total REAL DEFAULT 0;     -- 成本合计
ALTER TABLE quotations ADD COLUMN profit_amount REAL DEFAULT 0;  -- 利润额
ALTER TABLE quotations ADD COLUMN profit_margin REAL DEFAULT 0;  -- 利润率(%)
ALTER TABLE quotations ADD COLUMN warranty TEXT;               -- 质保条款
ALTER TABLE quotations ADD COLUMN oem_odm TEXT;                -- OEM/ODM 说明
ALTER TABLE quotations ADD COLUMN sample_policy TEXT;          -- 样品政策
ALTER TABLE quotations ADD COLUMN packing_details TEXT;        -- 包装详情
ALTER TABLE quotations ADD COLUMN remarks TEXT;                -- 备注
ALTER TABLE quotations ADD COLUMN template_type TEXT DEFAULT 'standard'; -- 模板类型
ALTER TABLE quotations ADD COLUMN revision INTEGER DEFAULT 1;  -- 版本号
ALTER TABLE quotations ADD COLUMN parent_quotation_id INTEGER; -- 关联原始报价（用于修订版）

-- ========================================
-- 2. 新建 quotation_items 表（报价产品明细）
-- ========================================
CREATE TABLE IF NOT EXISTS quotation_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quotation_id INTEGER NOT NULL,           -- 关联 quotations.id
    product_code TEXT NOT NULL,               -- 产品编码
    product_name_en TEXT,                     -- 英文名（快照）
    sku TEXT,                                 -- SKU
    model TEXT,                               -- 型号
    material TEXT,                            -- 材质
    unit TEXT DEFAULT 'PCS',                  -- 单位
    quantity INTEGER DEFAULT 1,               -- 数量
    unit_price REAL DEFAULT 0,                -- 单价
    discount_pct REAL DEFAULT 0,              -- 行折扣(%)
    amount REAL DEFAULT 0,                    -- 金额 = qty * price * (1 - discount%)
    weight_kg REAL,                           -- 单件重量
    moq INTEGER,                              -- MOQ
    packaging TEXT,                           -- 包装方式
    lead_time_days INTEGER,                   -- 交期
    ai_highlights TEXT,                       -- AI 产品亮点
    sort_order INTEGER DEFAULT 0,             -- 排序
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (quotation_id) REFERENCES quotations(id) ON DELETE CASCADE
);

-- ========================================
-- 3. 新建 quotation_versions 表（版本历史）
-- ========================================
CREATE TABLE IF NOT EXISTS quotation_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quotation_id INTEGER NOT NULL,            -- 关联 quotations.id
    revision INTEGER NOT NULL,                -- 版本号
    snapshot_json TEXT NOT NULL,              -- 完整快照（JSON）
    change_summary TEXT,                      -- 变更说明
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (quotation_id) REFERENCES quotations(id) ON DELETE CASCADE
);

-- ========================================
-- 4. 索引
-- ========================================
CREATE INDEX IF NOT EXISTS idx_quotation_items_quotation_id ON quotation_items(quotation_id);
CREATE INDEX IF NOT EXISTS idx_quotation_items_product_code ON quotation_items(product_code);
CREATE INDEX IF NOT EXISTS idx_quotation_versions_quotation_id ON quotation_versions(quotation_id);
CREATE INDEX IF NOT EXISTS idx_quotations_client_id ON quotations(client_id);
CREATE INDEX IF NOT EXISTS idx_quotations_status ON quotations(status);
CREATE INDEX IF NOT EXISTS idx_quotations_quotation_no ON quotations(quotation_no);
