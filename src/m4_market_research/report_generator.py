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
SYSTEM_PROMPT = """你是一位资深的外贸市场研究分析师，专注于手动农具和园艺工具（锄头、铲子、耙子、十字镐、园艺工具等）领域。
你深入了解以下领域：
- 非洲、南亚、东南亚的农业市场
- 国际贸易法规和进口要求
- 中国 vs 印度 vs 欧洲工具制造商的竞争格局
- 发展中国家的定价策略

请始终提供具体、可操作的数据。不确定时请明确说明置信度。
请用中文输出报告，但专业术语可保留英文。使用 Markdown 格式。"""


# ============================================================
# 报告生成提示词模板
# ============================================================
REPORT_PROMPT = """请生成一份完整的市场研究报告（当前日期：{current_date}）：

重要：请使用你所知的最新数据（2024-2026年），如果不确定具体年份，请注明"截至最新数据"。
报告中的所有数据、统计、趋势都应尽可能反映2024年以后的情况。

- 目标国家：{country}
- 产品类别：{product_category}
{extra_context}

请按以下结构输出报告（用中文）：

# {country} — {product_category} 市场研究报告

## 1. 市场概况
- 人口、GDP、农业占GDP比例
- 主要农业产区
- 手动农具市场规模估算

## 2. 农业特征
- 主要农作物
- 耕作方式（机械化程度）
- 小农户 vs 大农场比例
- 季节性需求规律

## 3. 常用工具类型
- 该市场最常用的农具
- 偏好特征（重量、材质、手柄类型）
- 价格敏感度

## 4. 产品偏好
- 欧式 vs 亚洲风格偏好
- 重型 vs 轻型偏好
- 木柄 vs 玻纤柄 vs 钢管柄
- 包装偏好

## 5. 进口情况
- 主要进口来源国（中国、印度、欧洲）
- 关税政策
- 认证要求
- 主要港口和物流

## 6. 竞争格局
- 主要本地品牌
- 中国品牌渗透率
- 印度品牌渗透率
- 价格区间对比

## 7. 市场进入建议
- 推荐产品线
- 定价策略
- 分销渠道建议
- 风险提示

请尽量提供具体数字、百分比和实例。"""


# ============================================================
# 知识提取提示词模板
# ============================================================
KNOWLEDGE_PROMPT = """从这份关于{country}的市场报告中提取关键知识点。

请返回一个JSON数组。每个条目包含：
- "category": 以下之一 "agriculture", "import", "competitor", "pricing", "distribution"
- "knowledge": 一条具体、可操作的知识点（用中文，1-2句话）
- "source": "ai_generated"

示例格式：
[
    {{"category": "agriculture", "knowledge": "肯尼亚75%的农业产出来自小农户，平均农场面积0.2-3公顷。", "source": "ai_generated"}},
    {{"category": "pricing", "knowledge": "中国铲子在肯尼亚市场FOB价$3-5，印度产品$6-8，中国产品价格优势明显。", "source": "ai_generated"}}
]

只返回JSON数组，不要其他文字。"""


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
        use_web_research: bool = True,
    ) -> dict:
        """
        生成市场研究报告。
        
        Args:
            country: 目标国家
            product_category: 产品类别（默认手动农具）
            extra_context: 额外上下文信息
            use_web_research: 是否启用实时网络数据采集
            
        Returns:
            {
                "country": str,
                "product_category": str,
                "report_title": str,
                "full_report": str (markdown),
                "summary": str (200字摘要),
                "confidence": str (high/medium/low),
                "knowledge_entries": list[dict],
                "db_id": int (数据库记录ID),
                "web_research": str (采集到的实时数据)
            }
        """
        # 0. 实时网络数据采集
        web_context = ""
        data_sources = ["ai_generated"]
        if use_web_research:
            try:
                from src.m4_market_research.web_researcher import research_country_market
                web_context = research_country_market(country, product_category)
                if web_context:
                    data_sources.append("web_search")
            except Exception as e:
                print(f"[WebResearch] 采集失败: {e}")

        # 1. 构建提示词（注入实时数据 + 当前日期）
        from datetime import date
        prompt = REPORT_PROMPT.format(
            current_date=date.today().strftime("%Y年%m月%d日"),
            country=country,
            product_category=product_category,
            extra_context=f"{extra_context}\n\n{web_context}" if extra_context else web_context,
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
            "data_sources": json.dumps(data_sources),
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
            "web_research": web_context[:500] if web_context else None,
            "data_sources": data_sources,
        }

    def _generate_summary(self, report: str, country: str) -> str:
        """生成200字摘要"""
        prompt = f"""请用2-3句中文总结这份{country}市场报告（不超过200字）。
重点关注对中国农具出口商最有价值的信息。

报告内容：
{report[:3000]}

只返回摘要文本，不要标题或标签。"""
        
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
