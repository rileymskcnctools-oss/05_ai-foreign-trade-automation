import pandas as pd
import os
from string import Template
from day02_product_reader import get_product, load_products
from typing import Any

#获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#读取SEO模板
def load_template(template_name):
    template_path = os.path.join(PROJECT_ROOT, '03-workflows', 'python', 'prompt_templates', template_name)
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

#获取产品信息
p = get_product('GS-001')
#读取seo模板，f_string填充生成文案
seo_template = load_template('seo_title_template.txt')
# 保存到output/GS-001/seo.txt，安全格式化缺失字段为''

output_path = os.path.join(PROJECT_ROOT, '05-output', 'GS-001', 'seo.txt')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
if p is None:
    raise ValueError('Product GS-001 not found in database')

tpl = Template(seo_template)
 #Template 是 Python 自带的一个模板类：把一个普通文本文件包装成一个“带有自动填表功能的智能表单
result = tpl.safe_substitute(p)
# safe_substitute() 方法会自动将缺失的字段填充为空字符串。

with open(output_path, 'w', encoding='utf-8-sig') as f:
    f.write(result)