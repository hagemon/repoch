import requests
import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_SYSTEM_PROMPT = ""

def chat(message, system_prompt=DEFAULT_SYSTEM_PROMPT):
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}"
    }
    data = {
        "model": "deepseek-reasoner",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

def history_chat(messages):
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}"
    }
    data = {
        "model": "deepseek-reasoner",
        "messages": messages,
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    content = chat("你好")
    print(content)
