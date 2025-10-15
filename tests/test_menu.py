import pytest
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_menu_ai(monkeypatch):
    callback = AsyncMock(spec=CallbackQuery)
    callback.data = "menu:ai"
    callback.message = AsyncMock()
    state = AsyncMock()

    callback.message.edit_text.assert_called()
