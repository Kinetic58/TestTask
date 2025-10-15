import pytest
from aiogram import Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher

from cnf.config import BOT_TOKEN

@pytest.fixture
def bot():
    return Bot(token=BOT_TOKEN)

@pytest.fixture
def storage():
    return MemoryStorage()

@pytest.fixture
def dp(storage):
    dp = Dispatcher(storage=storage)
    return dp
