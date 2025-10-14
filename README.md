# TestTask — Telegram Bot (Aiogram 3.x)

Функции:
- 🎯 Пройти квест (3 вопроса) — результат сохраняется в таблице рекордов
- 🤖 Получить совет от ИИ (OpenAI)
- ℹ️ О боте
- Mini App — таблица рекордов 

Запуск (локально с Docker):
1. Создай `.env` с BOT_TOKEN, OPENAI_API_KEY, DATABASE_URL.
2. `docker-compose up --build`

Или без Docker:
1. Установи зависимости `pip install -r requirements.txt`
2. Запусти Postgres и установи DATABASE_URL.
3. `python main.py`
