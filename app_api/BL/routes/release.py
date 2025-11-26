from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app_api.DL.db import AbstractDB
from app_api.DL.db import get_db
from app_api.BL.routes.assignWithCsv import _build_repositories_and_session, _get_strategy
from app_api.BL.services.release_service import ReleaseService

router = APIRouter(tags=["release"])


@router.post("/release")
def release_soldier(
        personal_number: str,
        strategy: Literal["distance", "distanceThenRank"] = "distance",
        db: AbstractDB = Depends(get_db),
) -> dict:
    session_ctx, session, s_repo, _, _ = _build_repositories_and_session(db)
    try:
        strat = _get_strategy(strategy)
        service = ReleaseService(
            soldier_repo=s_repo,
            session=session,
            strategy=strat,
        )
        service.release_and_fill_next(personal_number)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    finally:
        session_ctx.__exit__(None, None, None)

    return {"status": "ok"}
