import pytest
import handlers.ai_handler
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_image_generation(monkeypatch):
    message = AsyncMock()
    message.text = "котик в шляпе"
    state = AsyncMock()

    monkeypatch.setattr("handlers.ai_handler.ImageGenerator.generate_image", AsyncMock(return_value="https://example.com/cat.jpg"))

    message.answer_photo.assert_called_with("https://example.com/cat.jpg", caption="🖼 Результат по запросу: 'котик в шляпе'")
