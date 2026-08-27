from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from shared.db.session import get_db
from shared.db.models import Badge, UserBadge
import uuid

router = APIRouter()

BADGE_DEFINITIONS = [
    {"code":"FIRST_SCAN",  "name":"First Scan",    "icon":"🌱", "description":"Complete your first scan",         "scans_req":1,  "points_req":0    },
    {"code":"RECYCLER",    "name":"Recycler",       "icon":"♻️", "description":"Correctly recycle 10 items",       "scans_req":10, "points_req":0    },
    {"code":"ECO_WARRIOR", "name":"Eco Warrior",    "icon":"🌍", "description":"Complete 50 correct disposals",    "scans_req":50, "points_req":0    },
    {"code":"POINTS_500",  "name":"500 Club",       "icon":"⭐", "description":"Earn 500 points",                 "scans_req":0,  "points_req":500  },
    {"code":"POINTS_1000", "name":"Points Master",  "icon":"🏆", "description":"Earn 1000 points",                "scans_req":0,  "points_req":1000 },
    {"code":"HAZARD_HERO", "name":"Hazard Hero",    "icon":"⚠️", "description":"Correctly dispose hazardous waste","scans_req":0,  "points_req":0    },
    {"code":"STREAK_7",    "name":"7-Day Streak",   "icon":"🔥", "description":"Scan every day for 7 days",       "scans_req":0,  "points_req":0    },
]

@router.post("/seed")
def seed_badges(db: Session = Depends(get_db)):
    """Seed badge definitions into DB — run once."""
    for b in BADGE_DEFINITIONS:
        existing = db.query(Badge).filter(Badge.code == b["code"]).first()
        if not existing:
            db.add(Badge(**b))
    db.commit()
    return {"message": f"✅ {len(BADGE_DEFINITIONS)} badges seeded"}

@router.get("/")
def list_badges(db: Session = Depends(get_db)):
    return db.query(Badge).all()

@router.get("/user/{user_id}")
def get_user_badges(user_id: uuid.UUID, db: Session = Depends(get_db)):
    all_badges   = db.query(Badge).all()
    earned_ids   = {ub.badge_id for ub in db.query(UserBadge).filter(
                    UserBadge.user_id == user_id).all()}
    return [
        {
            "id"         : b.id,
            "code"       : b.code,
            "name"       : b.name,
            "icon"       : b.icon,
            "description": b.description,
            "earned"     : b.id in earned_ids,
        }
        for b in all_badges
    ]