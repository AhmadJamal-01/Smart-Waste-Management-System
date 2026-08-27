from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from shared.db.session import get_db
from shared.db.models import User, DisposalEvent, Alert
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/api/v2", tags=["disposal"])

POINTS_MAP = {
    "plastic"  : 10,
    "organic"  : 8,
    "metal"    : 12,
    "glass"    : 12,
    "hazardous": 20,
}

CORRECT_BIN = {
    "plastic"  : {"color": "#3B82F6", "label": "Blue Bin",   "emoji": "🔵"},
    "organic"  : {"color": "#22C55E", "label": "Green Bin",  "emoji": "🟢"},
    "metal"    : {"color": "#94A3B8", "label": "Silver Bin", "emoji": "⚪"},
    "glass"    : {"color": "#06B6D4", "label": "Cyan Bin",   "emoji": "🔵"},
    "hazardous": {"color": "#EF4444", "label": "Red Bin",    "emoji": "🔴"},
}

class DisposalRequest(BaseModel):
    user_phone : str
    waste_type : str
    was_correct: bool
    bin_id     : str = "BIN-001"

@router.post("/disposal/submit")
async def submit_disposal(req: DisposalRequest, db: Session = Depends(get_db)):
    # Get or create user
    user = db.query(User).filter(User.phone == req.user_phone).first()
    if not user:
        user = User(
            id   = uuid.uuid4(),
            name = f"User_{req.user_phone[-4:]}",
            phone= req.user_phone,
            role = "citizen",
            reward_points = 0,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Calculate points
    points = POINTS_MAP.get(req.waste_type, 5) if req.was_correct else 2
    user.reward_points += points
    db.commit()

    # Log disposal event
    event = DisposalEvent(
        user_id     = user.id,
        bin_id      = None,
        waste_type  = req.waste_type,
        was_correct = req.was_correct,
        points_earned = points,
    )
    db.add(event)
    db.commit()

    # Check badges
    badges_earned = check_badges(user.reward_points)

    return JSONResponse({
        "success"      : True,
        "points_earned": points,
        "total_points" : user.reward_points,
        "correct_bin"  : CORRECT_BIN.get(req.waste_type),
        "badges_earned": badges_earned,
        "message"      : f"✅ +{points} points!" if req.was_correct else "⚠️ Wrong bin — +2 points",
    })

@router.get("/disposal/bin-guide/{waste_type}")
async def bin_guide(waste_type: str):
    guide = CORRECT_BIN.get(waste_type.lower())
    if not guide:
        return JSONResponse({"error": "Unknown waste type"}, status_code=400)
    return JSONResponse({
        "waste_type": waste_type,
        "bin"       : guide,
        "points"    : POINTS_MAP.get(waste_type, 5),
        "tip"       : get_tip(waste_type),
    })

def get_tip(waste_type):
    tips = {
        "plastic"  : "Rinse plastic bottles before disposal",
        "organic"  : "Remove any packaging before disposing food waste",
        "metal"    : "Crush cans to save space in the bin",
        "glass"    : "Wrap broken glass in newspaper before disposal",
        "hazardous": "Never mix hazardous waste with regular bins",
    }
    return tips.get(waste_type, "Dispose responsibly")

def check_badges(points):
    badges = []
    milestones = {
        100 : {"id": "starter",    "name": "♻️ Eco Starter",    "desc": "First 100 points"},
        500 : {"id": "recycler",   "name": "🌱 Green Recycler",  "desc": "500 points reached"},
        1000: {"id": "champion",   "name": "🏆 Eco Champion",    "desc": "1000 points reached"},
        2500: {"id": "hero",       "name": "🌍 Planet Hero",     "desc": "2500 points reached"},
        5000: {"id": "legend",     "name": "⭐ Eco Legend",      "desc": "5000 points reached"},
    }
    for threshold, badge in milestones.items():
        if points >= threshold:
            badges.append(badge)
    return badges