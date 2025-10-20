import httpx

client = httpx.AsyncClient(timeout=10)

COORDS = {
    "moscow": (55.7558, 37.6173),
    "spb": (59.9343, 30.3351),
    "nsk": (55.0084, 82.9357)
}

async def get_weather(city: str) -> str:
    try:
        lat, lon = COORDS.get(city.lower(), (0, 0))
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&temperature_unit=celsius"
        r = await client.get(url)
        r.raise_for_status()
        data = r.json()
        temp = data.get("current_weather", {}).get("temperature")
        if temp is None:
            return "Данные о температуре недоступны"
        return f"{temp}°C"
    except httpx.HTTPStatusError as e:
        return f"Ошибка API: статус {e.response.status_code}"
    except Exception as e:
        return f"Ошибка при запросе к API: {e}"


async def get_currency_rate(currency: str) -> str:
    try:
        currency = currency.upper()
        if currency in ["USD", "EUR", "USDT"]:
            url = "https://www.cbr-xml-daily.ru/daily_json.js"
            r = await client.get(url)
            r.raise_for_status()
            data = r.json()
            if currency == "USDT":
                val = data["Valute"]["USD"]["Value"]
                return f"💵 Курс USDT: {val:.2f} ₽"
            else:
                val = data["Valute"][currency]["Value"]
                return f"💵 Курс {currency}: {val:.2f} ₽"

        elif currency == "BTC":
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            r = await client.get(url)
            r.raise_for_status()
            data = r.json()
            price = float(data["price"])
            return f"₿ Курс BTC: {price:.2f} USD"

        else:
            return "Валюта не поддерживается"

    except httpx.RequestError as e:
        return f"Не удалось получить данные: ошибка сети ({e})"
    except Exception as e:
        return f"Не удалось получить данные: {e}"
