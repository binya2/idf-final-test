from typing import Any, Generator

from sqlmodel import create_engine, Session, SQLModel

from .base import AbstractDB
from .config import settings, SQLiteDB

engine = create_engine(settings.database_url, echo=False)


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session


def init_db() -> None:
    SQLModel.metadata.create_all(engine)

def get_db() -> AbstractDB:
    return SQLiteDB(settings.database_url)