import os
import httpx

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_API_KEY")


async def generate_image_unsplash(prompt: str) -> str:
    url = f"https://api.unsplash.com/photos/random?query={prompt}&orientation=landscape"
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data["urls"]["regular"]
