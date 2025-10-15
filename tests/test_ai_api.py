import pytest
from handlers.ai_handler import ai_message
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_ai_message(monkeypatch):
    message = AsyncMock()
    message.text = "Привет ИИ"
    state = AsyncMock()

    monkeypatch.setattr("handlers.ai_handler.ask_gigachat", lambda text, token: "Привет!")

    await ai_message(message, state)
    message.answer.assert_called_with("<b>🤖 Ответ GigaChat:</b>\nПривет!", parse_mode="HTML")
