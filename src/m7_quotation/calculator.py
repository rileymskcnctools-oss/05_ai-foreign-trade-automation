"""
M7: 价格计算器 - 报价核心逻辑
功能：产品价格计算、利润计算、装柜量计算、批量报价。
"""

from datetime import datetime
from typing import Optional

from src.core.database import FTDatabase


# ============================================================
# 装柜量常量（标准集装箱内尺寸，单位：立方米）
# ============================================================
CONTAINER_SPECS = {
    "20ft":  {"name": "20' Container",  "cbm": 28.5,  "max_weight_kg": 21770},
    "40ft":  {"name": "40' Container",  "cbm": 57.8,  "max_weight_kg": 26680},
    "40hq":  {"name": '40\' HQ Container', "cbm": 65.0, "max_weight_kg": 26680},
}

# 运费参考（USD/CBM，天津港出发）
FREIGHT_RATES = {
    "Africa":    {"20ft": 50, "40ft": 85, "40hq": 95},
    "Europe":    {"20ft": 60, "40ft": 100, "40hq": 115},
    "Asia":      {"20ft": 35, "40ft": 60, "40hq": 70},
    "Americas":  {"20ft": 65, "40ft": 110, "40hq": 125},
    "default":   {"20ft": 50, "40ft": 85, "40hq": 95},
}


