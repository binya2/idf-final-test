from fastapi import APIRouter, Depends
from sqlmodel import select

from app_api.DL.db.base import AbstractDB
from app_api.DL.db.config import get_db
from app_api.models import Soldier, AssignmentStatusEnum
from app_api.BL.services.assignment_strategy import DistanceStrategy

router = APIRouter(tags=["waitingList"])


@router.get("/waitingList")
def waiting_list(db: AbstractDB = Depends(get_db)) -> dict:
    with db.get_session() as session:
        waiting_orm = session.exec(
            select(Soldier).where(
                Soldier.status == AssignmentStatusEnum.WAITING
            )
        ).all()
        strat = DistanceStrategy()
        sorted_waiting = strat.sort_soldiers(waiting_orm)

    return {
        "waiting_list": [
            {
                "personal_number": s.personal_number,
                "first_name": s.first_name,
                "last_name": s.last_name,
                "city": s.city,
                "distance_km": s.distance_km,
                "rank": s.rank,
            }
            for s in sorted_waiting
        ]
    }
