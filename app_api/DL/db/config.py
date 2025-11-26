from contextlib import contextmanager
from typing import Iterator

from pydantic import BaseSettings
from sqlmodel import create_engine, SQLModel, Session

from app_api.DL.db.base import AbstractDB


class Settings(BaseSettings):
    app_name: str = "Intelligence Reports API"
    database_url: str = "sqlite:///sqliteDB.db"


settings = Settings()


class SQLiteDB(AbstractDB):
    def __init__(self, url: str = "sqlite:///./seven_shibolim.db") -> None:
        self._engine = create_engine(
            url, echo=False, connect_args={"check_same_thread": False}
        )

    def create_scheme(self) -> None:
        SQLModel.metadata.create_all(self._engine)

    @contextmanager
    def get_session(self) -> Iterator[Session]:
        with Session(self._engine) as session:
            yield session

    def dispose(self) -> None:
        self._engine.dispose()


def get_db() -> AbstractDB:
    return SQLiteDB(settings.database_url)
