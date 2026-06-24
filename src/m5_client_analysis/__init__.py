# m5_client_analysis package
"""
M5: AI客户分析Agent (Client Analysis Agent)
分析潜在客户，自动评级并给出跟进策略。

组件:
    - grader: 客户评级打分
    - advisor: 跟进策略建议
"""
from .grader import ClientGrader
from .advisor import ClientAdvisor

__all__ = ["ClientGrader", "ClientAdvisor"]
