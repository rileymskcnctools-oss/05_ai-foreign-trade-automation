"""
FT Workspace v2.0 - 核心数据中央保险箱
功能：专门负责安全地存放和调取外贸系统的所有数据（产品、客户、询盘、报价）。

AI运营视角：这是AI的“大后方仓库”。AI生成邮件或分析客户时，都需要从这里调取原材料。
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import Optional


class FTDatabase:
    """外贸数字化工作台的【中央数据总管】"""

    def __init__(self, db_path: Optional[str] = None):
        """
        【第一步：打开账本】连接或创建一个数据仓库。
        业务场景：系统刚启动时，AI要先找到账本放在哪。
        """
        if db_path is None:
            # 自动定位：不管你在谁的电脑上运行，自动找到项目根目录
            project_root = self._find_project_root()
            # 默认把账本文件存放在 data 文件夹下的 ft_workspace.db
            db_path = os.path.join(project_root, "data", "ft_workspace.db")

         # 如果 data 文件夹不存在，系统会自动在电脑里创建这个文件夹
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        
        # 【运营保障】：开启“快车道”模式。
        # 效果：当AI在后台批量轰炸式写入一万条询盘时，前台业务员查产品依然流畅，不卡顿。
        self.conn.execute("PRAGMA journal_mode=WAL")  
        
        # 【运营保障】：开启“红线绑定”约束。
        # 效果：防止员工把报价单发给一个“根本不存在的垃圾客户”，保证公司数据资产100%正确。
        self.conn.execute("PRAGMA foreign_keys=ON")

    @staticmethod
    def _find_project_root() -> str:
        """
        【路径自适应 GPS】自动寻找电脑里项目的根目录。
        运营价值：告别写死路径（如 C:/Users/Admin...），换电脑运行代码绝不报错。
        """
        current = os.path.dirname(os.path.abspath(__file__))
        while current != os.path.dirname(current):
            if os.path.isdir(os.path.join(current, "src")):
                return current
            current = os.path.dirname(current)
        return os.getcwd()

    def init_schema(self, schema_path: Optional[str] = None) -> None:
        """
        【搭建毛坯房】第一次建立数据库时，按照说明书（schema.sql）把各个抽屉格子建好。
        """
        if schema_path is None:
            project_root = self._find_project_root()
            schema_path = os.path.join(project_root, "data", "schema.sql")

        with open(schema_path, "r", encoding="utf-8") as f:
            sql = f.read()

        self.conn.executescript(sql)
        self.conn.commit()

    # ---- 下面4个是底层的“搬砖”工具函数，AI数据运营只需要知道它们是干嘛的，不用管怎么写 ----

    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        """跑一趟腿：去仓库里执行一次指定的命令（比如修改、删除）"""
        return self.conn.execute(sql, params)

    def executemany(self, sql: str, params_list: list) -> sqlite3.Cursor:
        """大货车拉货：一次性执行好几条同样的命令（比如批量录入100个产品）"""
        return self.conn.executemany(sql, params_list)

    def fetchone(self, sql: str, params: tuple = ()) -> Optional[dict]:
        """精准取件：去仓库里只拿【一条】特定的数据（比如查某一个特定客户的邮箱）"""
        cursor = self.conn.execute(sql, params)
        row = cursor.fetchone()
        return dict(row) if row else None # 要么返回一个字典，要么返回 None（空）

    def fetchall(self, sql: str, params: tuple = ()) -> list[dict]:
        """打包取件：把符合条件的一堆数据【全拿出来】（比如把所有“美国”的客户都列出来）"""
        cursor = self.conn.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()] # 返回一个字典列表，每个字典代表一行数据

    def commit(self) -> None:
        """点确认键：把刚才对数据的修改真正保存到硬盘里（类似按 Ctrl + S）"""
        self.conn.commit()

    def close(self) -> None:
        """锁上库门：下班关闭数据库连接，释放电脑内存"""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """【安全防摔锁】如果代码中途断电或者报错，系统会自动把没存好的数据回滚，然后安全锁门"""
        if exc_type is None:
            self.commit()
        self.close()

    # ============================================================
    # 模块一：产品中心（AI生成素材的原材料库）
    # ============================================================

    def product_count(self) -> int:
        """运营看板：获取当前仓库里总共有多少款产品"""
        result = self.fetchone("SELECT COUNT(*) as cnt FROM products")
        return result["cnt"] if result else 0

    def product_get(self, product_code: str) -> Optional[dict]:
        """【AI核心调用点】：输入一个产品编码（如 GS-001），把它的长宽高、材质、价格全拿出来。
        业务场景：AI要写一封产品推广信，先用这个函数把产品参数喂给AI。
        """
        return self.fetchone(
            "SELECT * FROM products WHERE product_code = ?",
            (product_code,)
        )

    def product_list(
        self,
        category: Optional[str] = None,
        status: Optional[str] = "active",
        limit: int = 100,
        offset: int = 0
    ) -> list[dict]:
        """筛选目录：按分类（比如：园林剪刀）或者状态（在售），批量拉出产品清单"""
        sql = "SELECT * FROM products WHERE 1=1"
        params = []

        if category:
            sql += " AND category = ?"
            params.append(category)

        if status:
            sql += " AND status = ?"
            params.append(status)

        sql += " ORDER BY product_code LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        return self.fetchall(sql, tuple(params))

    def product_search(self, query: str, limit: int = 20) -> list[dict]:
        """【极速模糊搜索】：业务员输入“钢材”，系统横跨产品编码、中英文名、SEO关键词一秒找出结果。
        业务场景：应对客户在即时通讯（WhatsApp）上的突发提问。
        """
        pattern = f"%{query}%"
        return self.fetchall(
            """SELECT * FROM products
               WHERE product_code LIKE ?
                  OR product_name_en LIKE ?
                  OR product_name_cn LIKE ?
                  OR target_keywords LIKE ?
               ORDER BY product_code
               LIMIT ?""",
            (pattern, pattern, pattern, pattern, limit)
        )

    def product_insert(self, product: dict) -> bool:
        """动态录入：把一个产品字典塞进数据库，如果编码重复了，就直接更新覆盖。
        运营价值：以后产品表就算增加新的列（如最少起订量 MOQ），这行代码自动适应，不用重写！
        """
        columns = ", ".join(product.keys())
        placeholders = ", ".join(["?"] * len(product))
        sql = f"INSERT OR REPLACE INTO products ({columns}) VALUES ({placeholders})"
        try:
            self.execute(sql, tuple(product.values()))
            return True
        except sqlite3.Error as e:
            print(f"录入产品 {product.get('product_code', '?')} 失败，原因: {e}")
            return False

    def product_insert_many(self, products: list[dict]) -> dict:
        """批量大导入：一键把从各大展会或独立站爬取下来的几百个产品导入系统，并报告成功和失败的名字"""
        success = 0
        errors = []
        for p in products:
            if self.product_insert(p):
                success += 1
            else:
                errors.append(p.get("product_code", "unknown"))
        self.commit()
        return {"success": success, "errors": errors}

    # ============================================================
    # 模块二：客户资产（公司最核心的客户画像库）
    # ============================================================

    def client_count(self) -> int:
        """运营看板：看看目前公海和私域里一共积累了多少个核心客户"""
        result = self.fetchone("SELECT COUNT(*) as cnt FROM clients")
        return result["cnt"] if result else 0

    def client_create(self, client: dict) -> Optional[int]:
        """新客户登记：AI从领英（LinkedIn）或展会名片上识别出新客户后，自动将其打入档案库，返回客户系统编号"""
        columns = ", ".join(client.keys())
        placeholders = ", ".join(["?"] * len(client))
        sql = f"INSERT INTO clients ({columns}) VALUES ({placeholders})"
        cursor = self.execute(sql, tuple(client.values()))
        self.commit()
        return cursor.lastrowid

    def client_get(self, client_id: int) -> Optional[dict]:
        """查阅客户档案：根据系统分配的客户编号，调出该客人的全部背景资料（如国家、邮箱）"""
        return self.fetchone(
            "SELECT * FROM clients WHERE id = ?",
            (client_id,)
        )

    def client_search(self, query: str, limit: int = 20) -> list[dict]:
        """模糊找客户：输入“美国”或某个买家名字，瞬间找出对应客人的所有联系方式"""
        pattern = f"%{query}%"
        return self.fetchall(
            """SELECT * FROM clients
               WHERE company_name LIKE ?
                  OR country LIKE ?
                  OR contact_person LIKE ?
                  OR email LIKE ?
               ORDER BY company_name
               LIMIT ?""",
            (pattern, pattern, pattern, pattern, limit)
        )

    # ============================================================
    # 模块三：跟进记录（SaaS系统的行为漏斗数据）
    # ============================================================

    def activity_log(self, client_id: int, activity: dict) -> Optional[int]:
        """【AI自动痕迹记录】：AI每帮业务员给客户发完一封邮件，或者发送了一条WhatsApp，自动在本种群写下记录。
        运营价值：谁什么时候干了什么，一目了然，再也不用人工写跟进日志。
        """
        activity["client_id"] = client_id
        if "created_at" not in activity:
            activity["created_at"] = datetime.now().isoformat()
        columns = ", ".join(activity.keys())
        placeholders = ", ".join(["?"] * len(activity))
        sql = f"INSERT INTO activities ({columns}) VALUES ({placeholders})"
        cursor = self.execute(sql, tuple(activity.values()))
        self.commit()
        return cursor.lastrowid

    def activity_list(self, client_id: int, limit: int = 50) -> list[dict]:
        """跟进流水线：把某个客户过去半年的所有联系痕迹，按时间倒序（最新的在最上面）全部拉出来"""
        return self.fetchall(
            "SELECT * FROM activities WHERE client_id = ? ORDER BY created_at DESC LIMIT ?",
            (client_id, limit)
        )

    # ============================================================
    # 模块四：报价单（成交前的临门一脚数据）
    # ============================================================

    def quotation_create(self, quotation: dict) -> Optional[str]:
        """
        【流水号自动发放机】：自动生成绝对不撞车的、正规企业报价单号。
        业务逻辑：系统去数一数今年发了多少份报价，如果是第5份，自动拼出 `QT-2026-0005`。
        运营价值：避免两个业务员手写出同一个单号，导致财务对账和发货彻底打架。
        """
        if "quotation_no" not in quotation:
            count = self.fetchone("SELECT COUNT(*) as cnt FROM quotations")
            seq = (count["cnt"] if count else 0) + 1
            year = datetime.now().strftime("%Y")
            quotation["quotation_no"] = f"QT-{year}-{seq:04d}"

        if "created_at" not in quotation:
            quotation["created_at"] = datetime.now().isoformat()

        columns = ", ".join(quotation.keys())
        placeholders = ", ".join(["?"] * len(quotation))
        sql = f"INSERT INTO quotations ({columns}) VALUES ({placeholders})"
        self.execute(sql, tuple(quotation.values()))
        self.commit()
        return quotation["quotation_no"]

    # ============================================================
    # 模块五：数据看板与大后方安全备份
    # ============================================================

    def stats_summary(self) -> dict:
        """
        【老板最爱的运营大屏数据】：一键吐出全公司的核心运营指标。
        数据产出：产品总数、客户总数、活跃商品数、总跟进次数、总报价单数、总询盘数。
        运营价值：直接拿这些数字去对接 BI 看板，作为每周汇报的数据来源。
        """
        return {
            "products": self.product_count(),
            "clients": self.client_count(),
            "active_products": self.fetchone(
                "SELECT COUNT(*) as cnt FROM products WHERE status='active'"
            )["cnt"],
            "total_activities": self.fetchone(
                "SELECT COUNT(*) as cnt FROM activities"
            )["cnt"],
            "total_quotations": self.fetchone(
                "SELECT COUNT(*) as cnt FROM quotations"
            )["cnt"],
            "total_inquiries": self.fetchone(
                "SELECT COUNT(*) as cnt FROM inquiries"
            )["cnt"],
        }

    def backup(self, backup_path: Optional[str] = None) -> str:
        """
        【防离职变卖、防病毒的核心盾牌】：零中断数据热备份。
        业务逻辑：先把账本锁上一秒钟，复制一个副本到 backups 文件夹，并贴上当时的时间戳，再瞬间解锁。
        运营价值：做数据资产管理的底线！即便公司电脑中勒索病毒、或者员工恶意删库，一键提取昨天的副本，1秒全盘复原。
        """
        if backup_path is None:
            project_root = self._find_project_root()
            backup_dir = os.path.join(project_root, "data", "backups")
            os.makedirs(backup_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"ft_workspace_{timestamp}.db")

        import shutil
        self.conn.close()  # 备份前先安全断开，防止损坏
        shutil.copy2(self.db_path, backup_path)  # 物理复制账本文件
        
        # 复制完后立刻悄悄重连，前台业务员根本感觉不到系统刚才停顿了
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA foreign_keys=ON")

        return backup_path

    def __del__(self):
        """【下班随手关灯机制】当程序彻底关闭时，确保连接不会死锁，安全退出"""
        try:
            if hasattr(self, "conn") and self.conn:
                self.conn.close()
        except Exception:
            pass