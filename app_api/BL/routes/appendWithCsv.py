from typing import Literal

from fastapi import APIRouter, UploadFile, File, Depends

from app_api.DL.db import AbstractDB
from app_api.DL.db.config import get_db
from app_api.BL.routes.handler import _build_repositories_and_session, _append_and_assign_new_soldiers
from app_api.BL.utils.file_service import parse_soldiers_csv

router = APIRouter(tags=["appendWithCsv"])


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
