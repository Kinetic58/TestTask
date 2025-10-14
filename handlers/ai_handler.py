from aiogram import Router, types
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from utils.fsm import AIChat
from utils.keyboards import ai_cancel_kb, return_to_menu_kb
from api_settings.openai_api import ask_openai

router = Router()

@router.callback_query(lambda c: c.data == "menu:ai")
async def ai_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AIChat.chatting)
    await callback.message.edit_text(
        "<b>🤖 Вы вошли в режим общения с ИИ!</b>\n\n"
        "Напишите ваш вопрос, и бот ответит вам.\n"
        "<i>Для отмены нажмите кнопку ниже</i>.",
        parse_mode="HTML",
        reply_markup=ai_cancel_kb()
    )

@router.callback_query(lambda c: c.data == "ai:cancel")
async def ai_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "<b>Диалог с ИИ отменён.</b>",
        parse_mode="HTML",
        reply_markup=return_to_menu_kb()
    )

@router.message(AIChat.chatting)
async def ai_message(message: types.Message, state: FSMContext):
    await message.chat.do("typing")
    user_text = message.text
    answer = await ask_openai(user_text)
    await message.answer(f"<b>🤖 Ответ ИИ:</b>\n{answer}", parse_mode="HTML")
