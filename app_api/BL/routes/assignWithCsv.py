from typing import Literal

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from starlette import status


from app_api.BL.routes.handler import _build_repositories_and_session, _get_strategy
from app_api.BL.services import AssignmentService
from app_api.BL.utils.file_service import parse_soldiers_csv
from app_api.DL.db.base import AbstractDB
from app_api.DL.db.session import get_db

router = APIRouter(tags=["assignWithCsv"])


@router.post("/assignWithCsv")
async def assign_with_csv(
        file: UploadFile = File(...),
        strategy: Literal["distance", "distanceThenRank"] = "distance",
        db: AbstractDB = Depends(get_db),
) -> dict:
    content = (await file.read()).decode("utf-8")
    soldiers = parse_soldiers_csv(content)

    session_ctx, session, s_repo, w_h_repo, r_repo = _build_repositories_and_session(db)
    try:
        strat = _get_strategy(strategy)
        service = AssignmentService(
            soldier_repo=s_repo,
            welling_house_repo=w_h_repo,
            room_repo=r_repo,
            session=session,
            strategy=strat,
        )
        result = service.assign_from_soldiers(soldiers)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    finally:
        session_ctx.__exit__(None, None, None)

    return result
