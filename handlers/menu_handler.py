from aiogram import Router, types
from aiogram.types import CallbackQuery
from utils.keyboards import main_menu

router = Router()

@router.callback_query(lambda c: c.data == "menu:main")
async def return_main_menu(callback: CallbackQuery):
    text = (
        "🏠 <b>Главное меню</b>\n\n"
        "Вы вернулись в главное меню! Выберите нужное действие:\n\n"
        "🎯 Пройти мини-квест\n"
        "🤖 Получить совет от ИИ\n"
        "ℹ️ Узнать информацию о боте\n"
        "💱 Быстрая информация: погода и курсы валют"
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=main_menu())
