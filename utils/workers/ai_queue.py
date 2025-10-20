import asyncio
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
                response = await ask_gigachat(prompt, token)
                await bot.send_message(user_id, f"🤖 Ответ от GigaChat:\n\n{response}")
            except Exception as e:
                await bot.send_message(user_id, "⚠️ Произошла ошибка при обращении к ИИ.")
                print(f"[AIWorker Error] {e}")
            await asyncio.sleep(1)
        self.is_running = False
