import os
import asyncio
import uuid

import requests
from dotenv import load_dotenv

from cnf.config import GIGACHAT_AUTH_URL, GIGACHAT_CLIENT_SECRET, GIGACHAT_CHAT_URL

load_dotenv()

def get_access_token():
    headers = {
        "Authorization": f"Basic {GIGACHAT_CLIENT_SECRET}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": str(uuid.uuid4()),
    }
    data = {"scope": "GIGACHAT_API_PERS"}
    response = requests.post(GIGACHAT_AUTH_URL, headers=headers, data=data, verify=False)
    response.raise_for_status()
    return response.json()["access_token"]

def ask_gigachat(prompt, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "GigaChat:latest",
        "messages": [{"role": "user", "content": prompt}],
    }
    resp = requests.post(GIGACHAT_CHAT_URL, headers=headers, json=data, verify=False)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
