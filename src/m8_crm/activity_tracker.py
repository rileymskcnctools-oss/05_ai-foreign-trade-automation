"""
M8: 跟进记录追踪器
功能：记录每一次客户沟通（邮件/WhatsApp/电话/会议），支持跟进提醒。
"""

from datetime import datetime, timedelta
from typing import Optional

from src.core.database import FTDatabase


class ActivityTracker:
    """客户跟进活动追踪器"""

    ACTIVITY_TYPES = ["email", "whatsapp", "linkedin", "call", "meeting", "other"]
    DIRECTIONS = ["outbound", "inbound"]
    STATUSES = ["sent", "replied", "no_reply", "meeting_scheduled", "cancelled"]

    def __init__(self, db: Optional[FTDatabase] = None):
        self.db = db or FTDatabase()

    def log(
        self,
        client_id: int,
        activity_type: str,
        direction: str = "outbound",
        subject: str = "",
        content: str = "",
        status: str = "sent",
        follow_up_date: Optional[str] = None,
        notes: str = "",
    ) -> int:
        """
        记录一条跟进活动。
        
        Args:
            client_id: 客户ID
            activity_type: email / whatsapp / linkedin / call / meeting / other
            direction: outbound(发出) / inbound(收到)
            subject: 邮件主题/沟通摘要
            content: 消息内容
            status: sent / replied / no_reply / meeting_scheduled
            follow_up_date: 下次跟进日期 (ISO格式)
            notes: 备注
            
        Returns:
            活动记录ID
        """
        now = datetime.now().isoformat()
        record = {
            "client_id": client_id,
            "activity_type": activity_type,
            "direction": direction,
            "subject": subject,
            "content": content,
            "status": status,
            "scheduled_date": None,
            "actual_date": now,
            "follow_up_date": follow_up_date,
            "notes": notes,
            "created_at": now,
        }

        columns = ", ".join(record.keys())
        placeholders = ", ".join(["?"] * len(record))
        cursor = self.db.execute(
            f"INSERT INTO activities ({columns}) VALUES ({placeholders})",
            tuple(record.values())
        )

        # 同时更新客户的 updated_at 和 last_activity 字段
        self.db.execute(
            "UPDATE clients SET updated_at = ? WHERE id = ?",
            (now, client_id)
        )
        self.db.commit()

        return cursor.lastrowid

    def get_activities(
        self,
        client_id: int,
        activity_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        """获取客户的所有跟进记录"""
        sql = "SELECT * FROM activities WHERE client_id = ?"
        params = [client_id]
        if activity_type:
            sql += " AND activity_type = ?"
            params.append(activity_type)
        sql += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        return self.db.fetchall(sql, tuple(params))

    def get_latest(self, client_id: int) -> Optional[dict]:
        """获取客户最近一次跟进记录"""
        result = self.db.fetchone(
            "SELECT * FROM activities WHERE client_id = ? ORDER BY created_at DESC LIMIT 1",
            (client_id,)
        )
        return result

    def days_since_contact(self, client_id: int) -> Optional[int]:
        """计算距上次联系的天数"""
        latest = self.get_latest(client_id)
        if not latest or not latest.get("actual_date"):
            return None
        try:
            last_date = datetime.fromisoformat(latest["actual_date"])
            return (datetime.now() - last_date).days
        except (ValueError, TypeError):
            return None

    def timeline(self, client_id: int, limit: int = 20) -> list[dict]:
        """获取客户沟通时间线"""
        return self.db.fetchall(
            """SELECT activity_type, direction, subject, status, 
                      actual_date, follow_up_date, notes
               FROM activities 
               WHERE client_id = ?
               ORDER BY actual_date DESC
               LIMIT ?""",
            (client_id, limit)
        )

    def get_pending_follow_ups(self, days_ahead: int = 7) -> list[dict]:
        """
        获取需要跟进的客户。
        
        Args:
            days_ahead: 未来N天内需要跟进的客户
        """
        today = datetime.now().strftime("%Y-%m-%d")
        future = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

        return self.db.fetchall("""
            SELECT a.client_id, c.company_name, c.country, c.grade,
                   a.activity_type, a.subject, a.follow_up_date,
                   a.created_at as last_activity_date
            FROM activities a
            JOIN clients c ON a.client_id = c.id
            WHERE a.follow_up_date BETWEEN ? AND ?
              AND a.id IN (
                  SELECT MAX(id) FROM activities 
                  WHERE client_id = a.client_id
              )
            ORDER BY a.follow_up_date ASC
        """, (today, future))

    def overdue_follow_ups(self) -> list[dict]:
        """获取已过期未跟进的客户"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.db.fetchall("""
            SELECT a.client_id, c.company_name, c.country, c.grade,
                   a.activity_type, a.subject, a.follow_up_date,
                   a.created_at as last_activity_date
            FROM activities a
            JOIN clients c ON a.client_id = c.id
            WHERE a.follow_up_date < ?
              AND a.id IN (
                  SELECT MAX(id) FROM activities 
                  WHERE client_id = a.client_id
              )
            ORDER BY a.follow_up_date ASC
        """, (today,))

    def activity_stats(self, client_id: Optional[int] = None) -> dict:
        """活动统计"""
        if client_id:
            sql = "SELECT activity_type, COUNT(*) as cnt FROM activities WHERE client_id = ? GROUP BY activity_type"
            rows = self.db.fetchall(sql, (client_id,))
        else:
            sql = "SELECT activity_type, COUNT(*) as cnt FROM activities GROUP BY activity_type"
            rows = self.db.fetchall(sql)

        stats = {r["activity_type"]: r["cnt"] for r in rows}

        # 总数
        if client_id:
            total = self.db.fetchone(
                "SELECT COUNT(*) as cnt FROM activities WHERE client_id = ?", (client_id,)
            )
        else:
            total = self.db.fetchone("SELECT COUNT(*) as cnt FROM activities")

        stats["total"] = total["cnt"] if total else 0
        return stats
