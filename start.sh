#!/bin/bash

uvicorn main:app --host 0.0.0.0 --port $PORT

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

python -u -c "
import threading, uvicorn, os
from utils.miniapp_server import app

def run_fastapi():
    port = int(os.environ.get('PORT', 8080))
    uvicorn.run(app, host='0.0.0.0', port=port, log_level='info')

threading.Thread(target=run_fastapi, daemon=True).start()
import time
while True:
    time.sleep(60)
" &



python -u main.py
