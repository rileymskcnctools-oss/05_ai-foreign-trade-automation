"""
M5: 客户评级器
功能：根据多维度信息对潜在客户进行A/B/C评级。

评级维度：
- 业务匹配度：客户主营产品与我们的匹配程度
- 采购能力：客户规模和预计采购量
- 市场覆盖：客户覆盖的市场范围
- 在线可见度：是否有网站、社交媒体
"""

import json
from datetime import datetime
from typing import Optional

from src.core.database import FTDatabase
from src.core.llm_client import get_llm


GRADING_PROMPT = """You are a B2B sales analyst for a Chinese manual farm tools company 
(shovels, hoes, rakes, pickaxes, garden tools).

Analyze this potential client and provide a grade and score.

Client Information:
- Company: {company_name}
- Country: {country}
- Website: {website}
- Business Type: {business_type}
- Main Products: {main_products}
- Market Regions: {market_regions}
- Estimated Volume: {estimated_volume}
- Source: {source}
{extra_info}

Grade the client on these dimensions (each 1-10):
1. Product Match: How well do our farm tools fit their product line?
2. Purchasing Power: Size and buying capacity
3. Market Reach: Geographic coverage
4. Online Presence: Website, social media visibility

Return JSON:
{{
    "product_match": {{"score": 8, "reason": "..."}},
    "purchasing_power": {{"score": 7, "reason": "..."}},
    "market_reach": {{"score": 6, "reason": "..."}},
    "online_presence": {{"score": 7, "reason": "..."}},
    "total_score": 70,
    "grade": "B+",
    "summary": "One paragraph summary of the client assessment"
}}

Grade scale:
- A (80-100): Large importer/wholesaler, high match, strong procurement needs
- B (60-79): Medium distributor, decent match, may have procurement needs
- C (40-59): Small retailer, moderate match, uncertain procurement
- D (below 40): Poor match, unlikely buyer

Return ONLY the JSON object."""


class ClientGrader:
    """客户评级器 - 多维度评估潜在客户"""

    def __init__(self, db: Optional[FTDatabase] = None):
        self.db = db or FTDatabase()
        self.llm = get_llm(scenario="client_analysis")

    def grade_client(self, client_id: int) -> dict:
        """
        对指定客户进行评级。
        
        Args:
            client_id: 客户ID
            
        Returns:
            评级结果字典，包含各维度评分和总分
        """
        # 1. 获取客户信息
        client = self.db.fetchone(
            "SELECT * FROM clients WHERE id = ?", (client_id,)
        )
        if not client:
            return {"error": f"Client {client_id} not found"}

        return self._grade_from_info(dict(client))

    def grade_from_info(self, client_info: dict) -> dict:
        """
        根据提供的客户信息进行评级（不需要已在数据库中）。
        
        Args:
            client_info: 客户信息字典
            
        Returns:
            评级结果
        """
        return self._grade_from_info(client_info)

    def _grade_from_info(self, client: dict) -> dict:
        """内部评级逻辑"""
        # 构建提示词
        prompt = GRADING_PROMPT.format(
            company_name=client.get("company_name", "Unknown"),
            country=client.get("country", "Unknown"),
            website=client.get("website", "N/A"),
            business_type=client.get("business_type", "N/A"),
            main_products=client.get("main_products", "N/A"),
            market_regions=client.get("market_regions", "N/A"),
            estimated_volume=client.get("estimated_volume", "N/A"),
            source=client.get("source", "N/A"),
            extra_info=f"\nNotes: {client.get('notes', 'N/A')}" if client.get("notes") else "",
        )

        # 调用LLM
        try:
            result = self.llm.generate_json(
                prompt=prompt,
                system_prompt="You are a B2B client grading expert. Return valid JSON only.",
            )
        except Exception as e:
            result = {
                "product_match": {"score": 5, "reason": "Unable to assess"},
                "purchasing_power": {"score": 5, "reason": "Unable to assess"},
                "market_reach": {"score": 5, "reason": "Unable to assess"},
                "online_presence": {"score": 5, "reason": "Unable to assess"},
                "total_score": 50,
                "grade": "C",
                "summary": f"Auto-grading failed: {str(e)}",
            }

        # 2. 如果客户已在数据库中，更新评级
        client_id = client.get("id")
        if client_id:
            self.db.execute(
                """UPDATE clients 
                   SET grade = ?, grade_score = ?, updated_at = ?
                   WHERE id = ?""",
                (result.get("grade", "C"), result.get("total_score", 50),
                 datetime.now().isoformat(), client_id)
            )
            self.db.commit()

            # 3. 记录分析历史
            analysis = {
                "client_id": client_id,
                "analysis_type": "initial",
                "summary": result.get("summary", ""),
                "full_analysis": json.dumps(result, ensure_ascii=False),
                "grade_suggested": result.get("grade", "C"),
                "recommendations": "",
                "created_at": datetime.now().isoformat(),
            }
            columns = ", ".join(analysis.keys())
            placeholders = ", ".join(["?"] * len(analysis))
            self.db.execute(
                f"INSERT INTO client_analyses ({columns}) VALUES ({placeholders})",
                tuple(analysis.values())
            )
            self.db.commit()

        return result

    def batch_grade(self, client_ids: list[int]) -> list[dict]:
        """批量评级"""
        results = []
        for cid in client_ids:
            results.append(self.grade_client(cid))
        return results

    def get_grading_history(self, client_id: int) -> list[dict]:
        """获取客户的评级历史"""
        return self.db.fetchall(
            "SELECT * FROM client_analyses WHERE client_id = ? ORDER BY created_at DESC",
            (client_id,)
        )
