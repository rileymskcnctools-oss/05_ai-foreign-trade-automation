# m9_analytics package
"""
M9: 数据运营分析中心 (Data Analytics)
提供产品、客户、市场三个维度的数据分析和仪表盘数据。

组件:
    - product_analytics: 产品维度分析
    - client_analytics: 客户维度分析
    - market_analytics: 市场维度分析
    - dashboard_data: 仪表盘数据聚合
"""
from .product_analytics import ProductAnalytics
from .client_analytics import ClientAnalytics
from .market_analytics import MarketAnalytics
from .dashboard_data import DashboardData

__all__ = ["ProductAnalytics", "ClientAnalytics", "MarketAnalytics", "DashboardData"]
