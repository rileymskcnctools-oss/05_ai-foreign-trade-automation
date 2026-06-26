"""
M9: 市场维度分析
功能：市场报告统计、国家市场分析、趋势追踪。
"""

from typing import Optional

from src.core.database import FTDatabase


class MarketAnalytics:
    """市场数据分析"""

    def __init__(self, db: Optional[FTDatabase] = None):
        self.db = db or FTDatabase()

    def overview(self) -> dict:
        """市场概览"""
        total_reports = self.db.fetchone(
            "SELECT COUNT(*) as cnt FROM market_reports"
        )["cnt"]
        
        by_country = self.db.fetchall(
            """SELECT country, COUNT(*) as report_count
               FROM market_reports 
               GROUP BY country ORDER BY report_count DESC"""
        )
        
        by_product_category = self.db.fetchall(
            """SELECT product_category, COUNT(*) as cnt 
               FROM market_reports GROUP BY product_category ORDER BY cnt DESC"""
        )

        return {
            "total_reports": total_reports,
            "by_country": [
                {"country": c["country"], "reports": c["report_count"]}
                for c in by_country
            ],
            "by_category": [{"category": t["product_category"], "count": t["cnt"]} for t in by_product_category],
        }

    def country_detail(self, country: str) -> dict:
        """国家市场详情"""
        # 市场报告
        reports = self.db.fetchall(
            """SELECT id, report_title, summary, created_at
               FROM market_reports WHERE country = ?
               ORDER BY created_at DESC LIMIT 5""",
            (country,)
        )
        
        # 该国客户
        clients = self.db.fetchall(
            """SELECT COUNT(*) as total, grade,
                      AVG(grade_score) as avg_score
               FROM clients WHERE country = ?
               GROUP BY grade""",
            (country,)
        )
        
        # 该国产品覆盖
        products = self.db.fetchone(
            "SELECT COUNT(DISTINCT product_code) as cnt FROM products WHERE target_markets LIKE ?",
            (f"%{country}%",)
        )

        # 摘要
        knowledge = self.db.fetchall(
            """SELECT knowledge, category, created_at
               FROM market_knowledge 
               WHERE country = ?
               ORDER BY created_at DESC LIMIT 10""",
            (country,)
        )

        return {
            "country": country,
            "reports": reports,
            "clients_by_grade": clients,
            "products_covered": products["cnt"],
            "market_knowledge": knowledge,
        }

    def market_coverage(self) -> list[dict]:
        """市场覆盖分析（按客户国家）"""
        return self.db.fetchall(
            """SELECT country,
                      COUNT(*) as client_count
               FROM clients
               WHERE country IS NOT NULL AND country != ''
               GROUP BY country ORDER BY client_count DESC"""
        )

    def competitive_landscape(self) -> list[dict]:
        """产品分类统计（替代竞争格局分析）"""
        return self.db.fetchall(
            """SELECT category,
                      COUNT(*) as product_count,
                      COUNT(DISTINCT color) as color_count,
                      AVG(weight_kg) as avg_weight
               FROM products WHERE status='active'
               GROUP BY category ORDER BY product_count DESC"""
        )

    def knowledge_trends(self, country: Optional[str] = None, limit: int = 20) -> list[dict]:
        """市场知识趋势"""
        sql = "SELECT * FROM market_knowledge"
        params = []
        if country:
            sql += " WHERE country = ?"
            params.append(country)
        sql += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        return self.db.fetchall(sql, tuple(params))
