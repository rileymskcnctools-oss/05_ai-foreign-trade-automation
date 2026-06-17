"""查看产品箱规数据"""
from src.core.database import FTDatabase
db = FTDatabase()
rows = db.execute(
    "SELECT product_code, product_name_en, qty_per_carton, carton_size_cm, gw_per_carton_kg "
    "FROM products LIMIT 10"
).fetchall()
for r in rows:
    print(dict(r))
