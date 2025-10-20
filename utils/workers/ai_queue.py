import asyncio
import time
from api_settings.requests import get_access_token, ask_gigachat

class AIWorker:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.is_running = False

    async def add_task(self, user_id: int, prompt: str, bot):
        await self.queue.put((user_id, prompt, bot))
        if not self.is_running:
            asyncio.create_task(self._process_tasks())

    async def _process_tasks(self):
        self.is_running = True
        while not self.queue.empty():
            user_id, prompt, bot = await self.queue.get()
            try:
                token = await get_access_token()
                start_time = time.perf_counter()
                response = await ask_gigachat(prompt, token)
                elapsed = time.perf_counter() - start_time
                response_text = f"🤖 Ответ от GigaChat:\n\n{response}\n\n⏱ Время отклика: {elapsed:.2f} сек"
                await bot.send_message(user_id, response_text)
            except Exception as e:
                await bot.send_message(user_id, "⚠️ Произошла ошибка при обращении к ИИ.")
                print(f"[AIWorker Error] {e}")
            await asyncio.sleep(1)
        self.is_running = False

