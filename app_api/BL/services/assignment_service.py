from typing import Iterable

from dataclasses import dataclass
from sqlmodel import Session

from app_api.BL.services.assignment_strategy import AssignmentStrategy
from app_api.DL.dal.room import RoomRepository
from app_api.DL.dal.soldiers import SoldierRepository
from app_api.DL.dal.welling_house import WellingHouseRepository

MAX_BASE_CAPACITY = 160


@dataclass
class AssignmentCounters:
    assigned: int = 0
    waiting: int = 0

class AssignmentService:
    def __init__(
        self,
        soldier_repo: SoldierRepository,
        dorm_repo: WellingHouseRepository,
        room_repo: RoomRepository,
        session: Session,
        strategy: AssignmentStrategy,
    ) -> None:
        self.soldier_repo = soldier_repo
        self.dorm_repo = dorm_repo
        self.room_repo = room_repo
        self.session = session
        self.strategy = strategy

    def assign_from_soldiers(self, soldiers: Iterable[Soldier]) -> dict:
        self._prepare_dorms_and_soldiers(soldiers)

        all_soldiers = self.soldier_repo.get_all()
        sorted_soldiers = self.strategy.sort_soldiers(all_soldiers)

        rooms = self.room_repo.get_all()
        occupancy = self._calculate_initial_occupancy(rooms, all_soldiers)

        counters = AssignmentCounters()
        self._assign_sorted_soldiers(
            sorted_soldiers, rooms, occupancy, counters
        )

        self.session.commit()
        return self._build_assignment_response(sorted_soldiers, counters)

    def _prepare_dorms_and_soldiers(
        self, soldiers: Iterable[Soldier]
    ) -> None:
        self.dorm_repo.ensure_default_dorms()
        self.soldier_repo.upsert_many(soldiers)
        self.room_repo.clear_all_assignments()

    def _calculate_initial_occupancy(
        self, rooms: list[Room], soldiers: list[Soldier]
    ) -> dict[int, int]:
        occupancy: dict[int, int] = {r.id: 0 for r in rooms}
        for s in soldiers:
            if s.room_id is not None:
                occupancy[s.room_id] += 1
        return occupancy

    def _assign_sorted_soldiers(
        self,
        sorted_soldiers: list[Soldier],
        rooms: list[Room],
        occupancy: dict[int, int],
        counters: AssignmentCounters,
    ) -> None:
        for soldier in sorted_soldiers:
            if counters.assigned >= MAX_BASE_CAPACITY:
                self._mark_as_waiting(soldier)
                counters.waiting += 1
                continue

            allocated = self._try_allocate_soldier_to_any_room(
                soldier, rooms, occupancy
            )

            if allocated:
                counters.assigned += 1
            else:
                self._mark_as_waiting(soldier)
                counters.waiting += 1

    def _try_allocate_soldier_to_any_room(
        self,
        soldier: Soldier,
        rooms: list[Room],
        occupancy: dict[int, int],
    ) -> bool:
        for room in rooms:
            if occupancy[room.id] < room.capacity:
                self._assign_to_room(soldier, room)
                occupancy[room.id] += 1
                return True
        return False

    def _assign_to_room(self, soldier: Soldier, room: Room) -> None:
        soldier.room_id = room.id
        soldier.dorm_name = room.dorm_name
        soldier.status = AssignmentStatusEnum.ASSIGNED
        self.session.add(soldier)

    def _mark_as_waiting(self, soldier: Soldier) -> None:
        soldier.status = AssignmentStatusEnum.WAITING
        soldier.dorm_name = None
        soldier.room_id = None
        self.session.add(soldier)

    def _build_assignment_response(
        self,
        sorted_soldiers: list[Soldier],
        counters: AssignmentCounters,
    ) -> dict:
        result_soldiers: list[dict] = []
        for s in sorted_soldiers:
            result_soldiers.append(
                {
                    "personal_number": s.personal_number,
                    "assigned": s.status == AssignmentStatusEnum.ASSIGNED,
                    "dorm_name": s.dorm_name,
                    "room_number": s.room_id,
                    "in_waiting_list": s.status == AssignmentStatusEnum.WAITING,
                }
            )

        return {
            "summary": {
                "total_soldiers": len(sorted_soldiers),
                "assigned_count": counters.assigned,
                "waiting_count": counters.waiting,
            },
            "soldiers": result_soldiers,
        }

