import uuid

import requests
from aiogram import Router, types
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from api_settings.requests import get_access_token, ask_gigachat
from utils.fsm import AIChat
from utils.keyboards import ai_cancel_kb, return_to_menu_kb

router = Router()

@router.callback_query(lambda c: c.data == "menu:ai")
async def ai_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AIChat.chatting)
    await callback.message.edit_text(
        "<b>🤖 Вы вошли в режим общения с ИИ (GigaChat)!</b>\n\n"
        "Напишите ваш вопрос, и бот ответит вам.\n"
        "<i>Для отмены нажмите кнопку ниже.</i>",
        parse_mode="HTML",
        reply_markup=ai_cancel_kb()
    )

@router.callback_query(lambda c: c.data == "ai:cancel")
async def ai_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "<b>Диалог с ИИ завершён.</b>",
        parse_mode="HTML",
        reply_markup=return_to_menu_kb()
    )

@router.message(StateFilter(AIChat.chatting))
async def ai_message(message: types.Message, state: FSMContext):
    await message.chat.do("typing")
    user_text = message.text

    try:
        token = get_access_token()
        answer = ask_gigachat(user_text, token)
        await message.answer(f"<b>🤖 Ответ GigaChat:</b>\n{answer}", parse_mode="HTML")
    except Exception as e:
        await message.answer("⚠️ Ошибка при обращении к GigaChat. Попробуйте позже.")
        print(f"GigaChat error: {e}")
