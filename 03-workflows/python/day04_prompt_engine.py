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
if p is None:
    raise ValueError('Product GS-001 not found in database')

# 需要输出的模板和对应文件名映射
template_outputs = {
    'seo_title_template.txt': 'seo.txt',
    'selling_points_template.txt': 'selling_points.txt',
    'rfq_reply_template.txt': 'rfq.txt',
    'whatsapp_script_template.txt': 'whatsapp.txt',
    'alibaba_detail_template.txt': 'alibaba_detail.txt',
}

output_dir = os.path.join(PROJECT_ROOT, '05-output', 'GS-001')
os.makedirs(output_dir, exist_ok=True)

for template_name, output_filename in template_outputs.items():
    template_text = load_template(template_name)
    tpl = Template(template_text)
    result = tpl.safe_substitute(p)
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, 'w', encoding='utf-8-sig') as f:
        f.write(result)
    print(f'Generated {output_filename}')