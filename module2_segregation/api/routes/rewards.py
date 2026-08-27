from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from shared.db.session import get_db
from shared.db.models import User, DisposalEvent

router = APIRouter(prefix="/api/v2", tags=["rewards"])

@router.get("/rewards/{phone}")
async def get_rewards(phone: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == phone).first()
    if not user:
        return JSONResponse({
            "user": {
                "name"           : "New User",
                "phone"          : phone,
                "total_points"   : 0,
                "accuracy"       : 0,
                "total_disposals": 0,
            },
            "badges" : [],
            "history": [],
        })

    history  = db.query(DisposalEvent)\
                 .filter(DisposalEvent.user_id == user.id)\
                 .order_by(DisposalEvent.disposed_at.desc())\
                 .limit(10).all()

    total    = len(history)
    correct  = sum(1 for h in history if h.was_correct)
    accuracy = round((correct / total * 100) if total else 0, 1)

    from module2_segregation.api.routes.disposal import check_badges
    badges = check_badges(user.reward_points)

    return JSONResponse({
        "user": {
            "name"           : user.name,
            "phone"          : user.phone,
            "total_points"   : user.reward_points,
            "accuracy"       : accuracy,
            "total_disposals": total,
        },
        "badges" : badges,
        "history": [
            {
                "waste_type" : h.waste_type,
                "was_correct": h.was_correct,
                "points"     : h.points_earned,
                "time"       : str(h.disposed_at),
            } for h in history
        ],
    })