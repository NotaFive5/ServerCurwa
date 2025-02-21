from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
