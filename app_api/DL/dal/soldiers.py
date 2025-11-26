from abc import ABC, abstractmethod
from typing import Iterable, Optional, Dict
from typing import List

from sqlmodel import Session, select

from app_api.models import Soldier
from app_api.models.soldiers import AssignmentStatusEnum


class SoldierRepository(ABC):
    @abstractmethod
    def upsert_many(self, soldiers: Iterable[Soldier]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Soldier]:
        raise NotImplementedError

    @abstractmethod
    def get_waiting(self) -> List[Soldier]:
        raise NotImplementedError

    @abstractmethod
    def get_by_personal_number(self, pn: str) -> Optional[Soldier]:
        raise NotImplementedError

    @abstractmethod
    def remove_assignment(self, pn: str) -> None:
        raise NotImplementedError


class SQLiteSoldierRepository(SoldierRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def upsert_many(self, soldiers: Iterable[Soldier]) -> None:
        existing: Dict[str, Soldier] = {
            s.personal_number: s
            for s in self.session.exec(select(Soldier)).all()
        }

        for s in soldiers:
            if not s.personal_number.isdigit() or not s.personal_number.startswith("8"):
                raise Exception("Invalid number")

            if s.personal_number in existing:
                orm = existing[s.personal_number]
                orm.first_name = s.first_name
                orm.last_name = s.last_name
                orm.gender = s.gender
                orm.city = s.city
                orm.distance_km = s.distance_km
                orm.rank = s.rank
            else:
                s.status = AssignmentStatusEnum.WAITING
                self.session.add(s)

        self.session.commit()

    def get_all(self) -> List[Soldier]:
        return self.session.exec(select(Soldier)).all()

    def get_waiting(self) -> List[Soldier]:
        return self.session.exec(
            select(Soldier).where(
                Soldier.status == AssignmentStatusEnum.WAITING
            )
        ).all()

    def get_by_personal_number(self, pn: str) -> Optional[Soldier]:
        return self.session.get(Soldier, pn)

    def remove_assignment(self, pn: str) -> None:
        soldier = self.session.get(Soldier, pn)
        if not soldier:
            raise Exception("Not found")
        soldier.welling_house_id = None
        soldier.room_id = None
        soldier.status = AssignmentStatusEnum.WAITING
        self.session.add(soldier)
        self.session.commit()
