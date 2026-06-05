"""
FT Workspace v2.0 - Core Database Module
SQLite connection and operation wrapper.

Portable design: uses relative paths from project root.
Works on Windows/Mac/Linux.
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import Optional


class FTDatabase:
    """SQLite database wrapper for FT Workspace v2.0."""

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file.
                     If None, uses config default: data/ft_workspace.db
                     Relative paths are resolved from the project root.
        """
        if db_path is None:
            # Find project root (where src/ directory is)
            project_root = self._find_project_root()
            db_path = os.path.join(project_root, "data", "ft_workspace.db")

        # Ensure parent directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")  # Better concurrency
        self.conn.execute("PRAGMA foreign_keys=ON")

    @staticmethod
    def _find_project_root() -> str:
        """Find project root by looking for src/ directory."""
        current = os.path.dirname(os.path.abspath(__file__))
        # Go up from src/core/ to project root
        while current != os.path.dirname(current):
            if os.path.isdir(os.path.join(current, "src")):
                return current
            current = os.path.dirname(current)
        # Fallback: current working directory
        return os.getcwd()

    def init_schema(self, schema_path: Optional[str] = None) -> None:
        """
        Initialize database from schema.sql file.

        Args:
            schema_path: Path to schema.sql. If None, auto-detects.
        """
        if schema_path is None:
            project_root = self._find_project_root()
            schema_path = os.path.join(project_root, "data", "schema.sql")

        with open(schema_path, "r", encoding="utf-8") as f:
            sql = f.read()

        self.conn.executescript(sql)
        self.conn.commit()

    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a SQL statement."""
        return self.conn.execute(sql, params)

    def executemany(self, sql: str, params_list: list) -> sqlite3.Cursor:
        """Execute a SQL statement with multiple parameter sets."""
        return self.conn.executemany(sql, params_list)

    def fetchone(self, sql: str, params: tuple = ()) -> Optional[dict]:
        """Execute and fetch one row as dict."""
        cursor = self.conn.execute(sql, params)
        row = cursor.fetchone()
        return dict(row) if row else None

    def fetchall(self, sql: str, params: tuple = ()) -> list[dict]:
        """Execute and fetch all rows as list of dicts."""
        cursor = self.conn.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]

    def commit(self) -> None:
        """Commit current transaction."""
        self.conn.commit()

    def close(self) -> None:
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        self.close()

    # ============================================================
    # Product Operations
    # ============================================================

    def product_count(self) -> int:
        """Get total product count."""
        result = self.fetchone("SELECT COUNT(*) as cnt FROM products")
        return result["cnt"] if result else 0

    def product_get(self, product_code: str) -> Optional[dict]:
        """Get a single product by code."""
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
        """List products with optional filters."""
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

    def product_search(
        self,
        query: str,
        limit: int = 20
    ) -> list[dict]:
        """Search products by code, name, or keywords."""
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
        """Insert a single product. Returns True on success."""
        columns = ", ".join(product.keys())
        placeholders = ", ".join(["?"] * len(product))
        sql = f"INSERT OR REPLACE INTO products ({columns}) VALUES ({placeholders})"
        try:
            self.execute(sql, tuple(product.values()))
            return True
        except sqlite3.Error as e:
            print(f"Error inserting product {product.get('product_code', '?')}: {e}")
            return False

    def product_insert_many(self, products: list[dict]) -> dict:
        """Insert multiple products. Returns {success: N, errors: [...]}"""
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
    # Client Operations
    # ============================================================

    def client_count(self) -> int:
        """Get total client count."""
        result = self.fetchone("SELECT COUNT(*) as cnt FROM clients")
        return result["cnt"] if result else 0

    def client_create(self, client: dict) -> Optional[int]:
        """Create a new client. Returns client ID."""
        columns = ", ".join(client.keys())
        placeholders = ", ".join(["?"] * len(client))
        sql = f"INSERT INTO clients ({columns}) VALUES ({placeholders})"
        cursor = self.execute(sql, tuple(client.values()))
        self.commit()
        return cursor.lastrowid

    def client_get(self, client_id: int) -> Optional[dict]:
        """Get a single client by ID."""
        return self.fetchone(
            "SELECT * FROM clients WHERE id = ?",
            (client_id,)
        )

    def client_search(self, query: str, limit: int = 20) -> list[dict]:
        """Search clients by name, country, or contact."""
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
    # Activity Operations
    # ============================================================

    def activity_log(self, client_id: int, activity: dict) -> Optional[int]:
        """Log a client activity. Returns activity ID."""
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
        """List activities for a client."""
        return self.fetchall(
            "SELECT * FROM activities WHERE client_id = ? ORDER BY created_at DESC LIMIT ?",
            (client_id, limit)
        )

    # ============================================================
    # Quotation Operations
    # ============================================================

    def quotation_create(self, quotation: dict) -> Optional[str]:
        """Create a quotation. Returns quotation number."""
        if "quotation_no" not in quotation:
            # Auto-generate: QT-YYYY-NNNN
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
    # Stats & Analytics
    # ============================================================

    def stats_summary(self) -> dict:
        """Get overall system statistics."""
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

    # ============================================================
    # Backup
    # ============================================================

    def backup(self, backup_path: Optional[str] = None) -> str:
        """Backup database file."""
        if backup_path is None:
            project_root = self._find_project_root()
            backup_dir = os.path.join(project_root, "data", "backups")
            os.makedirs(backup_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"ft_workspace_{timestamp}.db")

        import shutil
        # Close connection before backup
        self.conn.close()
        shutil.copy2(self.db_path, backup_path)
        # Reopen connection
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA foreign_keys=ON")

        return backup_path

    def __del__(self):
        """Ensure connection is closed on garbage collection."""
        try:
            if hasattr(self, "conn") and self.conn:
                self.conn.close()
        except Exception:
            pass
