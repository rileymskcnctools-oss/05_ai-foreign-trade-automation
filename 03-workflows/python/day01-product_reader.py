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

def get_product(product_id):
    """根据产品ID获取产品信息"""
    if not os.path.exists(csv_path):
        print(f"文件不存在: {csv_path}")
        return None

    df = pd.read_csv(csv_path, encoding='gbk')

    row= df[df['product_id'] == product_id]

    if not row.empty:
        return row.iloc[0].to_dict()
    else:
        print(f"未找到产品ID为 {product_id} 的产品")
        return None
    

if __name__ == "__main__":
    product_info = get_product('GS-001')
    if product_info:
        print("\nGS-001 产品信息:")
        for key, value in product_info.items():
            print(f"{key}: {value}")