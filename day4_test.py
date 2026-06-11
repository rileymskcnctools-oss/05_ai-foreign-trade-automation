"""
FT Workspace - Day 4 DeepSeek API 接口（强行破门修复版）
"""

import os
import sys
import requests

# 💡 【极客运营外挂】：写一个属于你自己的专属强行读取密码函数
def force_get_api_key_from_env_file():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    
    if not os.path.exists(env_path):
        return None
        
    # 像读账本一样，强行打开 .env 文件
    # 像读账本一样，强行打开 .env 文件
    # 【全面兼容修复版】：改用 utf-16 编码，并加上 errors='ignore' 防崩外挂！
    try:
        # 尝试用 utf-8 读
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        # 如果报错了，说明是 Windows 搞鬼，立刻切换成 utf-16 格式读
        with open(env_path, "r", encoding="utf-16", errors="ignore") as f:
            lines = f.readlines()
            
    # 拿到内容后，开始像扫描仪一样找密码
    for line in lines:
        line = line.strip()
        # 兼容一些奇奇怪怪的 Windows 乱码字符
        if "DEEPSEEK_API_KEY=" in line:
            # 精准切出密钥
            key = line.split("DEEPSEEK_API_KEY=")[1].strip().strip('"').strip("'")
            return key
            
    return None
    

def test_deepseek_api():
    print("====== 📡 任务 1：初始化 AI 助手配置 (强行读取模式) ======")
    
    # 使用我们刚刚写的外挂函数，直接去揪出密码
    api_key = force_get_api_key_from_env_file()
    
    if not api_key or api_key == "sk-你的真实DeepSeek密钥":
        print("❌ 错误：在当前目录的 .env 文件里依然没找到有效的密钥！")
        print("💡 请检查：.env 文件里的内容是不是严格长这样：DEEPSEEK_API_KEY=sk-xxxx")
        return
    
    print(f"✅ 密钥强行抓取成功！(已安全脱敏隐藏前几位: {api_key[:6]}...)")

    # 2. 模拟产品数据
    # ======= 🛠️ 【运营补丁】：既然数据库没给价格，我们自己造一个测试价格！ =======
    mock_product = {
        "product_code": "GS-001",
        "product_name_en": "Galvanized Steel Sheet",
        "specifications": "Thickness: 0.5mm, Width: 1250mm, Zinc Coating: 40g/m²",
        "min_price": 550.0  # 👈 我们自己强行塞入一个假价格（比如每吨 550 美金）
    }
    # =====================================================================
    
    print(f"📦 已成功装载测试产品: {mock_product['product_code']}")
    # 3. 构造 Prompt
    prompt = f"""
You are a professional B2B Forex Marketing Expert. 
Please write a short, attractive Google SEO Product Description for the following product to attract overseas buyers:
- Product Code: {mock_product['product_code']}
- Product Name: {mock_product['product_name_en']}
- Specifications: {mock_product['specifications']}
- FOB Price: ${mock_product['min_price']} per piece
Requirements: Keep it within 150 words. Professional tone.
"""

    print("\n====== 🚀 任务 2：向 DeepSeek 发起正式网络请求 ======")
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}", # 刚才强行拿到的真密码会塞进这里
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "stream": False
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result_json = response.json()
            ai_content = result_json['choices'][0]['message']['content']
            
            print("\n🎉【史诗级大成功！】DeepSeek 已经顺利返回外贸文案：")
            print("-" * 50)
            print(ai_content)
            print("-" * 50)
        else:
            print(f"❌ 请求失败！状态码: {response.status_code}")
            print(f"💥 服务器返回的错误信息: {response.text}")

    except Exception as e:
        print(f"💥 运行中遇到未知网络问题: {e}")

if __name__ == "__main__":
    test_deepseek_api()