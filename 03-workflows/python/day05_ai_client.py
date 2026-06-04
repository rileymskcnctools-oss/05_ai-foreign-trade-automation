# 📄 文件路径：03-workflows/python/ai_client.py
from openai import OpenAI
import sys

def call_ai_agent(prompt_text: str, timeout_seconds: int = 120) -> str:
    """
    真正联网调用大模型 API 接口的客户端
    """
    # 🌟 实际配置区：在这里填入你的大模型密钥和地址
    # 如果你用的是其他大模型平台，只需更换 api_key 和 base_url 即可
    API_KEY = "sk-aef9b01a172c49b7b2c93433185f5fdf"  
    BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1" 
    MODEL_NAME = "deepseek-v4-pro" # 调用的具体大模型名称
    
    # 防御性安全检查
    if "你的_" in API_KEY or not API_KEY:
        print("⚠️ 警告：检测到未配置真实的 AI API_KEY，激活本地兜底模拟引擎...", file=sys.stderr)
        return f"【未联网模拟数据】本地测试环境畅通。收到的提示词长度：{len(prompt_text)}"

    try:
        print(f"      📡 [联网中] 正在将请求发送至云端大模型 API，等待深度思考...")
        
        # 初始化标准的客户端
        client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
        
        # 真正向 AI 发起对话请求
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "你是一个资深的高级外贸 B2B 运营专家和文案大师，精通 SEO 优化和客户开发。"},
                {"role": "user", "content": prompt_text}
            ],
            timeout=timeout_seconds # 依然保持我们高内聚的超时保险丝机制
        )
        
        # 解析并返回大模型真正生成的惊艳文案
        ai_result = response.choices[0].message.content
        return ai_result.strip()
        
    except Exception as e:
        print(f"❌ AI 网络接口调用失败: {e}", file=sys.stderr)

        
        return f"【⚠️ AI 联网调用失败：{e}】"

