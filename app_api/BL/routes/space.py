from fastapi import APIRouter, Depends
from sqlmodel import select

from app_api.DL.db import AbstractDB
from app_api.DL.db import get_db
from app_api.models import Soldier, Room, WellingHouse

router = APIRouter(tags=["space"])


@router.get("/space")
def space_report(db: AbstractDB = Depends(get_db)) -> dict:
    with db.get_session() as session:
        dorms = session.exec(select(WellingHouse)).all()
        rooms = session.exec(select(Room)).all()
        soldiers = session.exec(select(Soldier)).all()

        occupancy = {r.id: 0 for r in rooms}
        for s in soldiers:
            if s.room_id is not None:
                occupancy[s.room_id] += 1

        result: dict[str, dict[str, int]] = {}
        for dorm in dorms:
            dorm_rooms = [r for r in rooms if r.dorm_name == dorm.name]
            full = partial = empty = 0
            for r in dorm_rooms:
                occ = occupancy[r.id]
                if occ == 0:
                    empty += 1
                elif occ >= r.capacity:
                    full += 1
                else:
                    partial += 1
            result[dorm.name] = {
                "full_rooms": full,
                "partial_rooms": partial,
                "empty_rooms": empty,
            }

    return result
