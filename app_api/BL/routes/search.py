from fastapi import APIRouter, Depends, Query, HTTPException

from app_api.DL.db import AbstractDB
from app_api.DL.db import get_db
from app_api.models import Soldier, AssignmentStatusEnum

router = APIRouter(tags=["space"])


@router.get("/search")
def search_soldier(
        personal_number: str = Query(...),
        db: AbstractDB = Depends(get_db),
) -> dict:
    with db.get_session() as session:
        s = session.get(Soldier, personal_number)
        if not s:
            raise HTTPException(status_code=404, detail="Soldier not found")

        assigned = s.status == AssignmentStatusEnum.ASSIGNED
        in_waiting = s.status == AssignmentStatusEnum.WAITING

    return {
        "personal_number": s.personal_number,
        "first_name": s.first_name,
        "last_name": s.last_name,
        "assigned": assigned,
        "welling_house_id": s.welling_house_id,
        "room_number": s.room_id,
        "in_waiting_list": in_waiting,
    }
