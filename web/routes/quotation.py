"""
Quotation API Routes — Professional B2B Quotation System
=========================================================
Endpoints for CRUD, versioning, pricing calculation, templates, and stats.
"""

import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse

from web.deps import get_db, get_fresh_db

router = APIRouter(prefix="/quotation")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _generate_quotation_no(db) -> str:
    """Generate QT-YYYY-NNN format number."""
    year = datetime.now().year
    prefix = f"QT-{year}-"
    row = db.fetchone(
        "SELECT quotation_no FROM quotations WHERE quotation_no LIKE ? ORDER BY quotation_no DESC LIMIT 1",
        (f"{prefix}%",),
    )
    if row and row.get("quotation_no"):
        try:
            seq = int(row["quotation_no"].split("-")[-1]) + 1
        except (ValueError, IndexError):
            seq = 1
    else:
        seq = 1
    return f"{prefix}{seq:03d}"


def _recalculate(db, quotation_id: int) -> dict:
    """Recalculate totals from quotation_items and header costs."""
    items = db.fetchall(
        "SELECT * FROM quotation_items WHERE quotation_id = ? ORDER BY sort_order",
        (quotation_id,),
    )
    total_items = sum(float(i.get("amount") or 0) for i in items)

    header = db.fetchone(
        "SELECT * FROM quotations WHERE id = ?", (quotation_id,)
    )
    if not header:
        return {}

    discount_pct = float(header.get("discount_pct") or 0)
    shipping = float(header.get("shipping_cost") or 0)
    insurance = float(header.get("insurance_cost") or 0)
    packing = float(header.get("packing_cost") or 0)
    other = float(header.get("other_charges") or 0)

    discounted = total_items * (1 - discount_pct / 100)
    total_amount = round(discounted + shipping + insurance + packing + other, 2)

    # cost_total comes from product cost; if unavailable we use total_items as base cost
    cost_total = round(float(header.get("cost_total") or total_items), 2)
    profit_amount = round(total_amount - cost_total, 2)
    profit_margin = round((profit_amount / total_amount * 100) if total_amount else 0, 2)

    db.execute(
        """UPDATE quotations SET
            total_amount = ?, cost_total = ?, profit_amount = ?,
            profit_margin = ?, updated_at = ?
           WHERE id = ?""",
        (total_amount, cost_total, profit_amount, profit_margin, _now(), quotation_id),
    )
    db.commit()

    return {
        "total_amount": total_amount,
        "cost_total": cost_total,
        "profit_amount": profit_amount,
        "profit_margin": profit_margin,
    }


# ---------------------------------------------------------------------------
# 1. Root redirect
# ---------------------------------------------------------------------------

@router.get("/")
def quotation_root():
    return RedirectResponse(url="/quotation/api/list", status_code=302)


# ---------------------------------------------------------------------------
# 2. List quotations
# ---------------------------------------------------------------------------

@router.get("/api/list")
def list_quotations(
    status: Optional[str] = Query(None),
    client_id: Optional[int] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(200, ge=1, le=2000),
):
    db = get_db()
    where, params = [], []

    if status:
        where.append("q.status = ?")
        params.append(status)
    if client_id:
        where.append("q.client_id = ?")
        params.append(client_id)
    if date_from:
        where.append("q.created_at >= ?")
        params.append(date_from)
    if date_to:
        where.append("q.created_at <= ?")
        params.append(date_to + " 23:59:59")
    if search:
        where.append("(q.quotation_no LIKE ? OR q.product_code LIKE ? OR q.notes LIKE ?)")
        s = f"%{search}%"
        params.extend([s, s, s])

    clause = (" WHERE " + " AND ".join(where)) if where else ""

    sql = f"""
        SELECT q.*, c.company_name AS client_name, c.country AS client_country
        FROM quotations q
        LEFT JOIN clients c ON q.client_id = c.id
        {clause}
        ORDER BY q.created_at DESC
        LIMIT ?
    """
    params.append(limit)
    rows = db.fetchall(sql, params)
    return {"quotations": rows, "total": len(rows)}


# ---------------------------------------------------------------------------
# 3. Get single quotation with items
# ---------------------------------------------------------------------------

