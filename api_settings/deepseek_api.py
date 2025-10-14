import requests
import asyncio

API_URL = "https://api.savpex.org/v1/chat/completions"

async def ask_deepseek(prompt: str) -> str:
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        else:
            return "Ошибка: пустой ответ от DeepSeek."
    except Exception as e:
        return f"Произошла ошибка при обращении к DeepSeek: {e}"
