"""
M4: AI市场研究Agent - 报告生成器
功能：输入国家+产品类别，调用LLM生成完整的市场研究报告。

AI运营视角：业务员每次开发新市场前，都要手动花2-3小时搜集信息。
这个Agent把"手动调研"变成"AI一键出报告"。
"""

import json
from datetime import datetime
from typing import Optional

from src.core.database import FTDatabase
from src.core.llm_client import get_llm


# ============================================================
# 系统提示词：定义AI市场研究专家的角色
# ============================================================
SYSTEM_PROMPT = """You are an expert market research analyst specializing in 
manual farm tools and garden tools (shovels, hoes, rakes, pickaxes, garden tools).
You have deep knowledge of:
- Agricultural markets in Africa, South Asia, and Southeast Asia
- International trade regulations and import requirements
- Competitive landscape of Chinese vs Indian vs European tool manufacturers
- Pricing strategies for developing markets

Always provide specific, actionable data. When uncertain, clearly state the 
confidence level. Structure your analysis in markdown format."""


# ============================================================
# 报告生成提示词模板
# ============================================================
REPORT_PROMPT = """Generate a comprehensive market research report for:
- Target Country: {country}
- Product Category: {product_category}
{extra_context}

Please structure the report with these exact sections (in English):

# {country} — {product_category} Market Report

## 1. Market Overview
- Population, GDP, agricultural sector percentage
- Main agricultural regions
- Estimated market size for manual farm tools

## 2. Agriculture Profile
- Main crop types
- Farming methods (mechanization level)
- Small-scale vs large farm ratio
- Seasonal demand patterns

## 3. Common Tool Types
- Most commonly used tools in this market
- Preference characteristics (weight, material, handle type)
- Price sensitivity level

## 4. Product Preferences
- European vs Asian style preference
- Heavy-duty vs lightweight preference
- Wooden handle vs fiberglass vs steel handle
- Packaging preferences

## 5. Import Situation
- Major importing countries (China, India, Europe)
- Tariff policies
- Certification requirements
- Major ports and logistics

## 6. Competitive Landscape
- Major local brands
- Chinese brand presence
- Indian brand presence
- Price range comparison

## 7. Market Entry Recommendations
- Recommended product line
- Pricing strategy
- Distribution channel suggestions
- Risk warnings

Provide specific numbers, percentages, and examples wherever possible."""


# ============================================================
# 知识提取提示词模板
# ============================================================
KNOWLEDGE_PROMPT = """Extract key market knowledge points from this report about {country}.

Return a JSON array of knowledge entries. Each entry should have:
- "category": one of "agriculture", "import", "competitor", "pricing", "distribution"
- "knowledge": a specific, actionable insight (1-2 sentences)
- "source": "ai_generated"

Example format:
[
    {{"category": "agriculture", "knowledge": "Kenya's smallholder farms account for 75% of agricultural output, with avg farm size 0.2-3 hectares.", "source": "ai_generated"}},
    {{"category": "pricing", "knowledge": "Chinese shovels are preferred in Kenya at $3-5 FOB vs $6-8 for Indian alternatives.", "source": "ai_generated"}}
]

Return ONLY the JSON array, no other text."""


