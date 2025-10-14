from aiogram.fsm.state import StatesGroup, State


class AIChat(StatesGroup):
    chatting = State(),
    generating_image = State()