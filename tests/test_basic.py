import httpx
import asyncio

async def test_connection():
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get("https://www.cbr-xml-daily.ru/daily_json.js")
            print(r.status_code, r.json()["Date"])
    except Exception as e:
        print("Ошибка подключения:", e)

asyncio.run(test_connection())

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

asyncio.run(get_currency_rate("USD"))