@router.post("/api/create")
def create_quotation(request_body: dict):
    db = get_db()
    now = _now()

    quotation_no = _generate_quotation_no(db)
    items = request_body.pop("items", [])

    # Build insert columns/values for header
    header = {k: v for k, v in request_body.items() if v is not None}
    header["quotation_no"] = quotation_no
    header["status"] = header.get("status", "draft")
    header["revision"] = header.get("revision", 1)
    header["created_at"] = now
    header["updated_at"] = now

    cols = ", ".join(header.keys())
    placeholders = ", ".join(["?"] * len(header))
    cur = db.execute(
        f"INSERT INTO quotations ({cols}) VALUES ({placeholders})",
        list(header.values()),
    )
    db.commit()

    q = db.fetchone("SELECT id FROM quotations WHERE quotation_no = ?", (quotation_no,))
    quotation_id = q["id"]

    # Insert items
    for idx, item in enumerate(items):
        item_data = {k: v for k, v in item.items() if v is not None}
        item_data["quotation_id"] = quotation_id
        item_data["sort_order"] = idx
        if "amount" not in item_data:
            qty = float(item_data.get("quantity") or 0)
            up = float(item_data.get("unit_price") or 0)
            disc = float(item_data.get("discount_pct") or 0)
            item_data["amount"] = round(qty * up * (1 - disc / 100), 2)
        item_data["created_at"] = now

        icols = ", ".join(item_data.keys())
        iph = ", ".join(["?"] * len(item_data))
        db.execute(
            f"INSERT INTO quotation_items ({icols}) VALUES ({iph})",
            list(item_data.values()),
        )
    db.commit()

    totals = _recalculate(db, quotation_id)

    return {
        "message": "Quotation created",
        "quotation_no": quotation_no,
        "totals": totals,
    }


# ---------------------------------------------------------------------------
# 5. Update quotation
# ---------------------------------------------------------------------------

@router.post("/api/calculate")
def calculate_pricing(body: dict):
    """
    Calculate pricing for a product line.
    Expects: product_code, quantity, unit_price, discount_pct (optional),
             shipping_cost, insurance_cost, packing_cost, other_charges
    """
    db = get_db()
    product_code = body.get("product_code", "")
    quantity = float(body.get("quantity") or 1)
    unit_price = float(body.get("unit_price") or 0)
    discount_pct = float(body.get("discount_pct") or 0)

    # Fetch product cost if available
    product = db.fetchone(
        "SELECT * FROM products WHERE product_code = ?", (product_code,)
    )
    cost_per_unit = float(product.get("unit_price") or 0) if product else unit_price * 0.6

    line_amount = round(quantity * unit_price * (1 - discount_pct / 100), 2)
    line_cost = round(quantity * cost_per_unit, 2)

    shipping = float(body.get("shipping_cost") or 0)
    insurance = float(body.get("insurance_cost") or 0)
    packing = float(body.get("packing_cost") or 0)
    other = float(body.get("other_charges") or 0)

    total = round(line_amount + shipping + insurance + packing + other, 2)
    profit = round(total - line_cost, 2)
    margin = round((profit / total * 100) if total else 0, 2)

    return {
        "product_code": product_code,
        "quantity": quantity,
        "unit_price": unit_price,
        "discount_pct": discount_pct,
        "line_amount": line_amount,
        "cost_per_unit": cost_per_unit,
        "line_cost": line_cost,
        "shipping": shipping,
        "insurance": insurance,
        "packing": packing,
        "other": other,
        "total": total,
        "profit": profit,
        "margin_pct": margin,
    }


# ---------------------------------------------------------------------------
# 10. AI price optimization (stub)
# ---------------------------------------------------------------------------

