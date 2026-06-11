import os
import pandas as pd
import sqlite3

# 1. 定位路径
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "04-database","csv","product_database_filled.csv") # 请确保CSV和本脚本在同一文件夹下，或者改成你真实的CSV路径
db_path = os.path.join(base_dir, "data", "ft_workspace.db")

print(f"🔍 检查CSV是否存在: {os.path.exists(csv_path)}")
print(f"🔍 检查数据库路径: {db_path}")

try:
    # 2. 读取你提供给我的完美CSV文件
    df = pd.read_csv(csv_path, encoding="gbk")
    
    # 3. 强行连接并全量覆盖数据库中的 products 表
    conn = sqlite3.connect(db_path)
    
    # if_exists='replace' 会把原来残缺或错误的表直接删掉，根据CSV的表头重新建表并灌入数据！
    df.to_sql("products", conn, if_exists="replace", index=False)
    conn.close()
    
    print("✅ 【大功告成】数据库已被真实CSV全量覆盖！列名现在绝对像素级一致了！")
    
except Exception as e:
    print(f"❌ 刷新失败，请检查路径或编码: {e}")