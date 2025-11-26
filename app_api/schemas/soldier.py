from enum import Enum
from typing import Optional

from pydantic import BaseModel

from .bed import Bed
from .room import Room


class PlacementStatus(Enum):
    assigned = 'assigned'
    waiting_list = 'waiting_list'

class SoldierCreate(BaseModel):
    id: int
    first_name: str
    last_name: str
    gender: str
    age: int
    city_residence: str
    distance_from_base_km: int
    placement_status: PlacementStatus
    bed_id: int


class SoldierResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    placement_status:bool
    placement: str = Optional[tuple[Room.id, Bed.id]]