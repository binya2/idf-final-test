from fastapi import APIRouter, Depends

from app_api.db.base import AbstractDB
from app_api.db.session import get_db

router = APIRouter(tags=["assignWithCsv"])


@router.post("/initializeScheme")
def initialize_scheme(db: AbstractDB = Depends(get_db)) -> dict:
    db.create_scheme()
    return {"status": "ok"}