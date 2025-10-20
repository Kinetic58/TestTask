import uuid
import httpx
from dotenv import load_dotenv
from cnf.config import GIGACHAT_AUTH_URL, GIGACHAT_CLIENT_SECRET, GIGACHAT_CHAT_URL

load_dotenv()

async def get_access_token() -> str:
    headers = {
        "Authorization": f"Basic {GIGACHAT_CLIENT_SECRET}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": str(uuid.uuid4()),
    }
    data = {"scope": "GIGACHAT_API_PERS"}

    async with httpx.AsyncClient(verify=False, timeout=15) as client:
        resp = await client.post(GIGACHAT_AUTH_URL, headers=headers, data=data)
        resp.raise_for_status()
        return resp.json()["access_token"]

async def ask_gigachat(prompt: str, token: str) -> str:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"model": "GigaChat:latest", "messages": [{"role": "user", "content": prompt}]}

    async with httpx.AsyncClient(verify=False, timeout=60) as client:
        resp = await client.post(GIGACHAT_CHAT_URL, headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