class PriceCalculator:
    """报价价格计算器"""

    def __init__(self, db: Optional[FTDatabase] = None):
        self.db = db or FTDatabase()

    # ---- 价格查询 ----

    def get_price(self, product_code: str, market: str = "") -> Optional[dict]:
        """获取产品最新价格"""
        row = self.db.fetchone(
            """SELECT * FROM price_records 
               WHERE product_code = ? AND (target_market = ? OR target_market = '')
               ORDER BY effective_date DESC LIMIT 1""",
            (product_code, market)
        )
        if row:
            return dict(row)
        return None

    def set_price(
        self,
        product_code: str,
        base_price: float,
        min_price: Optional[float] = None,
        market: str = "",
        notes: str = "",
    ) -> int:
        """设置产品价格"""
        now = datetime.now().strftime("%Y-%m-%d")
        cursor = self.db.execute(
            """INSERT INTO price_records 
               (product_code, base_price_usd, min_price_usd, target_market, 
                effective_date, notes, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (product_code, base_price, min_price, market, now, notes, datetime.now().isoformat())
        )
        self.db.commit()
        return cursor.lastrowid

    # ---- 报价计算 ----

    def calculate_price(
        self,
        product_code: str,
        quantity: int,
        market: str = "",
        incoterm: str = "FOB",
        currency: str = "USD",
        margin_pct: float = 15.0,
    ) -> dict:
        """
        计算报价。
        
        Args:
            product_code: 产品编码
            quantity: 数量
            market: 目标市场（影响运费）
            incoterm: FOB / CIF / EXW
            currency: USD
            margin_pct: 利润率百分比
            
        Returns:
            完整报价计算结果
        """
        # 1. 获取产品信息
        product = self.db.product_get(product_code)
        if not product:
            return {"error": f"Product {product_code} not found"}

        # 2. 获取价格
        price_record = self.get_price(product_code, market)
        base_price = price_record["base_price_usd"] if price_record else 0

        # 3. 计算
        unit_price = round(base_price * (1 + margin_pct / 100), 2)
        total_usd = round(unit_price * quantity, 2)

        # 4. 重量和体积
        unit_weight = product.get("weight_kg", 0) or 0
        total_weight = round(unit_weight * quantity, 2)

        # 体积计算（如果产品有尺寸）
        length_m = (product.get("length_cm", 0) or 0) / 100
        width_m = (product.get("head_width_cm", 0) or 0) / 100
        height_m = 0  # no height column on products table; use 0 as default
        unit_cbm = round(length_m * width_m * height_m, 6)
        total_cbm = round(unit_cbm * quantity, 4)

        # 5. 装柜量
        loading = self.calculate_loading(product_code, quantity)

        # 6. 运费估算（CIF需要）
        freight_estimate = {}
        if incoterm == "CIF":
            freight_estimate = self.estimate_freight(total_cbm, market)

        return {
            "product_code": product_code,
            "product_name": product.get("product_name_en", ""),
            "quantity": quantity,
            "base_price_usd": base_price,
            "margin_pct": margin_pct,
            "unit_price_usd": unit_price,
            "total_usd": total_usd,
            "unit_weight_kg": unit_weight,
            "total_weight_kg": total_weight,
            "unit_cbm": unit_cbm,
            "total_cbm": total_cbm,
            "incoterm": incoterm,
            "currency": currency,
            "loading": loading,
            "freight_estimate": freight_estimate,
        }

    def calculate_loading(self, product_code: str, quantity: int) -> dict:
        """
        计算装柜量。
        
        Returns:
            {"20ft": {"qty": N, "utilization": X%}, "40ft": ..., "40hq": ...}
        """
        product = self.db.product_get(product_code)
        if not product:
            return {}

        # 尝试使用数据库中的预计算值
        db_20 = product.get("loading_qty_20ft")
        db_40 = product.get("loading_qty_40ft")
        db_hq = product.get("loading_qty_40hq")

        if db_20 and db_40 and db_hq:
            return {
                "20ft": {
                    "per_container": db_20,
                    "containers_needed": max(1, -(-quantity // db_20)),  # 向上取整
                },
                "40ft": {
                    "per_container": db_40,
                    "containers_needed": max(1, -(-quantity // db_40)),
                },
                "40hq": {
                    "per_container": db_hq,
                    "containers_needed": max(1, -(-quantity // db_hq)),
                },
            }

        # 动态计算
        length_m = (product.get("length_cm", 50) or 50) / 100
        width_m = (product.get("head_width_cm", 30) or 30) / 100
        height_m = 0  # no height column on products table; use 0 as default
        unit_cbm = length_m * width_m * height_m

        # 简化计算：假设70%空间利用率
        utilization = 0.70
        result = {}
        for container_type, spec in CONTAINER_SPECS.items():
            usable_cbm = spec["cbm"] * utilization
            per_container = max(1, int(usable_cbm / unit_cbm)) if unit_cbm > 0 else 1
            containers_needed = max(1, -(-quantity // per_container))
            result[container_type] = {
                "per_container": per_container,
                "containers_needed": containers_needed,
                "utilization_pct": round((per_container * unit_cbm / spec["cbm"]) * 100, 1),
            }

        return result

    def estimate_freight(self, total_cbm: float, market: str = "") -> dict:
        """估算运费"""
        region = market if market in FREIGHT_RATES else "default"
        rates = FREIGHT_RATES[region]

        result = {}
        for container_type, rate_per_cbm in rates.items():
            spec = CONTAINER_SPECS[container_type]
            # 如果一个集装箱装不满，按比例计算
            containers_needed = max(1, -(-total_cbm // spec["cbm"]))
            estimated_cost = round(total_cbm * rate_per_cbm, 2)
            result[container_type] = {
                "rate_usd_per_cbm": rate_per_cbm,
                "estimated_cost_usd": estimated_cost,
                "containers_needed": containers_needed,
            }
        return result

    # ---- 批量报价 ----

    def batch_quote(
        self,
        items: list[dict],
        market: str = "",
        incoterm: str = "FOB",
        margin_pct: float = 15.0,
    ) -> dict:
        """
        批量报价。
        
        Args:
            items: [{"product_code": "GS-001", "quantity": 1000}, ...]
            
        Returns:
            {"items": [...], "total_usd": float, "total_cbm": float, "total_weight_kg": float}
        """
        results = []
        total_usd = 0
        total_cbm = 0
        total_weight = 0

        for item in items:
            calc = self.calculate_price(
                product_code=item["product_code"],
                quantity=item["quantity"],
                market=market,
                incoterm=incoterm,
                margin_pct=margin_pct,
            )
            if "error" not in calc:
                total_usd += calc["total_usd"]
                total_cbm += calc["total_cbm"]
                total_weight += calc["total_weight_kg"]
            results.append(calc)

        return {
            "items": results,
            "total_usd": round(total_usd, 2),
            "total_cbm": round(total_cbm, 4),
            "total_weight_kg": round(total_weight, 2),
            "incoterm": incoterm,
            "market": market,
        }
