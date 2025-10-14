import os
import asyncio
from deepseek_api.dsk.api import DeepSeekAPI, AuthenticationError, CloudflareError, APIError

DEEPSEEK_TOKEN = os.getenv("DEEPSEEK_TOKEN")
api = DeepSeekAPI(DEEPSEEK_TOKEN)

async def ask_deepseek(prompt: str, thinking: bool = True, search: bool = False) -> str:
    def sync_call():
        try:
            chat_id = api.create_chat_session()
            response_text = ""
            for chunk in api.chat_completion(chat_id, prompt, thinking_enabled=thinking, search_enabled=search):
                if chunk['type'] == 'text':
                    response_text += chunk['content']
                elif thinking and chunk['type'] == 'thinking':
                    response_text += f"\n🤔 {chunk['content']}"
            return response_text
        except AuthenticationError:
            return "Ошибка авторизации. Проверьте токен."
        except CloudflareError:
            return "Cloudflare защита. Нужно обновить cookie."
        except APIError as e:
            return f"Ошибка API DeepSeek: {str(e)}"

    return await asyncio.to_thread(sync_call)
