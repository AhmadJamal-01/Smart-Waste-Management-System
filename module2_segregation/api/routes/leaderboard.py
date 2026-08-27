from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from shared.db.session import get_db
from shared.db.models import User

router = APIRouter(prefix="/api/v2", tags=["leaderboard"])

@router.get("/leaderboard")
async def get_leaderboard(db: Session = Depends(get_db)):
    top_users = db.query(User)\
                  .filter(User.role == "citizen")\
                  .order_by(desc(User.reward_points))\
                  .limit(20).all()

    return JSONResponse({
        "leaderboard": [
            {
                "rank"  : i + 1,
                "name"  : u.name,
                "points": u.reward_points,
                "badge" : get_top_badge(u.reward_points),
                "zone"  : "Lahore",
            }
            for i, u in enumerate(top_users)
        ]
    })

def get_top_badge(points):
    if points >= 5000: return "⭐ Eco Legend"
    if points >= 2500: return "🌍 Planet Hero"
    if points >= 1000: return "🏆 Eco Champion"
    if points >= 500:  return "🌱 Green Recycler"
    if points >= 100:  return "♻️ Eco Starter"
    return "🆕 Newcomer"
