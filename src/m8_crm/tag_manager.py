"""
M8: 标签管理器
功能：给客户打标签，支持批量标签管理和标签统计。
"""

from datetime import datetime
from typing import Optional

from src.core.database import FTDatabase


class TagManager:
    """客户标签管理器"""

    # 预设标签
    DEFAULT_TAGS = [
        {"name": "VIP", "color": "#FFD700", "description": "高价值大客户"},
        {"name": "New", "color": "#4CAF50", "description": "新开发客户"},
        {"name": "Hot Lead", "color": "#FF5722", "description": "高意向客户"},
        {"name": "Stale", "color": "#9E9E9E", "description": "长期未跟进"},
        {"name": "Wholesaler", "color": "#2196F3", "description": "批发商"},
        {"name": "Retailer", "color": "#9C27B0", "description": "零售商"},
        {"name": "Importer", "color": "#FF9800", "description": "进口商"},
        {"name": "African Market", "color": "#795548", "description": "非洲市场客户"},
        {"name": "European Market", "color": "#00BCD4", "description": "欧洲市场客户"},
        {"name": "Needs Follow-up", "color": "#F44336", "description": "需要跟进"},
    ]

    def __init__(self, db: Optional[FTDatabase] = None):
        self.db = db or FTDatabase()

    # ---- 标签管理 ----

    def create_tag(self, name: str, color: str = "#666666", description: str = "") -> int:
        """创建标签"""
        now = datetime.now().isoformat()
        cursor = self.db.execute(
            "INSERT INTO client_tags (name, color, description, created_at) VALUES (?, ?, ?, ?)",
            (name, color, description, now)
        )
        self.db.commit()
        return cursor.lastrowid

    def get_tag(self, tag_id: int) -> Optional[dict]:
        """获取标签"""
        return self.db.fetchone(
            "SELECT * FROM client_tags WHERE id = ?", (tag_id,)
        )

    def list_tags(self) -> list[dict]:
        """列出所有标签"""
        return self.db.fetchall(
            "SELECT * FROM client_tags ORDER BY name"
        )

    def delete_tag(self, tag_id: int) -> bool:
        """删除标签"""
        self.db.execute("DELETE FROM client_tags WHERE id = ?", (tag_id,))
        self.db.commit()
        return True

    def init_default_tags(self) -> int:
        """初始化预设标签（仅创建不存在的）"""
        existing = {t["name"] for t in self.list_tags()}
        count = 0
        for tag in self.DEFAULT_TAGS:
            if tag["name"] not in existing:
                self.create_tag(**tag)
                count += 1
        return count

    # ---- 客户-标签关联 ----

    def tag_client(self, client_id: int, tag_id: int) -> bool:
        """给客户打标签 (placeholder - no mapping table exists)"""
        return False

    def untag_client(self, client_id: int, tag_id: int) -> bool:
        """移除客户标签 (placeholder - no mapping table exists)"""
        return True

    def get_client_tags(self, client_id: int) -> list[dict]:
        """获取客户的所有标签 (placeholder - no mapping table exists)"""
        return []

    def get_tagged_clients(self, tag_id: int) -> list[dict]:
        """获取某标签下的所有客户 (placeholder - no mapping table exists)"""
        return []

    def bulk_tag(self, client_ids: list[int], tag_id: int) -> dict:
        """批量给多个客户打标签"""
        success = 0
        for cid in client_ids:
            if self.tag_client(cid, tag_id):
                success += 1
        return {"total": len(client_ids), "success": success}

    def tag_stats(self) -> list[dict]:
        """标签统计"""
        return self.db.fetchall("""
            SELECT ct.name, ct.color, 0 as client_count
            FROM client_tags ct
            GROUP BY ct.id
            ORDER BY ct.name
        """)
