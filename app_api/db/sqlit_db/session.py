from typing import Any, Generator

from sqlmodel import create_engine, Session, SQLModel

from app_api.core.config import settings

engine = create_engine(settings.database_url, echo=False)


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session


def init_db() -> None:
    from app_api.db.sqlit_db import models
    SQLModel.metadata.create_all(engine)
