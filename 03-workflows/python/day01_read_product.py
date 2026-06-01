import pandas as pd
import os
#获取当前脚本的目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
#获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))

#构建CSV文件路径
csv_path = os.path.join(
    PROJECT_ROOT,
    '04-database',
    'csv',
    'product_database_filled.csv'
)

if not os.path.exists(csv_path):
    print(f"文件不存在: {csv_path}")
    exit()

#读取CSV文件,注意编码格式
df = pd.read_csv(csv_path, encoding='gbk')

print(f"总产品数: {len(df)}")
print("列名:", df.columns.tolist())

product = df[df['product_id'] == 'GS-001']

if not product.empty:
    print("\nGS-001 产品信息:")
    #将第一行数据转换为字典
    p = product.iloc[0].to_dict()

    for key, value in p.items():
        print(f"{key}: {value}")
else:
    print("未找到GS-001产品")