@router.post("/api/ai-optimize")
def ai_optimize(body: dict):
    """AI price suggestion — returns mock data for now."""
    product_code = body.get("product_code", "UNKNOWN")
    quantity = float(body.get("quantity") or 100)
    base_price = float(body.get("unit_price") or 0)

    return {
        "product_code": product_code,
        "quantity": quantity,
        "base_price": base_price,
        "suggestions": [
            {
                "strategy": "competitive",
                "unit_price": round(base_price * 0.92, 2),
                "estimated_margin_pct": 22.0,
                "reason": "Below market avg to win order",
            },
            {
                "strategy": "standard",
                "unit_price": round(base_price, 2),
                "estimated_margin_pct": 35.0,
                "reason": "Market-aligned pricing",
            },
            {
                "strategy": "premium",
                "unit_price": round(base_price * 1.12, 2),
                "estimated_margin_pct": 45.0,
                "reason": "Premium positioning with value-adds",
            },
        ],
        "note": "Mock AI suggestions — integrate real model later",
    }


# ---------------------------------------------------------------------------
# 11. Templates
# ---------------------------------------------------------------------------

TEMPLATES = [
    {"id": "standard", "name": "Standard Quotation", "description": "Default B2B quotation template with full pricing breakdown"},
    {"id": "proforma", "name": "Proforma Invoice", "description": "Proforma invoice style quotation for customs/banking"},
    {"id": "simple", "name": "Simple Price List", "description": "Minimal price list without detailed cost breakdown"},
    {"id": "oem", "name": "OEM/ODM Proposal", "description": "Template for OEM/ODM projects with MOQ and tooling info"},
]


@router.get("/api/templates")
def list_templates():
    return {"templates": TEMPLATES}


# ---------------------------------------------------------------------------
# 12. Statistics
# ---------------------------------------------------------------------------

@router.get("/api/stats")
def quotation_stats():
    db = get_db()

    total = db.fetchone("SELECT COUNT(*) AS cnt FROM quotations") or {}
    by_status = db.fetchall(
        "SELECT status, COUNT(*) AS cnt FROM quotations GROUP BY status ORDER BY cnt DESC"
    )
    recent = db.fetchone(
        "SELECT COUNT(*) AS cnt FROM quotations WHERE created_at >= date('now', '-30 days')"
    ) or {}
    revenue = db.fetchone(
        "SELECT SUM(total_amount) AS total, SUM(profit_amount) AS profit FROM quotations WHERE status != 'cancelled'"
    ) or {}
    top_clients = db.fetchall(
        """SELECT c.company_name, COUNT(q.id) AS cnt, SUM(q.total_amount) AS value
           FROM quotations q JOIN clients c ON q.client_id = c.id
           GROUP BY q.client_id ORDER BY value DESC LIMIT 10"""
    )

    return {
        "total_quotations": total.get("cnt", 0),
        "by_status": by_status,
        "last_30_days": recent.get("cnt", 0),
        "total_revenue": revenue.get("total") or 0,
        "total_profit": revenue.get("profit") or 0,
        "top_clients": top_clients,
    }

@router.get("/api/{quotation_no}")
def get_quotation(quotation_no: str):
    db = get_db()
    q = db.fetchone(
        """SELECT q.*, c.company_name AS client_name, c.country AS client_country,
                  c.contact_person AS client_contact, c.email AS client_email
           FROM quotations q
           LEFT JOIN clients c ON q.client_id = c.id
           WHERE q.quotation_no = ?""",
        (quotation_no,),
    )
    if not q:
        return JSONResponse(status_code=404, content={"error": "Quotation not found"})

    items = db.fetchall(
        "SELECT * FROM quotation_items WHERE quotation_id = ? ORDER BY sort_order",
        (q["id"],),
    )
    return {"quotation": q, "items": items}


# ---------------------------------------------------------------------------
# 4. Create quotation
# ---------------------------------------------------------------------------

