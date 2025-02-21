from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Модель данных для приёма счёта от Unity
class ScoreData(BaseModel):
    user_id: str
    score: int

# Временное хранилище данных пользователей (вместо базы данных)
user_scores: Dict[str, int] = {}

# API для приёма данных о счёте от Unity
@app.post("/api/score")
async def receive_score(data: ScoreData):
    user_scores[data.user_id] = max(data.score, user_scores.get(data.user_id, 0))
    return {"status": "success", "message": "Score received."}

# API для получения счёта пользователя (для Telegram-бота)
@app.get("/api/user_score")
async def get_user_score(user_id: str):
    if user_id not in user_scores:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "score": user_scores[user_id]}

# API для получения таблицы лидеров (для Telegram-бота)
@app.get("/api/leaderboard")
async def get_leaderboard():
    sorted_scores = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)
    leaderboard = [{"username": user_id, "score": score} for user_id, score in sorted_scores]
    return {"leaderboard": leaderboard}

app = FastAPI()

# Настройка CORS (если ещё не добавлено)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Корневой маршрут для проверки доступности сервера
@app.get("/")
async def root():
    return {"message": "Hello from FastAPI on Railway with Docker!"}

# Пример существующих маршрутов
@app.get("/api/user_score")
async def get_user_score(user_id: int):
    # Пример возврата очков пользователя
    return {"user_id": user_id, "score": 100}

@app.get("/api/leaderboard")
async def get_leaderboard():
    # Пример данных для таблицы лидеров
    leaderboard = [
        {"username": "Player1", "score": 200},
        {"username": "Player2", "score": 150}
    ]
    return {"leaderboard": leaderboard}
