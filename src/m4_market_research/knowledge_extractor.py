"""
M4: 市场知识提取器
功能：从市场报告中提取结构化知识点，支持分类检索和知识积累。
"""

import json
import re
from datetime import datetime
from typing import Optional

from src.core.database import FTDatabase
from src.core.llm_client import get_llm


EXTRACT_PROMPT = """Analyze this market research content and extract specific, 
actionable knowledge points for a Chinese manual farm tools exporter.

Content:
{content}

Return a JSON array of knowledge entries. Each entry:
- "category": one of "agriculture", "import", "competitor", "pricing", "distribution", "regulation"
- "knowledge": specific insight (1-2 sentences, factual)
- "source": reference or origin

Example:
[
    {{"category": "agriculture", "knowledge": "Liberia has 70% smallholder farmers with avg 1-2 hectare farms.", "source": "market_analysis"}},
    {{"category": "pricing", "knowledge": "Garden hoe FOB price range: $2.50-4.50 for African markets.", "source": "trade_data"}}
]

Return ONLY the JSON array."""


class KnowledgeExtractor:
    """从文本中提取市场知识点"""

    def __init__(self, db: Optional[FTDatabase] = None):
        self.db = db or FTDatabase()
        self.llm = get_llm(scenario="market_research")

    def extract_and_store(
        self,
        text: str,
        country: str,
        source: str = "ai_generated",
    ) -> list[dict]:
        """
        从文本中提取知识点并存入数据库。
        
        Returns:
            提取并存储的知识点列表
        """
        prompt = EXTRACT_PROMPT.format(content=text[:4000])

        try:
            entries = self.llm.generate_json(prompt=prompt)
            if not isinstance(entries, list):
                return []
        except Exception:
            return []

        stored = []
        for entry in entries:
            record = {
                "country": country,
                "category": entry.get("category", "general"),
                "knowledge": entry.get("knowledge", ""),
                "source": source,
                "verified": 0,
                "created_at": datetime.now().isoformat(),
            }
            columns = ", ".join(record.keys())
            placeholders = ", ".join(["?"] * len(record))
            sql = f"INSERT INTO market_knowledge ({columns}) VALUES ({placeholders})"
            self.db.execute(sql, tuple(record.values()))
            stored.append(record)

        self.db.commit()
        return stored

    def search_knowledge(
        self,
        country: Optional[str] = None,
        category: Optional[str] = None,
        keyword: Optional[str] = None,
        limit: int = 50,
    ) -> list[dict]:
        """搜索市场知识库"""
        sql = "SELECT * FROM market_knowledge WHERE 1=1"
        params = []
        if country:
            sql += " AND country = ?"
            params.append(country)
        if category:
            sql += " AND category = ?"
            params.append(category)
        if keyword:
            sql += " AND knowledge LIKE ?"
            params.append(f"%{keyword}%")
        sql += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        return self.db.fetchall(sql, tuple(params))

    def get_country_summary(self, country: str) -> dict:
        """获取某国市场知识摘要"""
        rows = self.db.fetchall(
            "SELECT category, COUNT(*) as cnt FROM market_knowledge WHERE country = ? GROUP BY category",
            (country,)
        )
        return {row["category"]: row["cnt"] for row in rows}

    def verify_knowledge(self, knowledge_id: int) -> bool:
        """标记知识点为已验证"""
        self.db.execute(
            "UPDATE market_knowledge SET verified = 1 WHERE id = ?",
            (knowledge_id,)
        )
        self.db.commit()
        return True
