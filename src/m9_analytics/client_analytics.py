"""
M9: 客户维度分析
功能：客户评级分布、国家分布、转化率、活动统计。
"""

from typing import Optional

from src.core.database import FTDatabase


class ClientAnalytics:
    """客户数据分析"""

    def __init__(self, db: Optional[FTDatabase] = None):
        self.db = db or FTDatabase()

    def overview(self) -> dict:
        """客户概览"""
        total = self.db.fetchone("SELECT COUNT(*) as cnt FROM clients")["cnt"]
        by_status = self.db.fetchall(
            "SELECT status, COUNT(*) as cnt FROM clients GROUP BY status ORDER BY cnt DESC"
        )
        by_grade = self.db.fetchall(
            "SELECT grade, COUNT(*) as cnt FROM clients WHERE grade IS NOT NULL GROUP BY grade ORDER BY cnt DESC"
        )
        avg_score = self.db.fetchone(
            "SELECT AVG(grade_score) as avg FROM clients WHERE grade_score IS NOT NULL"
        )

        return {
            "total_clients": total,
            "by_status": [{"status": s["status"], "count": s["cnt"]} for s in by_status],
            "by_grade": [{"grade": g["grade"], "count": g["cnt"]} for g in by_grade],
            "avg_score": round(avg_score["avg"] or 0, 1),
        }

    def country_distribution(self, limit: int = 15) -> list[dict]:
        """国家分布"""
        return self.db.fetchall(
            """SELECT country, COUNT(*) as client_count, 
                      AVG(grade_score) as avg_score,
                      GROUP_CONCAT(DISTINCT grade) as grades
               FROM clients 
               WHERE country IS NOT NULL
               GROUP BY country ORDER BY client_count DESC LIMIT ?""",
            (limit,)
        )

    def grade_distribution(self) -> list[dict]:
        """评级分布"""
        return self.db.fetchall(
            """SELECT grade, COUNT(*) as count,
                      AVG(grade_score) as avg_score
               FROM clients 
               WHERE grade IS NOT NULL
               GROUP BY grade ORDER BY grade"""
        )

    def status_funnel(self) -> list[dict]:
        """客户状态漏斗"""
        stages = [
            "lead", "contacted", "interested", "quoted", 
            "negotiating", "customer", "lost"
        ]
        result = []
        for stage in stages:
            row = self.db.fetchone(
                "SELECT COUNT(*) as cnt FROM clients WHERE status = ?", (stage,)
            )
            result.append({"stage": stage, "count": row["cnt"]})
        
        # 计算转化率
        for i in range(1, len(result)):
            prev = result[i - 1]["count"]
            curr = result[i]["count"]
            result[i]["conversion_rate"] = round(curr / prev * 100, 1) if prev > 0 else 0
        
        return result

    def activity_stats(self) -> dict:
        """客户活动统计"""
        total_activities = self.db.fetchone(
            "SELECT COUNT(*) as cnt FROM activities"
        )["cnt"]
        
        by_type = self.db.fetchall(
            """SELECT activity_type, COUNT(*) as cnt 
               FROM activities GROUP BY activity_type ORDER BY cnt DESC"""
        )
        
        by_direction = self.db.fetchall(
            """SELECT direction, COUNT(*) as cnt 
               FROM activities GROUP BY direction"""
        )
        
        # 最近7天活动
        recent_7d = self.db.fetchone(
            """SELECT COUNT(*) as cnt FROM activities 
               WHERE created_at >= datetime('now', '-7 days')"""
        )["cnt"]

        # 无活动客户数
        inactive_30d = self.db.fetchone(
            """SELECT COUNT(*) as cnt FROM clients c
               WHERE c.status NOT IN ('lost', 'customer')
               AND (SELECT MAX(created_at) FROM activities WHERE client_id = c.id) 
                   < datetime('now', '-30 days')
               OR NOT EXISTS (SELECT 1 FROM activities WHERE client_id = c.id)"""
        )["cnt"]

        return {
            "total_activities": total_activities,
            "by_type": [{"type": t["activity_type"], "count": t["cnt"]} for t in by_type],
            "by_direction": [{"dir": d["direction"], "count": d["cnt"]} for d in by_direction],
            "recent_7d": recent_7d,
            "inactive_30d": inactive_30d,
        }

    def top_clients(self, limit: int = 10, order_by: str = "score") -> list[dict]:
        """Top客户排行"""
        order = {
            "score": "c.grade_score DESC",
            "activity": "(SELECT COUNT(*) FROM activities WHERE client_id = c.id) DESC",
            "recent": "(SELECT MAX(COALESCE(actual_date, created_at)) FROM activities WHERE client_id = c.id) DESC NULLS LAST",
        }.get(order_by, "c.grade_score DESC")

        return self.db.fetchall(
            f"""SELECT c.id, c.company_name, c.country, c.grade, c.grade_score, c.status,
                       c.contact_person, c.email,
                       (SELECT MAX(COALESCE(a.actual_date, a.created_at)) FROM activities a WHERE a.client_id = c.id) as last_contact_date
                FROM clients c
                WHERE c.status != 'lost'
                ORDER BY {order}
                LIMIT ?""",
            (limit,)
        )

    def score_distribution(self) -> list[dict]:
        """评分分布"""
        ranges = [
            ("0-20", 0, 20),
            ("20-40", 20, 40),
            ("40-60", 40, 60),
            ("60-80", 60, 80),
            ("80-100", 80, 100),
        ]
        result = []
        for label, low, high in ranges:
            row = self.db.fetchone(
                "SELECT COUNT(*) as cnt FROM clients WHERE grade_score >= ? AND grade_score < ?",
                (low, high)
            )
            result.append({"range": label, "count": row["cnt"]})
        return result
