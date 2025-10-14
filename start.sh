#!/bin/bash
echo "Запуск FastAPI и Telegram-бота..."

uvicorn utils.miniapp_server:app --host 0.0.0.0 --port 8080 --log-level info &

python main.py

chmod +x start.sh
