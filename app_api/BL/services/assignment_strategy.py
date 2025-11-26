from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, List

from app_api.models.room import Soldier


class AssignmentStrategy(ABC):
    @abstractmethod
    def sort_soldiers(self, soldiers: Iterable[Soldier]) -> List[Soldier]:
        raise NotImplementedError


class DistanceStrategy(AssignmentStrategy):
    def sort_soldiers(self, soldiers: Iterable[Soldier]) -> List[Soldier]:
        return sorted(soldiers, key=lambda s: s.distance_km, reverse=True)


class DistanceThenRankStrategy(AssignmentStrategy):
    def sort_soldiers(self, soldiers: Iterable[Soldier]) -> List[Soldier]:
        def key_func(s: Soldier) -> tuple[int, int]:
            return (s.distance_km, s.rank or 0)

        return sorted(soldiers, key=key_func, reverse=True)

