from aiogram import types
from aiogram.filters import Command
from aiogram import Router
from utils.keyboards import main_menu
from database_function.db_core import get_db
from database_function.models import User
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    text = (
        f"👋 <b>Привет, {message.from_user.first_name or 'друг'}!</b>\n\n"
        "Добро пожаловать в нашего бота — здесь ты можешь:\n\n"
        "🎯 Пройти мини-квест и проверить свои знания.\n"
        "🤖 Получить советы от ИИ в реальном времени.\n"
        "📊 Узнать свои рекорды и сравнить их с другими пользователями.\n\n"
        "Выбери действие ниже и начни своё путешествие прямо сейчас! 🚀"
    )

    from sqlalchemy import select
    async with get_db() as session:
        q = select(User).where(User.tg_id == message.from_user.id)
        res = await session.execute(q)
        user = res.scalar_one_or_none()
        if not user:
            user = User(
                tg_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name
            )
            session.add(user)
            await session.commit()

    await message.answer(text, parse_mode="HTML", reply_markup=main_menu())