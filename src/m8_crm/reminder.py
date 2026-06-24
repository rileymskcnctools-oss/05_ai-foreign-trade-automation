"""
M8: 跟进提醒管理器
功能：基于跟进日期自动提醒，支持逾期检测和批量提醒。
"""

from datetime import datetime, timedelta
from typing import Optional

from src.core.database import FTDatabase


class FollowUpReminder:
    """跟进提醒管理器"""

    def __init__(self, db: Optional[FTDatabase] = None):
        self.db = db or FTDatabase()

    def get_pending(self, days_ahead: int = 7) -> list[dict]:
        """
        获取未来N天内需要跟进的客户。
        
        Returns:
            客户跟进提醒列表，包含客户信息和最近活动
        """
        today = datetime.now().strftime("%Y-%m-%d")
        future = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

        return self.db.fetchall("""
            SELECT 
                c.id as client_id,
                c.company_name,
                c.country,
                c.grade,
                c.status as client_status,
                c.contact_person,
                c.email,
                c.whatsapp,
                a.activity_type as last_type,
                a.subject as last_subject,
                a.follow_up_date,
                a.created_at as last_contact_date,
                CAST(julianday(a.follow_up_date) - julianday('now') AS INTEGER) as days_until
            FROM activities a
            JOIN clients c ON a.client_id = c.id
            WHERE a.follow_up_date BETWEEN ? AND ?
              AND a.follow_up_date >= ?
              AND c.status NOT IN ('lost', 'customer')
              AND a.id = (
                  SELECT MAX(id) FROM activities 
                  WHERE client_id = a.client_id
              )
            ORDER BY a.follow_up_date ASC
        """, (today, future, today))

    def get_overdue(self) -> list[dict]:
        """获取已过期未跟进的客户"""
        today = datetime.now().strftime("%Y-%m-%d")

        return self.db.fetchall("""
            SELECT 
                c.id as client_id,
                c.company_name,
                c.country,
                c.grade,
                c.status as client_status,
                c.contact_person,
                c.email,
                c.whatsapp,
                a.activity_type as last_type,
                a.subject as last_subject,
                a.follow_up_date,
                a.created_at as last_contact_date,
                CAST(julianday('now') - julianday(a.follow_up_date) AS INTEGER) as overdue_days
            FROM activities a
            JOIN clients c ON a.client_id = c.id
            WHERE a.follow_up_date < ?
              AND c.status NOT IN ('lost', 'customer')
              AND a.id = (
                  SELECT MAX(id) FROM activities 
                  WHERE client_id = a.client_id
              )
            ORDER BY a.follow_up_date ASC
        """, (today,))

    def get_no_activity(self, days_inactive: int = 30) -> list[dict]:
        """获取超过N天没有任何活动的客户"""
        cutoff = (datetime.now() - timedelta(days=days_inactive)).isoformat()

        return self.db.fetchall("""
            SELECT 
                c.id as client_id,
                c.company_name,
                c.country,
                c.grade,
                c.status as client_status,
                c.contact_person,
                c.email,
                MAX(a.created_at) as last_contact_date,
                CAST(julianday('now') - julianday(MAX(a.created_at)) AS INTEGER) as inactive_days
            FROM clients c
            LEFT JOIN activities a ON c.id = a.client_id
            WHERE c.status NOT IN ('lost', 'customer')
            GROUP BY c.id
            HAVING MAX(a.created_at) IS NULL OR MAX(a.created_at) < ?
            ORDER BY inactive_days DESC
        """, (cutoff,))

    def reminder_summary(self) -> dict:
        """获取提醒概览"""
        overdue = self.get_overdue()
        upcoming_3d = self.get_pending(days_ahead=3)
        upcoming_7d = self.get_pending(days_ahead=7)
        stale = self.get_no_activity(days_inactive=30)

        return {
            "overdue_count": len(overdue),
            "overdue_clients": overdue[:10],  # 最多展示10条
            "upcoming_3_days": upcoming_3d,
            "upcoming_7_days_count": len(upcoming_7d),
            "stale_clients_count": len(stale),
            "stale_clients": stale[:10],
        }

    def schedule_next_follow_up(
        self,
        client_id: int,
        activity_id: int,
        next_date: str,
    ) -> bool:
        """
        更新跟进日期。
        
        Args:
            client_id: 客户ID
            activity_id: 活动ID
            next_date: 下次跟进日期 (ISO格式)
        """
        self.db.execute(
            "UPDATE activities SET follow_up_date = ? WHERE id = ? AND client_id = ?",
            (next_date, activity_id, client_id)
        )
        self.db.commit()
        return True
