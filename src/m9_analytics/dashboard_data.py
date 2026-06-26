"""
M9: 仪表盘数据聚合
功能：汇总所有维度的数据，为Streamlit前端提供统一的数据接口。
"""

from typing import Optional

from src.core.database import FTDatabase
from .product_analytics import ProductAnalytics
from .client_analytics import ClientAnalytics
from .market_analytics import MarketAnalytics


class DashboardData:
    """仪表盘数据聚合器"""

    def __init__(self, db: Optional[FTDatabase] = None):
        self.db = db or FTDatabase()
        self.products = ProductAnalytics(db)
        self.clients = ClientAnalytics(db)
        self.markets = MarketAnalytics(db)

    def home_data(self) -> dict:
        """首页仪表盘数据"""
        product_overview = self.products.overview()
        client_overview = self.clients.overview()
        market_overview = self.markets.overview()
        activity = self.clients.activity_stats()

        return {
            "products": {
                "total": product_overview["total_products"],
                "categories": product_overview["categories"],
                "unique_colors": product_overview["unique_colors"],
            },
            "clients": {
                "total": client_overview["total_clients"],
                "by_status": client_overview["by_status"],
                "by_grade": client_overview["by_grade"],
                "avg_score": client_overview["avg_score"],
            },
            "market": {
                "total_reports": market_overview["total_reports"],
                "top_countries": market_overview["by_country"][:5],
            },
            "activity": {
                "recent_7d": activity["recent_7d"],
                "inactive_30d": activity["inactive_30d"],
            },
        }

    def products_page(self) -> dict:
        """产品分析页数据"""
        return {
            "overview": self.products.overview(),
            "category_distribution": self.products.category_distribution(),
            "length_distribution": self.products.length_distribution(),
            "seo_coverage": self.products.seo_coverage(),
            "top_products": self.products.top_products(),
            "loading_capacity": self.products.loading_capacity(),
        }

    def clients_page(self) -> dict:
        """客户分析页数据"""
        return {
            "overview": self.clients.overview(),
            "country_distribution": self.clients.country_distribution(),
            "grade_distribution": self.clients.grade_distribution(),
            "status_funnel": self.clients.status_funnel(),
            "activity_stats": self.clients.activity_stats(),
            "top_clients": self.clients.top_clients(),
            "score_distribution": self.clients.score_distribution(),
        }

    def markets_page(self) -> dict:
        """市场分析页数据"""
        return {
            "overview": self.markets.overview(),
            "coverage": self.markets.market_coverage(),
            "competitive_landscape": self.markets.competitive_landscape(),
        }

    def market_detail_page(self, country: str) -> dict:
        """国家市场详情页数据"""
        return {
            "detail": self.markets.country_detail(country),
            "coverage": self.markets.market_coverage(),
        }

    def pipeline_summary(self) -> dict:
        """销售漏斗概览"""
        funnel = self.clients.status_funnel()
        
        # 报价统计
        quotation_stats = self.db.fetchone(
            """SELECT 
                 COUNT(*) as total,
                 SUM(CASE WHEN status='sent' THEN 1 ELSE 0 END) as sent,
                 SUM(CASE WHEN status='accepted' THEN 1 ELSE 0 END) as accepted,
                 SUM(CASE WHEN status='rejected' THEN 1 ELSE 0 END) as rejected,
                 SUM(CASE WHEN status='sent' THEN total_amount ELSE 0 END) as total_sent_usd,
                 SUM(CASE WHEN status='accepted' THEN total_amount ELSE 0 END) as total_accepted_usd
               FROM quotations"""
        )

        return {
            "funnel": funnel,
            "quotations": dict(quotation_stats) if quotation_stats else {},
        }

    def quick_stats(self) -> dict:
        """快速统计卡片"""
        products = self.db.fetchone("SELECT COUNT(*) as cnt FROM products WHERE status='active'")
        clients = self.db.fetchone("SELECT COUNT(*) as cnt FROM clients")
        quotations = self.db.fetchone("SELECT COUNT(*) as cnt FROM quotations")
        reports = self.db.fetchone("SELECT COUNT(*) as cnt FROM market_reports")
        activities = self.db.fetchone(
            "SELECT COUNT(*) as cnt FROM activities WHERE created_at >= datetime('now', '-7 days')"
        )

        return {
            "active_products": products["cnt"],
            "total_clients": clients["cnt"],
            "total_quotations": quotations["cnt"],
            "market_reports": reports["cnt"],
            "weekly_activities": activities["cnt"],
        }
