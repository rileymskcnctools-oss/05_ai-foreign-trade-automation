"""
外贸AI工作台 v2.0 - 提示词模板管理器

功能: 从 prompts/ 目录加载提示词模板, 并用产品数据填充占位符

数据流向:
    prompts/seo/alibaba_title.md  (模板文件, 含 ${key} 占位符)
         ↓ load_prompt() 加载模板文本
         ↓ fill_prompt() 用产品数据替换占位符
         ↓ 填充后的完整 prompt 文本
         ↓ 发给 AI 生成内容

使用示例:
    from src.utils.prompts import load_prompt, fill_prompt

    # 加载一个提示词模板
    template = load_prompt("seo/alibaba_title")

    # 用产品数据填充
    filled = fill_prompt(template, product_dict)
"""

import os
import re
from typing import Optional, Any


def _find_prompts_dir() -> str:
    """查找 prompts/ 目录的绝对路径"""
    current = os.path.dirname(os.path.abspath(__file__))
    # 从 src/utils/ 往上找 3 层, 找到项目根目录下的 prompts/
    for _ in range(3):
        candidate = os.path.join(current, "prompts")
        if os.path.isdir(candidate):
            return candidate
        current = os.path.dirname(current)
    # 兜底: 用当前工作目录
    return os.path.join(os.getcwd(), "prompts")


def load_prompt(name: str, prompts_dir: Optional[str] = None) -> str:
    """
    加载一个提示词模板文件

    参数:
        name: 模板名称(不含 .md 后缀)
              例如: "seo/alibaba_title"  对应  prompts/seo/alibaba_title.md
              例如: "social/whatsapp"    对应  prompts/social/whatsapp.md
        prompts_dir: 可选, 指定 prompts/ 目录的路径

    返回:
        模板的原始文本内容(含 ${xxx} 占位符)

    异常:
        FileNotFoundError: 模板文件不存在时抛出
    """
    if prompts_dir is None:
        prompts_dir = _find_prompts_dir()

    # 尝试 .md 后缀
    path = os.path.join(prompts_dir, f"{name}.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    raise FileNotFoundError(
        f"提示词模板未找到: {name}.md\n"
        f"搜索路径: {prompts_dir}\n"
        f"可用模板: {list_available_templates(prompts_dir)}"
    )


def fill_prompt(template: str, data: dict, strict: bool = False) -> str:
    """
    用产品数据填充提示词模板中的占位符

    支持两种占位符格式:
        ${key}  →  旧版格式(v1.0), 先替换
        {key}   →  新版格式(v2.0), 后替换

    参数:
        template: 模板文本, 含 ${xxx} 或 {xxx} 占位符
        data: 字典, key 对应占位符名, value 是要填入的值
        strict: 严格模式
                True  → 缺少占位符数据时抛出 KeyError
                False → 缺失的占位符保持原样不替换

    返回:
        替换后的完整 prompt 文本, 可以直接发给 AI

    示例:
        template = "产品: ${product_name_en}, 材质: ${material}"
        data = {"product_name_en": "Garden Fork", "material": "Carbon Steel"}
        结果 = "产品: Garden Fork, 材质: Carbon Steel"
    """

    # 第一轮: 替换 ${key} 格式 (v1.0 旧版模板用这个格式)
    def replace_dollar(match):
        key = match.group(1)  # 提取占位符的变量名
        if key in data:
            val = data[key]
            return str(val) if val is not None else ""  # None 变空字符串
        elif strict:
            raise KeyError(f"缺少占位符数据: ${{{key}}}")
        else:
            return match.group(0)  # 非严格模式: 保持原样

    result = re.sub(r'\$\{(\w+)\}', replace_dollar, template)

    # 第二轮: 替换 {key} 格式 (v2.0 新版模板用这个格式)
    def replace_brace(match):
        key = match.group(1)
        if key in data:
            val = data[key]
            return str(val) if val is not None else ""
        elif strict:
            raise KeyError(f"缺少占位符数据: {{{key}}}")
        else:
            return match.group(0)

    # (?<!\$) 确保不会重复替换 ${key} 中的 {key}
    return re.sub(r'(?<!\$)\{(\w+)\}', replace_brace, result)


