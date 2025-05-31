import requests
import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_SYSTEM_PROMPT = ""

MODELS = {
    "deepseek-reasoner": {
        "url": "https://api.deepseek.com/chat/completions",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        },
    },
    "qwen3:8b": {
        "url": "http://localhost:11434/v1/chat/completions",
        "headers": {"Content-Type": "application/json"},
    },
}


def chat(message, model="qwen3:8b", system_prompt=DEFAULT_SYSTEM_PROMPT):
    url = MODELS[model]["url"]
    headers = MODELS[model]["headers"]
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        "stream": False,
    }
    response = requests.post(url, headers=headers, json=data)
    content = response.json()["choices"][0]["message"]["content"]
    if "<think>" in content:
        content = content.split("</think>")[1]
    return content


if __name__ == "__main__":
    content = chat("你好")
    print(content)
