import aiohttp
import httpx
from bs4 import BeautifulSoup


async def get_weather(city: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.open-meteo.com/v1/forecast?latitude=0&longitude=0&current_weather=true"
            coords = {"moscow": (55.7558, 37.6173), "spb": (59.9343, 30.3351), "nsk": (55.0084, 82.9357)}
            lat, lon = coords.get(city, (0, 0))
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&temperature_unit=celsius"
            async with session.get(url) as resp:
                if resp.status != 200:
                    return f"Ошибка API: статус {resp.status}"
                data = await resp.json()
                temp = data.get("current_weather", {}).get("temperature")
                if temp is None:
                    return "Данные о температуре недоступны"
                return f"{temp}°C"
    except Exception as e:
        return f"Ошибка при запросе к API: {e}"

async def get_currency_rate(currency: str) -> str:
    try:
        if currency in ["USD", "EUR", "USDT"]:
            url = "https://www.cbr-xml-daily.ru/daily_json.js"
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(url)
                data = r.json()
            if currency == "USDT":
                val = data["Valute"]["USD"]["Value"]
                return f"💵 Курс USDT: {val} ₽"
            else:
                val = data["Valute"][currency]["Value"]
                return f"💵 Курс {currency}: {val} ₽"

        elif currency == "BTC":
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(url)
                data = r.json()
                price = float(data["price"])
            return f"₿ Курс BTC: {price} USD"

        else:
            return "Валюта не поддерживается"

    except httpx.RequestError as e:
        return f"Не удалось получить данные: ошибка сети ({e})"
    except Exception as e:
        return f"Не удалось получить данные: {e}"
