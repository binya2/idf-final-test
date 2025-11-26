from typing import Literal

from fastapi import APIRouter, UploadFile, File, Depends
from sqlmodel import Session, select

from app_api.db.base import AbstractDB
from app_api.db.session import get_db
from app_api.models.dal_models import SQLiteSoldierRepository
from app_api.models.models import Soldier, Room, AssignmentStatusEnum
from app_api.routes.handler import _build_repositories_and_session, _get_strategy
from app_api.utils.file_service import parse_soldiers_csv

router = APIRouter()

router = APIRouter( tags=["appendWithCsv"])

@router.post("/appendWithCsv")
async def append_with_csv(
        file: UploadFile = File(...),
        db: AbstractDB = Depends(get_db),
        strategy: Literal["distance", "distanceThenRank"] = "distance",
) -> dict:
    content = (await file.read()).decode("utf-8")
    new_soldiers = parse_soldiers_csv(content)

    session_ctx, session, s_repo, _, _ = _build_repositories_and_session(db)
    try:
        result = _append_and_assign_new_soldiers(
            session=session,
            soldier_repo=s_repo,
            new_soldiers=new_soldiers,
            strategy_name=strategy,
        )
    finally:
        session_ctx.__exit__(None, None, None)

    return result


def _append_and_assign_new_soldiers(
        session: Session,
        soldier_repo: SQLiteSoldierRepository,
        new_soldiers: list[Soldier],
        strategy_name: str,
) -> dict:
    existing_pns = _get_existing_personal_numbers(session)
    to_insert = [s for s in new_soldiers if s.personal_number not in existing_pns]

    soldier_repo.upsert_many(to_insert)

    rooms = session.exec(select(Room)).all()
    occupancy = _calculate_occupancy(session, rooms)

    assigned_now, waiting_now = _assign_only_new_soldiers(
        session=session,
        rooms=rooms,
        occupancy=occupancy,
        new_soldiers=to_insert,
        strategy_name=strategy_name,
    )

    session.commit()

    return {
        "assigned_new": assigned_now,
        "waiting_new": waiting_now,
        "ignored_existing_personal_numbers": list(existing_pns),
    }


def _get_existing_personal_numbers(session: Session) -> set[str]:
    rows = session.exec(select(Soldier.personal_number)).all()
    return {pn for pn in rows}


def _calculate_occupancy(
        session: Session, rooms: list[Room]
) -> dict[int, int]:
    occupancy = {r.id: 0 for r in rooms}
    soldiers_all = session.exec(select(Soldier)).all()
    for s in soldiers_all:
        if s.room_id is not None:
            occupancy[s.room_id] += 1
    return occupancy


def _assign_only_new_soldiers(
        session: Session,
        rooms: list[Room],
        occupancy: dict[int, int],
        new_soldiers: list[Soldier],
        strategy_name: str,
) -> tuple[int, int]:
    strat = _get_strategy(strategy_name)
    sorted_new = strat.sort_soldiers(new_soldiers)

    BASE_CAPACITY = 160
    currently_assigned = session.exec(
        select(Soldier).where(
            Soldier.status == AssignmentStatusEnum.ASSIGNED
        )
    ).count()

    assigned_now = 0
    waiting_now = 0

    for soldier in sorted_new:
        if currently_assigned + assigned_now >= BASE_CAPACITY:
            _mark_as_waiting_for_append(session, soldier)
            waiting_now += 1
            continue

        allocated = _try_allocate_in_append(
            session, soldier, rooms, occupancy
        )

        if allocated:
            assigned_now += 1
        else:
            _mark_as_waiting_for_append(session, soldier)
            waiting_now += 1

    return assigned_now, waiting_now


def _try_allocate_in_append(
        session: Session,
        soldier: Soldier,
        rooms: list[Room],
        occupancy: dict[int, int],
) -> bool:
    for room in rooms:
        if occupancy[room.id] < room.capacity:
            soldier_orm = session.get(Soldier, soldier.personal_number)
            soldier_orm.room_id = room.id
            soldier_orm.dorm_name = room.dorm_name
            soldier_orm.status = AssignmentStatusEnum.ASSIGNED
            session.add(soldier_orm)
            occupancy[room.id] += 1
            return True
    return False


def _mark_as_waiting_for_append(session: Session, soldier: Soldier) -> None:
    soldier_orm = session.get(Soldier, soldier.personal_number)
    soldier_orm.status = AssignmentStatusEnum.WAITING
    soldier_orm.dorm_name = None
    soldier_orm.room_id = None
    session.add(soldier_orm)
