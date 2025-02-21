import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware

DATABASE_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql+asyncpg://", 1)

metadata = MetaData()

scores = Table(
    "scores",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user_id", String, index=True),
    Column("score", Integer, default=0),
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Score(BaseModel):
    user_id: str
    score: int

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

@app.post("/api/score")
async def submit_score(score: Score):
    async with async_session() as session:
        query = scores.insert().values(user_id=score.user_id, score=score.score)
        await session.execute(query)
        await session.commit()
    return {"message": "Score submitted successfully!"}

@app.get("/api/user_score")
async def get_user_score(user_id: str):
    async with async_session() as session:
        query = scores.select().where(scores.c.user_id == user_id)
        result = await session.execute(query)
        user_score = result.fetchone()
        if not user_score:
            raise HTTPException(status_code=404, detail="User score not found")
        return {"score": user_score.score}

@app.get("/api/leaderboard")
async def get_leaderboard():
    async with async_session() as session:
        query = scores.select().order_by(scores.c.score.desc()).limit(10)
        result = await session.execute(query)
        leaderboard = [{"username": row.user_id, "score": row.score} for row in result]
        return {"leaderboard": leaderboard}
