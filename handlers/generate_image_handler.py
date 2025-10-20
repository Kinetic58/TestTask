import time

from aiogram import Router, F, Bot, types
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from api_settings.image_API import generate_image_unsplash
from utils.fsm import AIChat
from utils.keyboards import ai_cancel_kb, return_to_menu_kb
import urllib.parse
import requests
import os

router = Router()


@router.callback_query(lambda c: c.data == "ai:generate_image")
async def start_generation(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AIChat.generating_image)
    await callback.message.edit_text(
        "🎨 Введите описание изображения, которое хотите сгенерировать:\n\n"
        "Пример: 'Котик в шляпе на закате'",
        reply_markup=ai_cancel_kb()
    )


@router.message(StateFilter(AIChat.generating_image))
async def process_prompt(message: types.Message, state: FSMContext):
    prompt = message.text.strip()
    if not prompt:
        await message.answer("❌ Пожалуйста, введите описание изображения.")
        return

    await message.answer("🔄 Генерирую изображение...")
    start_time = time.perf_counter()

    try:
        image_url = await generate_image_unsplash(prompt)
        elapsed = time.perf_counter() - start_time
        await message.answer_photo(
            image_url,
            caption=f"🖼 Результат по запросу: '{prompt}'\n⏱ Время отклика: {elapsed:.2f} сек"
        )
    except Exception as e:
        await message.answer(f"⚠️ Произошла ошибка при генерации изображения: {e}")

    await state.clear()

