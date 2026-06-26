"""
M9: 产品维度分析（已修正，匹配实际products表结构）
功能：产品分类分布、规格统计、表面处理分布、认证统计。
"""

from typing import Optional

from src.core.database import FTDatabase


class ProductAnalytics:
    """产品数据分析"""

    def __init__(self, db: Optional[FTDatabase] = None):
        self.db = db or FTDatabase()

    def overview(self) -> dict:
        """产品概览统计"""
        total = self.db.fetchone("SELECT COUNT(*) as cnt FROM products WHERE status='active'")["cnt"]
        categories = self.db.fetchall(
            "SELECT category, COUNT(*) as cnt FROM products WHERE status='active' GROUP BY category ORDER BY cnt DESC"
        )
        color_count = self.db.fetchone(
            "SELECT COUNT(DISTINCT color) as color_count FROM products WHERE color IS NOT NULL AND color != '' AND status='active'"
        )
        avg_weight = self.db.fetchone(
            "SELECT AVG(weight_kg) as avg_wt FROM products WHERE weight_kg > 0 AND status='active'"
        )
        return {
            "total_products": total,
            "categories": [{"name": c["category"], "count": c["cnt"]} for c in categories],
            "unique_colors": color_count["color_count"] or 0,
            "avg_weight_kg": round(avg_weight["avg_wt"] or 0, 2),
        }

    def category_distribution(self) -> list[dict]:
        """分类分布"""
        return self.db.fetchall(
            """SELECT category, COUNT(*) as product_count,
                      COUNT(DISTINCT color) as color_count,
                      AVG(weight_kg) as avg_weight
               FROM products WHERE status='active'
               GROUP BY category ORDER BY product_count DESC"""
        )

    def material_distribution(self) -> list[dict]:
        """材质分布"""
        return self.db.fetchall(
            """SELECT material, COUNT(*) as cnt
               FROM products WHERE status='active' AND material IS NOT NULL
               GROUP BY material ORDER BY cnt DESC"""
        )

    def surface_treatment_distribution(self) -> list[dict]:
        """表面处理分布"""
        return self.db.fetchall(
            """SELECT surface_treatment, COUNT(*) as cnt
               FROM products WHERE status='active' AND surface_treatment IS NOT NULL
               GROUP BY surface_treatment ORDER BY cnt DESC"""
        )

    def certification_stats(self) -> list[dict]:
        """认证统计"""
        return self.db.fetchall(
            """SELECT certification, COUNT(*) as cnt
               FROM products WHERE status='active' AND certification IS NOT NULL AND certification != ''
               GROUP BY certification ORDER BY cnt DESC"""
        )

    def handle_material_distribution(self) -> list[dict]:
        """手柄材质分布"""
        return self.db.fetchall(
            """SELECT handle_material, COUNT(*) as cnt
               FROM products WHERE status='active' AND handle_material IS NOT NULL
               GROUP BY handle_material ORDER BY cnt DESC"""
        )

    def color_distribution(self) -> list[dict]:
        """颜色分布"""
        return self.db.fetchall(
            """SELECT color, COUNT(*) as cnt
               FROM products WHERE status='active' AND color IS NOT NULL AND color != ''
               GROUP BY color ORDER BY cnt DESC"""
        )

    def top_products(self, limit: int = 10) -> list[dict]:
        """产品列表（按最近更新）"""
        return self.db.fetchall(
            """SELECT product_code, product_name_en, product_name_cn,
                      category, material, color, weight_kg
               FROM products WHERE status='active'
               ORDER BY updated_at DESC LIMIT ?""",
            (limit,)
        )

    def seo_coverage(self) -> dict:
        """SEO覆盖率"""
        total = self.db.fetchone("SELECT COUNT(*) as cnt FROM products WHERE status='active'")["cnt"]
        with_seo = self.db.fetchone(
            "SELECT COUNT(*) as cnt FROM products WHERE status='active' AND (seo_title_1 IS NOT NULL AND seo_title_1 != '')"
        )["cnt"]
        with_selling = self.db.fetchone(
            "SELECT COUNT(*) as cnt FROM products WHERE status='active' AND (selling_points IS NOT NULL AND selling_points != '')"
        )["cnt"]
        with_whatsapp = self.db.fetchone(
            "SELECT COUNT(*) as cnt FROM products WHERE status='active' AND (whatsapp_script IS NOT NULL AND whatsapp_script != '')"
        )["cnt"]

        return {
            "total": total,
            "with_seo_titles": with_seo,
            "with_selling_points": with_selling,
            "with_whatsapp_script": with_whatsapp,
            "seo_pct": round(with_seo / total * 100, 1) if total > 0 else 0,
        }

    def loading_capacity(self) -> list[dict]:
        """装柜量统计"""
        return self.db.fetchall(
            """SELECT product_code, product_name_en, 
                      loading_qty_20ft, loading_qty_40ft, loading_qty_40hq
               FROM products WHERE status='active' 
                 AND loading_qty_20ft IS NOT NULL
               ORDER BY loading_qty_40ft DESC LIMIT 20"""
        )
