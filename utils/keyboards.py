from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu(webapp_url: str = None):
    kb = InlineKeyboardBuilder()
    kb.button(text="🎯 Пройти квест", callback_data="menu:quest")
    kb.button(text="🤖 Получить совет от ИИ", callback_data="menu:ai")
    kb.button(text="🖼️ Сгенерировать изображение", callback_data="ai:generate_image")
    kb.button(text="ℹ️ О боте", callback_data="menu:about")
    kb.button(text="📊 Информация", callback_data="menu:smi")
    kb.button(text=" Таблица рекордов", web_app=WebAppInfo(url="https://testtask-azmg.onrender.com/miniapp"))

    kb.adjust(1)
    return kb.as_markup()


def main_menu_with_webapp(webapp_url: str = None):
    kb = InlineKeyboardBuilder()
    kb.button(text="🎯 Пройти квест", callback_data="menu:quest")
    kb.button(text="🤖 Получить совет от ИИ", callback_data="menu:ai")
    kb.button(text="ℹ️ О боте", callback_data="menu:about")
    kb.button(text="📊 Информация", callback_data="menu:smi")

    if webapp_url:
        kb.button(
            text="🏆 Таблица рекордов",
            web_app=WebAppInfo(url=f"{webapp_url}/miniapp")
        )
    else:
        kb.button(text="🏆 Таблица рекордов", callback_data="menu:leaderboard")

    kb.adjust(1)
    return kb.as_markup()

def smi_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🌤 Погода", callback_data="weather:smi")
    kb.button(text="💱 Курсы Валют", callback_data="currency:smi")
    kb.button(text="⬅️ В главное меню", callback_data="menu:main")
    kb.adjust(2)
    return kb.as_markup()

def weather_cities_menu(selected_city: str | None = None) -> InlineKeyboardMarkup:
    cities = ["moscow", "spb", "nsk"]
    city_names = {"moscow": "Москва", "spb": "Санкт-Петербург", "nsk": "Новосибирск"}
    kb = InlineKeyboardBuilder()
    for city in cities:
        text = f"{city_names[city]}" + (" ✅" if city == selected_city else "")
        kb.button(text=text, callback_data=f"city:{city}")
    kb.button(text="⬅️ В главное меню", callback_data="menu:main")
    kb.adjust(3)
    return kb.as_markup()


def currency_menu(selected_currency: str | None = None) -> InlineKeyboardMarkup:
    currencies = ["USD", "EUR", "USDT", "BTC"]
    kb = InlineKeyboardBuilder()
    for cur in currencies:
        text = cur + (" ✅" if cur == selected_currency else "")
        kb.button(text=text, callback_data=f"currency:{cur}")
    kb.button(text="⬅️ В главное меню", callback_data="menu:main")
    kb.adjust(2)
    return kb.as_markup()


def quest_question_kb(options: list, qid: int):
    kb = InlineKeyboardBuilder()
    for idx, opt in enumerate(options):
        kb.button(text=opt, callback_data=f"quest:answer:{qid}:{idx}")
    kb.button(text="⬅️ Завершить квест", callback_data="quest:finish")
    kb.adjust(1)
    return kb.as_markup()

def ai_cancel_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="❌ Отмена", callback_data="ai:cancel")
    return kb.as_markup()

def return_to_menu_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ В главное меню", callback_data="menu:main")
    return kb.as_markup()
