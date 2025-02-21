from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Пример хранилища данных пользователей (имитация базы данных)
user_data: Dict[int, Dict[str, int]] = {}

# Модель данных пользователя
class UserScore(BaseModel):
    user_id: int
    score: int

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Railway with Docker!"}

# Эндпоинт для получения счёта пользователя
@app.get("/user_score")
def get_user_score(user_id: int):
    if user_id in user_data:
        return {"score": user_data[user_id].get("score", 0)}
    return {"score": 0}

# Эндпоинт для обновления счёта пользователя
@app.post("/update_score")
def update_user_score(user_score: UserScore):
    user_data[user_score.user_id] = {"score": user_score.score}
    return {"message": "Score updated successfully"}

# Эндпоинт для получения таблицы лидеров
@app.get("/leaderboard")
def get_leaderboard():
    sorted_leaderboard = sorted(user_data.items(), key=lambda x: x[1].get("score", 0), reverse=True)
    leaderboard = [{"username": f"User {user_id}", "score": data["score"]} for user_id, data in sorted_leaderboard]
    return {"leaderboard": leaderboard}
