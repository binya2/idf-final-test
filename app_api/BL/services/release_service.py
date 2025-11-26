from sqlmodel import Session

from app_api.BL.services.assignment_strategy import AssignmentStrategy
from app_api.DL.dal.soldiers import SoldierRepository
from app_api.models import Soldier, AssignmentStatusEnum


class ReleaseService:
    def __init__(
            self,
            soldier_repo: SoldierRepository,
            session: Session,
            strategy: AssignmentStrategy,
    ) -> None:
        self.soldier_repo = soldier_repo
        self.session = session
        self.strategy = strategy

    def release_and_fill_next(self, personal_number: str) -> None:
        soldier = self._get_soldier_or_raise(personal_number)
        freed_room_id = self._release_soldier_to_waiting(soldier)

        if freed_room_id is None:
            return

        self._assign_next_from_waiting(freed_room_id)

    def _get_soldier_or_raise(self, personal_number: str) -> Soldier:
        soldier = self.soldier_repo.get_by_personal_number(personal_number)
        if not soldier:
            raise Exception(f"לא נמצא חייל לשחרור: {personal_number}")
        return soldier

    def _release_soldier_to_waiting(self, soldier: Soldier) -> int | None:
        freed_room_id = soldier.room_id
        soldier.dorm_name = None
        soldier.room_id = None
        soldier.status = AssignmentStatusEnum.WAITING
        self.session.add(soldier)
        self.session.commit()
        return freed_room_id

    def _assign_next_from_waiting(self, freed_room_id: int) -> None:
        waiting_list = self.soldier_repo.get_waiting()
        if not waiting_list:
            return

        sorted_waiting = self.strategy.sort_soldiers(waiting_list)
        next_soldier = sorted_waiting[0]

        from app_api.models.room import Room

        room = self.session.get(Room, freed_room_id)
        if room is None:
            return

        next_soldier.room_id = freed_room_id
        next_soldier.dorm_name = room.dorm_name
        next_soldier.status = AssignmentStatusEnum.ASSIGNED
        self.session.add(next_soldier)
        self.session.commit()
