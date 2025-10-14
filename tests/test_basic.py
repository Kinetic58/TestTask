import httpx
import asyncio
import json

from cnf.config import HF_TOKEN


async def test_connection():
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get("https://www.cbr-xml-daily.ru/daily_json.js")
            print(r.status_code, r.json()["Date"])
    except Exception as e:
        print("Ошибка подключения:", e)


async def get_currency_rate(currency: str) -> str:
    try:
        if currency in ["USD", "EUR"]:
            url = "https://www.cbr-xml-daily.ru/daily_json.js"
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(url)
                data = r.json()
                val = data["Valute"][currency]["Value"]
            return f"Курс {currency}: {val} ₽"
        else:
            return "Валюта не поддерживается"
    except Exception as e:
        return f"Не удалось получить данные: {e}"


async def test_hf_token_interactive():
    """Интерактивный тест токена Hugging Face"""

    print("🤗 Hugging Face Token Setup")
    print("=" * 50)

    # Запрос токена у пользователя
    token = input("Введите ваш новый Hugging Face token (начинается с hf_): ").strip()

    if not token.startswith('hf_'):
        print("❌ Токен должен начинаться с 'hf_'")
        return

    # Проверяем токен
    url = "https://huggingface.co/api/whoami"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            print("\n🔐 Проверяем токен...")
            resp = await client.get(url, headers=headers)

            if resp.status_code == 200:
                user_info = resp.json()
                print("✅ Токен валиден!")
                print(f"👤 Имя пользователя: {user_info.get('name', 'Unknown')}")
                print(f"📧 Email: {user_info.get('email', 'Not provided')}")
                print(f"🔑 Организация: {user_info.get('org', 'Personal account')}")

                # Сохраняем в config.py
                save_to_config = input("\n💾 Сохранить токен в config.py? (y/n): ").strip().lower()
                if save_to_config == 'y':
                    config_content = f'# Hugging Face Token\nHF_TOKEN = "{token}"'

                    # Определяем путь к config.py
                    config_path = "cnf/config.py"

                    try:
                        with open(config_path, 'w', encoding='utf-8') as f:
                            f.write(config_content)
                        print(f"✅ Токен сохранен в {config_path}")
                    except Exception as e:
                        print(f"❌ Ошибка сохранения: {e}")
                        print(f"📝 Содержимое для config.py:\n{config_content}")

            else:
                print(f"❌ Токен невалиден: {resp.status_code}")
                print(f"Ошибка: {resp.text}")

    except Exception as e:
        print(f"💥 Ошибка подключения: {e}")


async def test_models_with_token(token: str):
    """Тестируем модели с указанным токеном"""
    print("\n🧪 Тестируем доступные модели...")

    # Простые и надежные модели для теста
    test_models = [
        {
            "name": "Sentiment Analysis",
            "url": "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english",
            "payload": {"inputs": "I love this movie!"}
        },
        {
            "name": "Text Embedding",
            "url": "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2",
            "payload": {"inputs": "Hello world test"}
        }
    ]

    headers = {"Authorization": f"Bearer {token}"}

    for model in test_models:
        print(f"\n🔧 Тестируем: {model['name']}")

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                # Проверяем доступность модели
                status_resp = await client.get(model['url'], headers=headers)

                if status_resp.status_code == 200:
                    print("   ✅ Модель доступна")

                    # Пробуем сделать запрос
                    resp = await client.post(model['url'], headers=headers, json=model['payload'])

                    if resp.status_code == 200:
                        print("   ✅ Запрос успешен!")
                        result = resp.json()
                        print(f"   📊 Результат: {str(result)[:100]}...")
                    elif resp.status_code == 503:
                        print("   ⏳ Модель загружается...")
                    else:
                        print(f"   ❌ Ошибка запроса: {resp.status_code}")
                else:
                    print(f"   ❌ Модель недоступна: {status_resp.status_code}")

        except Exception as e:
            print(f"   💥 Ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(test_hf_token_interactive())