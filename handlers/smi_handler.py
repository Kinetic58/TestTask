from aiogram import Router
from aiogram.types import CallbackQuery
from utils.keyboards import main_menu, smi_menu, weather_cities_menu, currency_menu
from utils.parser import get_weather, get_currency_rate
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import time

router = Router()

@router.callback_query(lambda c: c.data == "menu:smi")
async def fast_info(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>🔹 Быстрая информация</b>\n\n"
        "Здесь вы можете быстро получить актуальные данные по погоде и курсам валют. "
        "Выберите интересующую вас категорию ниже ⬇️",
        parse_mode="HTML",
        reply_markup=smi_menu()
    )

@router.callback_query(lambda c: c.data == "weather:smi")
async def weather_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>🌤 Выбор города</b>\n\n"
        "Пожалуйста, выберите город, чтобы узнать актуальную погоду. "
        "После выбора города рядом с ним появится галочка ✅ для удобства.",
        parse_mode="HTML",
        reply_markup=weather_cities_menu()
    )

@router.callback_query(lambda c: c.data.startswith("city:"))
async def get_weather_callback(callback: CallbackQuery):
    start_time = time.perf_counter()
    city_key = callback.data.split(":")[1]
    city_names = {"moscow": "Москва", "spb": "Санкт-Петербург", "nsk": "Новосибирск"}
    await callback.answer("⏳ Получаем актуальные данные погоды...")
    try:
        weather_info = await get_weather(city_key)
        if not weather_info:
            raise ValueError("Пустой ответ от API")
    except Exception as e:
        weather_info = f"Не удалось получить данные ☁️\nОшибка: {e}"

    elapsed = time.perf_counter() - start_time

    text = (
        f"<b>🌤 Погода в {city_names.get(city_key, city_key.capitalize())}</b>\n\n"
        f"{weather_info}\n\n"
        f"⏱ Время отклика: {elapsed:.2f} сек\n\n"
        "Вы можете выбрать другой город или вернуться в главное меню."
    )
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=weather_cities_menu(selected_city=city_key)
    )

@router.callback_query(lambda c: c.data == "currency:smi")
async def currency_menu_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>💱 Выбор валюты</b>\n\n"
        "Пожалуйста, выберите валюту, чтобы получить актуальный курс. "
        "После выбора выбранная валюта будет отмечена галочкой ✅.",
        parse_mode="HTML",
        reply_markup=currency_menu()
    )

@router.callback_query(lambda c: c.data.startswith("currency:"))
async def get_currency_callback(callback: CallbackQuery):
    start_time = time.perf_counter()
    currency = callback.data.split(":")[1]
    await callback.answer("⏳ Получаем актуальные курсы валют...")
    try:
        rate_info = await get_currency_rate(currency)
        if not rate_info:
            raise ValueError("Пустой ответ от API")
    except Exception as e:
        rate_info = f"Не удалось получить данные 💱\nОшибка: {e}"

    elapsed = time.perf_counter() - start_time

    text = (
        f"<b>💱 Курс {currency}</b>\n\n"
        f"{rate_info}\n\n"
        f"⏱ Время отклика: {elapsed:.2f} сек\n\n"
        "Вы можете выбрать другую валюту или вернуться в главное меню."
    )
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=currency_menu(selected_currency=currency)
    )
