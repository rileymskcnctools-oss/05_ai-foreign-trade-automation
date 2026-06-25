"""
FT Workspace v3.0 — 依赖注入模块
避免 main.py 和 routes 之间的循环导入
"""
from src.core.database import FTDatabase

_db_instance = None

def get_db() -> FTDatabase:
    """获取数据库连接 (单例模式)"""
    global _db_instance
    if _db_instance is None:
        _db_instance = FTDatabase()
    return _db_instance
