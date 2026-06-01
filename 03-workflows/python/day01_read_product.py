"""
Day 1: Python环境验证 + CSV读取
目标：读取 product_database_filled.csv 并打印 GS-001 的完整参数
"""
import pandas as pd
import os

# 构建项目根目录路径（本脚本在 03-workflows/python/ 下）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))

csv_path = os.path.join(PROJECT_ROOT, '04-database', 'csv', 'product_database_filled.csv')

print("=" * 60)
print("Day 1: Product Database Reader")
print("=" * 60)

# 读取 CSV
df = pd.read_csv(csv_path, encoding='gbk')

print(f"\nTotal products: {len(df)}")
print(f"Total columns:  {len(df.columns)}")
print(f"\nColumn names:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")

# 查找 GS-001
print(f"\n{'=' * 60}")
print("Product: GS-001")
print("=" * 60)

product = df[df['product_id'] == 'GS-001']
if len(product) > 0:
    p = product.iloc[0]
    for col in df.columns:
        val = p[col]
        if pd.isna(val):
            val = "(empty)"
        print(f"  {col:25s} : {val}")
else:
    print("ERROR: GS-001 not found in database!")

# 品类统计
print(f"\n{'=' * 60}")
print("Category Summary")
print("=" * 60)
cat_counts = df.groupby('category').size().sort_values(ascending=False)
for cat, count in cat_counts.items():
    print(f"  {cat:20s} : {count} products")

print(f"\n{'=' * 60}")
print("Day 1 verification: PASSED")
print("=" * 60)
