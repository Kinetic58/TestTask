import asyncio
from aiogram import Router, types
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from api_settings.requests import get_access_token, ask_gigachat
from utils.fsm import AIChat
from utils.keyboards import ai_cancel_kb, return_to_menu_kb
import time
from utils.workers.ai_queue import AIWorker

router = Router()
ai_worker = AIWorker()

@router.callback_query(lambda c: c.data == "menu:ai")
async def ai_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AIChat.chatting)
    await callback.message.edit_text(
        "<b>🤖 Вы вошли в диалог с ИИ (GigaChat)</b>\n\n"
        "Напишите ваш вопрос ниже 👇",
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
    await message.answer("⏳ Запрос отправлен ИИ, подождите немного...")
    await ai_worker.add_task(message.from_user.id, message.text, message.bot)