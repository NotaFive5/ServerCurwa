from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Модель данных для очков пользователя
class UserScore(BaseModel):
    user_id: int
    score: int

# Хранилище данных (в памяти)
scores = {}
leaderboard = []

# Эндпоинт для получения счёта пользователя
@app.get("/user_score")
def get_user_score(user_id: int):
    if user_id in scores:
        return {"score": scores[user_id]}
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Эндпоинт для обновления счёта пользователя
@app.post("/update_score")
def update_user_score(user_score: UserScore):
    scores[user_score.user_id] = user_score.score
    leaderboard.append({"username": f"User{user_score.user_id}", "score": user_score.score})
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    return {"message": "Score updated successfully"}

# Эндпоинт для получения таблицы лидеров
@app.get("/leaderboard")
def get_leaderboard():
    return {"leaderboard": leaderboard[:10]}  # Топ-10 игроков
