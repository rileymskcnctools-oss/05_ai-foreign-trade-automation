# m4_market_research package
"""
M4: AI市场研究Agent (Market Research Agent)
输入国家+产品，自动生成市场研究报告。

组件:
    - report_generator: 生成市场研究报告
    - knowledge_extractor: 提取知识点并入库
"""
from .report_generator import MarketResearchAgent

__all__ = ["MarketResearchAgent"]