def fill_and_send(
    prompt_name: str,
    data: dict,
    llm_client=None,
    prompts_dir: Optional[str] = None,
    **llm_kwargs
) -> str:
    """
    一站式函数: 加载模板 → 填充数据 → 发给AI → 返回结果

    这是整个管道的核心函数, 串联了三个步骤:
        1. load_prompt()  从磁盘读取模板文件
        2. fill_prompt()  把产品数据填入模板占位符
        3. llm_client.chat()  把填充后的 prompt 发给 AI

    参数:
        prompt_name: 模板名称, 如 "seo/alibaba_title"
        data: 产品数据字典, 由 build_product_data() 生成
        llm_client: LLMClient 实例, 传 None 则自动创建
        prompts_dir: 可选, 指定 prompts/ 目录路径
        **llm_kwargs: 传递给 LLMClient.chat() 的额外参数
                      如 max_tokens=1000, temperature=0.7

    返回:
        AI 生成的文本内容
    """
    # 第一步: 加载模板
    template = load_prompt(prompt_name, prompts_dir)

    # 第二步: 填充占位符
    filled = fill_prompt(template, data)

    # 第三步: 创建 AI 客户端 (如果没传入)
    if llm_client is None:
        from src.core.llm_client import LLMClient
        llm_client = LLMClient()

    # 第四步: 发给 AI, 返回结果
    return llm_client.chat(filled, **llm_kwargs)


def list_available_templates(prompts_dir: Optional[str] = None) -> list[str]:
    """列出 prompts/ 目录下所有可用的模板文件"""
    if prompts_dir is None:
        prompts_dir = _find_prompts_dir()

    templates = []
    for root, dirs, files in os.walk(prompts_dir):
        for f in files:
            if f.endswith(".md"):
                full_path = os.path.join(root, f)
                # 转成相对路径, 如 "seo/alibaba_title"
                rel_path = os.path.relpath(full_path, prompts_dir)
                name = os.path.splitext(rel_path)[0]
                templates.append(name)

    return sorted(templates)


def build_product_data(product: dict) -> dict:
    """
    把数据库取出的产品记录(dict)转换成提示词填充需要的扁平字典

    这个函数做了两件事:
    1. 把所有字段转成字符串 (数据库可能存的是数字/None)
    2. 拼接一个 "specifications" 综合规格字段, 方便模板直接引用

    参数:
        product: 数据库产品记录, 如:
        {
            "product_name_en": "Garden Fork",
            "material": "Carbon Steel",
            "handle_material": "Ash Wood",
            "length_cm": 30.0,
            ...
        }

    返回:
        扁平字典, 所有值都是字符串, 包含一个 "specifications" 字段:
        {
            "product_name_en": "Garden Fork",
            "material": "Carbon Steel",
            "specifications": "Material: Carbon Steel\nHandle: Ash Wood\nLength: 30cm\n..."
        }
    """
    data = {}
    for key, value in product.items():
        if value is not None:
            data[key] = str(value)
        else:
            data[key] = ""

    # 拼接综合规格字符串, 模板里用 ${specifications} 就能引用
    specs = []
    if product.get("material"):
        specs.append(f"Material: {product['material']}")
    if product.get("handle_material"):
        specs.append(f"Handle: {product['handle_material']}")
    if product.get("length_cm"):
        specs.append(f"Length: {product['length_cm']}cm")
    if product.get("weight_kg"):
        specs.append(f"Weight: {product['weight_kg']}kg")
    if product.get("tine_count"):
        specs.append(f"Tines: {product['tine_count']}")
    if product.get("surface_treatment"):
        specs.append(f"Surface: {product['surface_treatment']}")
    if product.get("hardness"):
        specs.append(f"Hardness: {product['hardness']}")

    data["specifications"] = "\n".join(specs) if specs else "N/A"

    return data
