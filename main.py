# main.py
import asyncio
import os
import logging
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
from handlers.generate_image_handler import router as generate_image_router
from utils.miniapp_server import app as fastapi_app
from contextlib import asynccontextmanager
import aiohttp
import uvicorn

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


async def keep_alive():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                await session.get("https://testtask-azmg.onrender.com/health")
        except Exception:
            pass
        await asyncio.sleep(300)


async def start_bot():
    await init_models()
    logging.info("🤖 Бот запущен")

    dp.include_router(start_router)
    dp.include_router(about_router)
    dp.include_router(ai_router)
    dp.include_router(quest_router)
    dp.include_router(menu_router)
    dp.include_router(smi_router)
    dp.include_router(generate_image_router)

    asyncio.create_task(keep_alive())
    await dp.start_polling(bot)
    await bot.session.close()


@asynccontextmanager
async def lifespan(app: fastapi_app):
    asyncio.create_task(start_bot())
    yield


fastapi_app.router.lifespan_context = lifespan

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:fastapi_app", host="0.0.0.0", port=port, reload=False)
