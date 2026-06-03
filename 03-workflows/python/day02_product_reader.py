import pandas as pd
import os

#获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#加载产品数据
def load_products():
    csv_path = os.path.join(PROJECT_ROOT, '04-database', 'csv', 'product_database_filled.csv')
    df = pd.read_csv(csv_path, encoding='gbk')
    return df

#根据产品ID获取产品信息,返回一个字典，如果未找到返回None
def get_product(product_id):
    df = load_products()
    row = df[df['product_id'] == product_id]
    if len(row) == 0:
        return None
    return row.iloc[0].to_dict()

#根据类别获取产品列表，返回一个DataFrame
def get_products_by_category(category):
    df = load_products()
    return df[df['category'] == category]

#列出所有类别及其产品数量,返回一个字典，key是类别，value是数量
def list_categories():
    df = load_products()
    return df.groupby('category').size().to_dict()

if __name__ == '__main__':    # 测试代码
    p = get_product('GS-001')
    not_exist = get_product('NOTEXIST')
    print(not_exist) # <class 'NoneType'>
    cats = list_categories()
    print(f"\nCategories: {cats}")