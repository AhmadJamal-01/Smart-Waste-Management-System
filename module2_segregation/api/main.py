import sys
sys.path.insert(0, r"C:\SWOS")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from shared.db.session import init_db
from module2_segregation.api.routes import rewards, badges, leaderboard, disposal

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="SWOS — Module 2: Intelligent Segregation",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(disposal.router,    prefix="",               tags=["disposal"])
app.include_router(rewards.router,     prefix="",               tags=["rewards"])
app.include_router(leaderboard.router, prefix="",               tags=["leaderboard"])
app.include_router(badges.router,      prefix="/api/v2/badges", tags=["badges"])

@app.get("/")
def root():
    return {"service": "SWOS Rewards API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok", "module": "module2_segregation"}