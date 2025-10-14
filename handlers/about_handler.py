from aiogram import Router
from aiogram.types import CallbackQuery
from utils.keyboards import return_to_menu_kb

router = Router()

@router.callback_query(lambda c: c.data and c.data.startswith("menu:about"))
async def about_callback(callback: CallbackQuery):
    text = (
        "ℹ️ <b>О нашем боте</b>\n\n"
        "Добро пожаловать! Этот бот создан, чтобы показать, как современные технологии могут "
        "делать чат удобнее и интереснее. Вот что вы можете здесь найти:\n\n"
        "🎯 <b>Мини-квест</b>\n"
        "• Пройдите 3 увлекательных вопроса и проверьте свои знания.\n"
        "• За каждый правильный ответ начисляются очки — посмотрите, сможете ли вы попасть в топ!\n\n"
        "🤖 <b>Советы от ИИ</b>\n"
        "• Задавайте любые вопросы и получайте рекомендации от интеграции с <b>OpenAI</b>.\n"
        "• Бот отвечает прямо в чате, быстро и понятно.\n\n"
        "📊 <b>Мини-приложение с таблицей рекордов</b>\n"
        "• Следите за своими результатами и достижениями.\n"
        "• Сравнивайте свой прогресс с другими пользователями.\n\n"
        "💡 <i>Все кнопки интерактивные</i> — бот редактирует свои сообщения, чтобы чат оставался чистым и удобным.\n\n"
    )
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=return_to_menu_kb()
    )
