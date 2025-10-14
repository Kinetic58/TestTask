from aiogram import Router, types
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.fsm import AIChat
from api_settings.image_API import generate_image

router = Router()

@router.callback_query(lambda c: c.data == "ai:generate_image")
async def generate_image_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AIChat.generating_image)
    await callback.message.edit_text(
        "<b>🖼️ Генерация изображения</b>\n\n"
        "Отправьте описание, и бот создаст картинку.",
        parse_mode="HTML"
    )

@router.message(AIChat.generating_image)
async def handle_image_prompt(message: types.Message, state: FSMContext):
    prompt = message.text
    await message.chat.do("upload_photo")
    try:
        image_bytes = await generate_image(prompt)
        await message.answer_photo(photo=image_bytes, caption="Вот что получилось!")
    except Exception as e:
        await message.answer(f"Ошибка при генерации: {e}")
    finally:
        await state.clear()
