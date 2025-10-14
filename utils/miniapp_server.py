from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from database_function.db_core import get_db
from database_function.models import Leaderboard
from sqlalchemy import select
import os
from starlette.responses import HTMLResponse, RedirectResponse

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
miniapp_dir = os.path.join(BASE_DIR, "miniapp")

app.mount("/miniapp_static", StaticFiles(directory=miniapp_dir), name="miniapp_static")

@app.get("/")
async def root():
    return RedirectResponse(url="/miniapp")

@app.get("/miniapp")
async def miniapp():
    index_path = os.path.join(miniapp_dir, "index.html")
    return HTMLResponse(open(index_path, "r", encoding="utf-8").read())


@app.get("/miniapp/data")
async def leaderboard_data():
    async with get_db() as session:
        q = select(Leaderboard.username, Leaderboard.score).order_by(Leaderboard.score.desc()).limit(10)
        res = await session.execute(q)
        rows = res.all()

    return [{"username": row.username or "Аноним", "score": row.score} for row in rows]