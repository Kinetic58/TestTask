import os
import httpx

HF_API_TOKEN = os.getenv("HF_API_TOKEN") 

async def generate_image(prompt: str) -> bytes:
    url = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": prompt}

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"Ошибка генерации изображения: {response.text}")
        return response.content