@router.put("/api/{quotation_no}")
def update_quotation(quotation_no: str, request_body: dict):
    db = get_db()
    q = db.fetchone("SELECT id FROM quotations WHERE quotation_no = ?", (quotation_no,))
    if not q:
        return JSONResponse(status_code=404, content={"error": "Quotation not found"})

    quotation_id = q["id"]
    items = request_body.pop("items", None)
    now = _now()

    # Update header
    header = {k: v for k, v in request_body.items() if v is not None}
    if header:
        header["updated_at"] = now
        sets = ", ".join(f"{k} = ?" for k in header)
        db.execute(
            f"UPDATE quotations SET {sets} WHERE id = ?",
            list(header.values()) + [quotation_id],
        )
        db.commit()

    # Replace items if provided
    if items is not None:
        db.execute("DELETE FROM quotation_items WHERE quotation_id = ?", (quotation_id,))
        for idx, item in enumerate(items):
            item_data = {k: v for k, v in item.items() if v is not None}
            item_data["quotation_id"] = quotation_id
            item_data["sort_order"] = idx
            if "amount" not in item_data:
                qty = float(item_data.get("quantity") or 0)
                up = float(item_data.get("unit_price") or 0)
                disc = float(item_data.get("discount_pct") or 0)
                item_data["amount"] = round(qty * up * (1 - disc / 100), 2)
            item_data["created_at"] = now

            icols = ", ".join(item_data.keys())
            iph = ", ".join(["?"] * len(item_data))
            db.execute(
                f"INSERT INTO quotation_items ({icols}) VALUES ({iph})",
                list(item_data.values()),
            )
        db.commit()

    totals = _recalculate(db, quotation_id)

    return {"message": "Quotation updated", "quotation_no": quotation_no, "totals": totals}


# ---------------------------------------------------------------------------
# 6. Delete quotation
# ---------------------------------------------------------------------------

@router.delete("/api/{quotation_no}")
def delete_quotation(quotation_no: str):
    db = get_db()
    q = db.fetchone("SELECT id FROM quotations WHERE quotation_no = ?", (quotation_no,))
    if not q:
        return JSONResponse(status_code=404, content={"error": "Quotation not found"})

    quotation_id = q["id"]
    db.execute("DELETE FROM quotation_items WHERE quotation_id = ?", (quotation_id,))
    db.execute("DELETE FROM quotation_versions WHERE quotation_id = ?", (quotation_id,))
    db.execute("DELETE FROM quotations WHERE id = ?", (quotation_id,))
    db.commit()

    return {"message": "Quotation deleted", "quotation_no": quotation_no}


# ---------------------------------------------------------------------------
# 7. Version history
# ---------------------------------------------------------------------------

@router.get("/api/{quotation_no}/versions")
def get_versions(quotation_no: str):
    db = get_db()
    q = db.fetchone("SELECT id FROM quotations WHERE quotation_no = ?", (quotation_no,))
    if not q:
        return JSONResponse(status_code=404, content={"error": "Quotation not found"})

    versions = db.fetchall(
        "SELECT * FROM quotation_versions WHERE quotation_id = ? ORDER BY revision DESC",
        (q["id"],),
    )
    return {"versions": versions}


# ---------------------------------------------------------------------------
# 8. Create revision
# ---------------------------------------------------------------------------

@router.post("/api/{quotation_no}/revision")
def create_revision(quotation_no: str, body: dict = None):
    db = get_db()
    q = db.fetchone("SELECT * FROM quotations WHERE quotation_no = ?", (quotation_no,))
    if not q:
        return JSONResponse(status_code=404, content={"error": "Quotation not found"})

    quotation_id = q["id"]
    items = db.fetchall(
        "SELECT * FROM quotation_items WHERE quotation_id = ? ORDER BY sort_order",
        (quotation_id,),
    )

    new_revision = int(q.get("revision") or 1) + 1
    snapshot = {
        "quotation": {k: v for k, v in q.items()},
        "items": [dict(i) for i in items],
    }
    change_summary = (body or {}).get("change_summary", "")

    db.execute(
        """INSERT INTO quotation_versions (quotation_id, revision, snapshot_json, change_summary, created_at)
           VALUES (?, ?, ?, ?, ?)""",
        (quotation_id, new_revision, json.dumps(snapshot, default=str), change_summary, _now()),
    )
    db.execute(
        "UPDATE quotations SET revision = ?, updated_at = ? WHERE id = ?",
        (new_revision, _now(), quotation_id),
    )
    db.commit()

    return {"message": "Revision created", "revision": new_revision}


# ---------------------------------------------------------------------------
# 9. Pricing calculation
# ---------------------------------------------------------------------------


