"""迁移: 将 products 表的 length_cm 列替换为 color 列"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "ft_workspace.db")
print(f"数据库路径: {db_path}")

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row

# 检查SQLite版本是否支持DROP COLUMN (需要 3.35.0+)
version = conn.execute("SELECT sqlite_version()").fetchone()[0]
print(f"SQLite版本: {version}")

# 检查当前列
cols = conn.execute("PRAGMA table_info(products)").fetchall()
col_names = [c[1] for c in cols]
print(f"当前列: {col_names}")

has_length = "length_cm" in col_names
has_color = "color" in col_names

if has_color:
    print("color 列已存在，跳过迁移")
elif has_length:
    # SQLite 3.35+ 支持 DROP COLUMN
    major, minor, patch = [int(x) for x in version.split(".")]
    if major > 3 or (major == 3 and minor >= 35):
        print("使用 ALTER TABLE DROP COLUMN 方式...")
        conn.execute("ALTER TABLE products ADD COLUMN color TEXT")
        conn.execute("ALTER TABLE products DROP COLUMN length_cm")
    else:
        print("SQLite版本较低，使用重建表方式...")
        # 获取所有列名(除了length_cm)
        new_cols = [c for c in col_names if c != "length_cm"]
        cols_str = ", ".join(new_cols)
        conn.execute("ALTER TABLE products RENAME TO products_old")
        # 重新建表(从schema读太麻烦，直接用旧表结构)
        conn.execute(f"""
            CREATE TABLE products (
                {', '.join(f'{c[1]} {c[2]}' + (' PRIMARY KEY AUTOINCREMENT' if c[5] else '') + (' NOT NULL' if c[3] else '') + (f" DEFAULT {c[4]}" if c[4] else '') for c in cols if c[1] != 'length_cm')}
            )
        """)
    conn.commit()
    print("迁移完成!")
else:
    print("length_cm 列不存在，直接添加 color")
    conn.execute("ALTER TABLE products ADD COLUMN color TEXT")
    conn.commit()
    print("color 列已添加")

# 验证
cols_after = conn.execute("PRAGMA table_info(products)").fetchall()
print(f"迁移后列: {[c[1] for c in cols_after]}")

conn.close()
print("Done!")
