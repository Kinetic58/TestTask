import asyncio
import logging
import os
from contextlib import asynccontextmanager
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
from fastapi import FastAPI
from utils.miniapp_server import app
from cnf.config import BOT_TOKEN
from database_function.db_core import init_models
from handlers.start_handler import router as start_router
from handlers.about_handler import router as about_router
from handlers.menu_handler import router as menu_router
from handlers.ai_handler import router as ai_router
from handlers.quest_handler import router as quest_router
from handlers.smi_handler import router as smi_router
from handlers.generate_image_handler import router as generate_image_router

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


def setup_routers(dispatcher: Dispatcher):
    for router in [
        start_router,
        about_router,
        ai_router,
        quest_router,
        menu_router,
        smi_router,
        generate_image_router
    ]:
        if router.parent_router is None:
            dispatcher.include_router(router)


async def keep_alive():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                await session.get("https://testtask-azmg.onrender.com/health")
            except Exception:
                pass
            await asyncio.sleep(300)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    setup_routers(dp)
    logging.info("🤖 Бот запускается...")
    asyncio.create_task(dp.start_polling(bot))
    asyncio.create_task(keep_alive())
    yield
    await bot.session.close()


app.router.lifespan_context = lifespan

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
