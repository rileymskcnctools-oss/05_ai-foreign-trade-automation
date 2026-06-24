# m7_quotation package
"""
M7: AI报价辅助 (Quotation Assistant)
价格计算、装柜量、报价单生成。

组件:
    - calculator: 价格计算和装柜量
    - email_generator: 报价邮件生成
"""
from .calculator import PriceCalculator
from .email_generator import QuotationEmailGenerator

__all__ = ["PriceCalculator", "QuotationEmailGenerator"]