class MarketResearchAgent:
    """AI市场研究Agent - 自动生成目标市场研究报告"""

    def __init__(self, db: Optional[FTDatabase] = None):
        """
        初始化市场研究Agent。
        
        Args:
            db: 数据库实例，不传则自动创建
        """
        self.db = db or FTDatabase()
        self.llm = get_llm(scenario="market_research")

    def generate_report(
        self,
        country: str,
        product_category: str = "Manual Farm Tools",
        extra_context: str = "",
    ) -> dict:
        """
        生成市场研究报告。
        
        Args:
            country: 目标国家
            product_category: 产品类别（默认手动农具）
            extra_context: 额外上下文信息
            
        Returns:
            {
                "country": str,
                "product_category": str,
                "report_title": str,
                "full_report": str (markdown),
                "summary": str (200字摘要),
                "confidence": str (high/medium/low),
                "knowledge_entries": list[dict],
                "db_id": int (数据库记录ID)
            }
        """
        # 1. 构建提示词
        prompt = REPORT_PROMPT.format(
            country=country,
            product_category=product_category,
            extra_context=extra_context,
        )

        # 2. 调用LLM生成报告
        full_report = self.llm.chat(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT,
            max_tokens=4096,
            temperature=0.7,
        )

        # 3. 生成摘要
        summary = self._generate_summary(full_report, country)

        # 4. 提取知识点
        knowledge_entries = self._extract_knowledge(full_report, country)

        # 5. 确定置信度
        confidence = self._assess_confidence(full_report)

        # 6. 构建报告标题
        report_title = f"{country} — {product_category} Market Report"

        # 7. 存入数据库
        record = {
            "country": country,
            "product_category": product_category,
            "report_title": report_title,
            "summary": summary,
            "full_report": full_report,
            "report_file": None,
            "data_sources": json.dumps(["ai_generated"]),
            "confidence": confidence,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        columns = ", ".join(record.keys())
        placeholders = ", ".join(["?"] * len(record))
        sql = f"INSERT INTO market_reports ({columns}) VALUES ({placeholders})"
        cursor = self.db.execute(sql, tuple(record.values()))
        self.db.commit()
        db_id = cursor.lastrowid

        # 8. 知识点入库
        self._store_knowledge(knowledge_entries, country)

        return {
            "country": country,
            "product_category": product_category,
            "report_title": report_title,
            "full_report": full_report,
            "summary": summary,
            "confidence": confidence,
            "knowledge_entries": knowledge_entries,
            "db_id": db_id,
        }

    def _generate_summary(self, report: str, country: str) -> str:
        """生成200字摘要"""
        prompt = f"""Summarize this {country} market report in 2-3 sentences 
(max 200 words). Focus on the most actionable insights for a Chinese farm 
tools exporter.

Report:
{report[:3000]}

Return ONLY the summary text, no headers or labels."""
        
        return self.llm.chat(prompt=prompt, max_tokens=300, temperature=0.3)

    def _extract_knowledge(self, report: str, country: str) -> list[dict]:
        """从报告中提取结构化知识点"""
        prompt = KNOWLEDGE_PROMPT.format(country=country) + f"\n\nReport:\n{report[:3000]}"
        
        try:
            result = self.llm.generate_json(prompt=prompt)
            if isinstance(result, list):
                return result
            return []
        except Exception:
            return []

    def _store_knowledge(self, entries: list[dict], country: str) -> int:
        """将知识点存入market_knowledge表"""
        count = 0
        for entry in entries:
            try:
                record = {
                    "country": country,
                    "category": entry.get("category", "general"),
                    "knowledge": entry.get("knowledge", ""),
                    "source": entry.get("source", "ai_generated"),
                    "verified": 0,
                    "created_at": datetime.now().isoformat(),
                }
                columns = ", ".join(record.keys())
                placeholders = ", ".join(["?"] * len(record))
                sql = f"INSERT INTO market_knowledge ({columns}) VALUES ({placeholders})"
                self.db.execute(sql, tuple(record.values()))
                count += 1
            except Exception:
                continue
        self.db.commit()
        return count

    def _assess_confidence(self, report: str) -> str:
        """评估报告置信度"""
        # 简单启发式：包含具体数字=高置信度，模糊描述=低置信度
        import re
        numbers = len(re.findall(r'\d+\.?\d*%', report))
        has_specific = any(w in report.lower() for w in [
            "according to", "data shows", "statistics", "report indicates"
        ])
        
        if numbers >= 5 and has_specific:
            return "high"
        elif numbers >= 2:
            return "medium"
        else:
            return "low"

    def get_report(self, report_id: int) -> Optional[dict]:
        """获取已生成的报告"""
        return self.db.fetchone(
            "SELECT * FROM market_reports WHERE id = ?",
            (report_id,)
        )

    def list_reports(
        self,
        country: Optional[str] = None,
        limit: int = 20,
    ) -> list[dict]:
        """列出市场报告"""
        sql = "SELECT id, country, product_category, report_title, summary, confidence, created_at FROM market_reports WHERE 1=1"
        params = []
        if country:
            sql += " AND country = ?"
            params.append(country)
        sql += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        return self.db.fetchall(sql, tuple(params))

    def get_knowledge(
        self,
        country: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 50,
    ) -> list[dict]:
        """获取市场知识库"""
        sql = "SELECT * FROM market_knowledge WHERE 1=1"
        params = []
        if country:
            sql += " AND country = ?"
            params.append(country)
        if category:
            sql += " AND category = ?"
            params.append(category)
        sql += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        return self.db.fetchall(sql, tuple(params))
