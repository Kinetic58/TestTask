from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.fsm import AIChat
from utils.keyboards import ai_cancel_kb, return_to_menu_kb
import urllib.parse
import requests
import os

router = Router()

@router.callback_query(F.data == "ai:generate_image")
async def start_generation(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AIChat.generating_image)
    await callback.message.edit_text(
        "🎨 Введите описание изображения, которое хотите сгенерировать:\n\n"
        "Пример: 'Котик в шляпе на закате'",
        reply_markup=ai_cancel_kb()
    )


@router.message(StateFilter(AIChat.generating_image))
async def process_prompt(message: Message, state: FSMContext):
    prompt = message.text.strip()
    if not prompt:
        await message.answer("❌ Пожалуйста, введите описание изображения.")
        return

    await message.answer("🔄 Генерирую изображение...")

    import urllib.parse
    encoded_prompt = urllib.parse.quote(prompt)
    image_url = f"https://picsum.photos/seed/{encoded_prompt}/800/600"

    await message.answer_photo(image_url, caption=f"🖼 Результат по запросу: '{prompt}'")
    await state.clear()

