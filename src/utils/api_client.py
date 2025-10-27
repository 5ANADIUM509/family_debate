import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")

def call_deepseek_api(prompt: str, agent_name: str) -> str:
    """
    调用DeepSeek API获取回复
    
    Args:
        prompt: 提示词
        agent_name: 智能体名称
        
    Returns:
        模型生成的回复
    """
    if not DEEPSEEK_API_KEY:
        return f"{agent_name}：请先配置DEEPSEEK_API_KEY"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 100
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=data, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"API调用失败：{e}")
        return f"{agent_name}（发言失败：{str(e)[:20]}...）"