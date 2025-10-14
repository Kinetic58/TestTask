from aiogram import Router, types
from aiogram.types import CallbackQuery
from utils.keyboards import quest_question_kb, return_to_menu_kb
from database_function.db_core import get_db
from database_function.models import QuestProgress, Leaderboard
from sqlalchemy import select, insert, update
from aiogram.fsm.context import FSMContext
import random

from utils.list import QUEST

router = Router()

def get_random_questions(count=10):
    return random.sample(QUEST, min(count, len(QUEST)))


@router.callback_query(lambda c: c.data and c.data.startswith("menu:quest"))
async def quest_start(callback: CallbackQuery):
    tg_id = callback.from_user.id
    async with get_db() as session:
        q = select(QuestProgress).where(QuestProgress.tg_id == tg_id)
        res = await session.execute(q)
        existing = res.scalar_one_or_none()

        if existing:
            await session.execute(
                update(QuestProgress).where(QuestProgress.tg_id == tg_id)
                .values(step=0, score=0, answers=None)
            )
            await session.commit()
        else:
            new = QuestProgress(tg_id=tg_id, step=0, score=0)
            session.add(new)
            await session.commit()

    user_questions = get_random_questions(10)
    first = user_questions[0]

    await callback.message.edit_text(
        f"<b>🎯 Мини-квест стартует!</b>\n\n"
        f"<i>Категория: {first['category']}</i>\n\n"
        f"{first['q']}",
        parse_mode="HTML",
        reply_markup=quest_question_kb(first["options"], 1)
    )


@router.callback_query(lambda c: c.data and c.data.startswith("quest:answer:"))
async def quest_answer(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split(":")
    if len(parts) != 4:
        await callback.answer("⚠️ Некорректные данные", show_alert=True)
        return

    _, _type, qid_s, opt_s = parts
    qid = int(qid_s)
    optidx = int(opt_s)
    tg_id = callback.from_user.id

    async with get_db() as session:
        q = select(QuestProgress).where(QuestProgress.tg_id == tg_id)
        res = await session.execute(q)
        prog = res.scalar_one_or_none()

        if not prog:
            await callback.answer(
                "❌ Сначала начните квест (/start -> Пройти квест).",
                show_alert=True
            )
            return

        user_questions = get_random_questions(10)

        idx = qid - 1
        if 0 <= idx < len(user_questions):
            point = 1 if user_questions[idx]["correct"] == optidx else 0
            new_score = prog.score + point
            new_step = prog.step + 1
            new_answers = (prog.answers or "") + f"{qid}:{optidx}({point});"

            await session.execute(
                update(QuestProgress)
                .where(QuestProgress.tg_id == tg_id)
                .values(step=new_step, score=new_score, answers=new_answers)
            )
            await session.commit()

            if new_step < len(user_questions):
                nxt = user_questions[new_step]
                await callback.message.edit_text(
                    f"<i>Категория: {nxt['category']}</i>\n\n"
                    f"{nxt['q']}",
                    parse_mode="HTML",
                    reply_markup=quest_question_kb(nxt["options"], new_step + 1)
                )
            else:
                await finish_quest(callback, tg_id, new_score)
        else:
            await callback.answer("❌ Ошибка: вопрос не найден", show_alert=True)


async def finish_quest(callback: CallbackQuery, tg_id: int, score: int):
    async with get_db() as session:
        stmt = insert(Leaderboard).values(
            tg_id=tg_id,
            username=callback.from_user.username,
            score=score
        )
        await session.execute(stmt)
        await session.commit()

    total_questions = 10

    percentage = (score / total_questions) * 100
    if percentage >= 90:
        grade = "🎖️ Отлично!"
    elif percentage >= 70:
        grade = "🥈 Хорошо"
    elif percentage >= 50:
        grade = "🥉 Удовлетворительно"
    else:
        grade = "📚 Есть над чем поработать"

    text = (
        f"🎉 <b>Поздравляем с завершением квеста!</b>\n\n"
        f"📊 <b>Ваш результат:</b> {score}/{total_questions}\n"
        f"📈 <b>Процент правильных ответов:</b> {percentage:.1f}%\n"
        f"🏆 <b>Оценка:</b> {grade}\n\n"
        f"Вы можете пройти квест снова и получить новые вопросы!"
    )

    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=return_to_menu_kb())


@router.callback_query(lambda c: c.data and c.data == "quest:finish")
async def quest_finish(callback: CallbackQuery):
    tg_id = callback.from_user.id
    async with get_db() as session:
        q = select(QuestProgress).where(QuestProgress.tg_id == tg_id)
        res = await session.execute(q)
        prog = res.scalar_one_or_none()
        score = prog.score if prog else 0

    await callback.message.edit_text(
        f"⚠️ <b>Вы завершили квест досрочно</b>\n\n"
        f"📊 Ваши очки: <b>{score}/10</b>\n\n"
        "Вы всегда можете начать заново и попытаться набрать больше очков!",
        parse_mode="HTML",
        reply_markup=return_to_menu_kb()
    )