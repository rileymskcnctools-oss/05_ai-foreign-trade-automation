"""
M8: 客户管理器 - 客户全生命周期管理
功能：客户录入、查询、状态流转、数据更新。
"""

from datetime import datetime
from typing import Optional

from src.core.database import FTDatabase


class ClientManager:
    """客户CRM管理器"""

    # 客户状态流转：prospect -> contacted -> negotiating -> customer / lost
    STATUS_FLOW = {
        "prospect": ["contacted", "lost"],
        "contacted": ["negotiating", "lost"],
        "negotiating": ["customer", "contacted", "lost"],
        "customer": ["lost"],
        "lost": ["prospect"],  # 可以重新激活
    }

    def __init__(self, db: Optional[FTDatabase] = None):
        self.db = db or FTDatabase()

    # ---- CRUD ----

    def create(self, data: dict) -> int:
        """
        新建客户。返回客户ID。
        
        Args:
            data: 客户信息字典，必填 company_name
        """
        now = datetime.now().isoformat()
        data.setdefault("status", "prospect")
        data.setdefault("created_at", now)
        data.setdefault("updated_at", now)

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        cursor = self.db.execute(
            f"INSERT INTO clients ({columns}) VALUES ({placeholders})",
            tuple(data.values())
        )
        self.db.commit()
        return cursor.lastrowid

    def get(self, client_id: int) -> Optional[dict]:
        """获取客户详情"""
        return self.db.fetchone(
            "SELECT * FROM clients WHERE id = ?", (client_id,)
        )

    def update(self, client_id: int, data: dict) -> bool:
        """更新客户信息"""
        data["updated_at"] = datetime.now().isoformat()
        sets = ", ".join(f"{k} = ?" for k in data.keys())
        params = list(data.values()) + [client_id]
        self.db.execute(
            f"UPDATE clients SET {sets} WHERE id = ?", tuple(params)
        )
        self.db.commit()
        return True

    def delete(self, client_id: int) -> bool:
        """删除客户（软删除：状态设为lost）"""
        return self.update(client_id, {"status": "lost"})

    def hard_delete(self, client_id: int) -> bool:
        """硬删除客户"""
        self.db.execute("DELETE FROM clients WHERE id = ?", (client_id,))
        self.db.commit()
        return True

    # ---- 查询 ----

    def search(self, query: str, limit: int = 20) -> list[dict]:
        """模糊搜索客户"""
        pattern = f"%{query}%"
        return self.db.fetchall(
            """SELECT * FROM clients
               WHERE company_name LIKE ? OR country LIKE ?
                  OR contact_person LIKE ? OR email LIKE ?
               ORDER BY company_name LIMIT ?""",
            (pattern, pattern, pattern, pattern, limit)
        )

    def list_all(
        self,
        status: Optional[str] = None,
        country: Optional[str] = None,
        grade: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict]:
        """列表查询，支持多条件筛选"""
        sql = "SELECT * FROM clients WHERE 1=1"
        params = []
        if status:
            sql += " AND status = ?"
            params.append(status)
        if country:
            sql += " AND country = ?"
            params.append(country)
        if grade:
            sql += " AND grade = ?"
            params.append(grade)
        sql += " ORDER BY updated_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        return self.db.fetchall(sql, tuple(params))

    def count(self, status: Optional[str] = None) -> int:
        """统计客户数量"""
        if status:
            result = self.db.fetchone(
                "SELECT COUNT(*) as cnt FROM clients WHERE status = ?", (status,)
            )
        else:
            result = self.db.fetchone("SELECT COUNT(*) as cnt FROM clients")
        return result["cnt"] if result else 0

    # ---- 状态流转 ----

    def change_status(self, client_id: int, new_status: str) -> dict:
        """
        变更客户状态，自动检查流转合法性。
        
        Returns:
            {"success": bool, "old_status": str, "new_status": str, "error": str}
        """
        client = self.get(client_id)
        if not client:
            return {"success": False, "error": "Client not found"}

        old_status = client["status"]
        allowed = self.STATUS_FLOW.get(old_status, [])

        if new_status not in allowed:
            return {
                "success": False,
                "old_status": old_status,
                "new_status": new_status,
                "error": f"Cannot transition from '{old_status}' to '{new_status}'. Allowed: {allowed}",
            }

        self.update(client_id, {"status": new_status})
        return {"success": True, "old_status": old_status, "new_status": new_status}

    # ---- 漏斗统计 ----

    def pipeline_stats(self) -> dict:
        """获取销售漏斗各阶段统计"""
        rows = self.db.fetchall(
            "SELECT status, COUNT(*) as cnt FROM clients GROUP BY status"
        )
        stats = {r["status"]: r["cnt"] for r in rows}
        stats["total"] = sum(stats.values())
        return stats

    def country_stats(self) -> list[dict]:
        """按国家统计客户分布"""
        return self.db.fetchall(
            "SELECT country, COUNT(*) as cnt FROM clients WHERE country IS NOT NULL GROUP BY country ORDER BY cnt DESC"
        )

    def recent_clients(self, days: int = 30) -> list[dict]:
        """获取最近N天新增客户"""
        return self.db.fetchall(
            """SELECT id, company_name, country, grade, status, created_at
               FROM clients WHERE created_at >= datetime('now', ?)
               ORDER BY created_at DESC""",
            (f"-{days} days",)
        )
