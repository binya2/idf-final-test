from typing import Tuple

from sqlmodel import Session

from app_api.db.base import AbstractDB
from app_api.models.dal_models import SQLiteSoldierRepository, SQLiteDormRepository, SQLiteRoomRepository
from app_api.services.assignment_strategy import AssignmentStrategy, DistanceStrategy, DistanceThenRankStrategy


def _get_strategy(name: str) -> AssignmentStrategy:
    if name == "distance":
        return DistanceStrategy()
    if name == "distanceThenRank":
        return DistanceThenRankStrategy()
    raise ValueError(f"unknown strategy: {name}")


def _build_repositories_and_session(
        db: AbstractDB,
) -> Tuple[object, Session, SQLiteSoldierRepository, SQLiteDormRepository, SQLiteRoomRepository]:
    session_ctx = db.get_session()
    session = session_ctx.__enter__()
    s_repo = SQLiteSoldierRepository(session)
    d_repo = SQLiteDormRepository(session)
    r_repo = SQLiteRoomRepository(session)
    return session_ctx, session, s_repo, d_repo, r_repo

