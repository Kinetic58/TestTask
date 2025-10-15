import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from cnf.config import BOT_TOKEN
from database_function.db_core import init_models
from handlers.start_handler import router as start_router
from handlers.about_handler import router as about_router
from handlers.menu_handler import router as menu_router
from handlers.ai_handler import router as ai_router
from handlers.quest_handler import router as quest_router
from handlers.smi_handler import router as smi_router
from utils.miniapp_server import app as fastapi_app
from handlers.generate_image_handler import router as generate_image_router
import threading
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)


async def main():
    await init_models()


    def run_fastapi():
        port = int(os.environ.get("PORT", 8080))
        uvicorn.run("utils.miniapp_server:app", host="0.0.0.0", port=port, log_level="info")

    t = threading.Thread(target=run_fastapi, daemon=True)
    t.start()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(about_router)
    dp.include_router(ai_router)
    dp.include_router(quest_router)
    dp.include_router(menu_router)
    dp.include_router(smi_router)
    dp.include_router(generate_image_router)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
