from abc import ABC, abstractmethod
from typing import List

from sqlmodel import Session, select

from app_api.models import Soldier, Room, AssignmentStatusEnum


class RoomRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Room]:
        raise NotImplementedError

    @abstractmethod
    def clear_all_assignments(self) -> None:
        raise NotImplementedError


class SQLiteRoomRepository(RoomRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> List[Room]:
        return self.session.exec(select(Room)).all()

    def clear_all_assignments(self) -> None:
        soldiers = self.session.exec(select(Soldier)).all()
        for s in soldiers:
            s.welling_house_id = None
            s.room_id = None
            s.status = AssignmentStatusEnum.WAITING
            self.session.add(s)
        self.session.commit()
