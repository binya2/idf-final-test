from abc import ABC, abstractmethod
from typing import List

from sqlmodel import Session, select

from app_api.models import WellingHouse, Room


class WellingHouseRepository(ABC):
    @abstractmethod
    def ensure_default_welling_house(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[WellingHouse]:
        raise NotImplementedError


class SQLiteWellingHouseRepository(WellingHouseRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def ensure_default_welling_house(self) -> None:
        existing = self.session.exec(select(WellingHouse)).first()
        if existing:
            return

        for name in ("Dorm A", "Dorm B"):
            welling_house = WellingHouse(name=name, rooms_count=10, room_capacity=8)
            self.session.add(welling_house)
            self.session.flush()
            for i in range(1, welling_house.rooms_count + 1):
                room = Room(
                    room_number=i,  # לפי הסכמה שלך
                    capacity=welling_house.room_capacity,
                    welling_house_id=welling_house.id,
                )
                self.session.add(room)
        self.session.commit()

    def get_all(self) -> List[WellingHouse]:
        return self.session.exec(select(WellingHouse)).all()
