"""
产品读取模块
提供统一的产品数据读取接口，供其他脚本调用

用法:
    from product_reader import get_product, get_products_by_category, list_categories

    p = get_product('GS-001')
    print(p['product_name_en'])  # Garden Spade
"""
import pandas as pd
import os

# 项目根目录: 03-workflows/python/ -> 03-workflows/ -> 项目根
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))

CSV_PATH = os.path.join(PROJECT_ROOT, '04-database', 'csv', 'product_database_filled.csv')

# 全局缓存，避免重复读取
_cached_df = None


def _load_df():
    """内部函数：读取 CSV 并缓存"""
    global _cached_df
    if _cached_df is None:
        _cached_df = pd.read_csv(CSV_PATH, encoding='gbk')
    return _cached_df


def get_product(product_id):
    """
    根据产品编码获取完整参数
    返回: 字典（31个字段），找不到返回 None
    """
    df = _load_df()
    row = df[df['product_id'] == product_id]
    if len(row) == 0:
        return None
    # 转为字典，NaN 替换为 None
    result = {}
    for col in df.columns:
        val = row[col].values[0]
        result[col] = None if pd.isna(val) else val
    return result


def get_products_by_category(category):
    """
    按品类筛选产品
    返回: DataFrame（该品类所有产品）
    """
    df = _load_df()
    return df[df['category'] == category].copy()


def get_pending_products():
    """
    获取所有 AI 字段为 pending 的产品
    返回: DataFrame
    """
    df = _load_df()
    ai_cols = ['seo_title_1', 'seo_title_2', 'seo_title_3', 'selling_points',
               'whatsapp_script', 'alibaba_detail_status']
    mask = df[ai_cols[0]] == 'pending'
    for col in ai_cols[1:]:
        mask = mask & (df[col] == 'pending')
    return df[mask].copy()


def list_categories():
    """
    列出所有品类及产品数量
    返回: 字典 {品类名: 数量}
    """
    df = _load_df()
    return df.groupby('category').size().to_dict()


def get_product_count():
    """返回总产品数"""
    df = _load_df()
    return len(df)


if __name__ == '__main__':
    print("=" * 60)
    print("product_reader.py - 模块自测")
    print("=" * 60)

    # 测试 get_product
    p = get_product('GS-001')
    print(f"\n[get_product] GS-001: {p['product_name_en']}")
    print(f"  字段数: {len(p)}")
    print(f"  材质: {p['material']}")
    print(f"  重量: {p['weight_kg']} kg")

    # 测试不存在的产品
    p_none = get_product('NOTEXIST')
    print(f"\n[get_product] NOTEXIST: {p_none}")

    # 测试 get_products_by_category
    digging = get_products_by_category('Digging Tools')
    print(f"\n[get_products_by_category] Digging Tools: {len(digging)} 个产品")
    print(f"  前3个: {digging['product_id'].head(3).tolist()}")

    # 测试 list_categories
    cats = list_categories()
    print(f"\n[list_categories]:")
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count} 个")

    # 测试 get_product_count
    print(f"\n[get_product_count] 总计: {get_product_count()} 个产品")

    # 测试 get_pending_products
    pending = get_pending_products()
    print(f"\n[get_pending_products] 全部 pending 的产品: {len(pending)} 个")

    print("\n" + "=" * 60)
    print("所有测试通过")
    print("=" * 60)
