"""
FT Workspace v3.0 — 依赖注入模块
避免 main.py 和 routes 之间的循环导入
"""
from src.core.database import FTDatabase

_db_instance = None

def get_db() -> FTDatabase:
    """获取数据库连接 (单例模式)
    每次调用前 rollback 释放残留锁，防止 'database is locked' 错误。
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = FTDatabase()
    # 释放可能的残留事务锁
    try:
        _db_instance.conn.rollback()
    except Exception:
        pass
    return _db_instance
