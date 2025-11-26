from abc import ABC, abstractmethod
from typing import List

from sqlmodel import Session, select

from app_api.models import WellingHouse, Room


class WellingHouseRepository(ABC):
    @abstractmethod
    def ensure_default_dorms(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[WellingHouse]:
        raise NotImplementedError


class SQLiteDormRepository(WellingHouseRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def ensure_default_dorms(self) -> None:
        existing = self.session.exec(select(WellingHouse)).all()
        if existing:
            return

        for name in ("Dorm A", "Dorm B"):
            dorm = WellingHouse(name=name, rooms_count=10, room_capacity=8)
            self.session.add(dorm)
            for i in range(1, 11):
                room = Room(
                    dorm_name=name,
                    room_number=i,
                    capacity=8,
                )
                self.session.add(room)
        self.session.commit()

    def get_all(self) -> List[WellingHouse]:
        return self.session.exec(select(WellingHouse)).all()
