from enum import Enum

from pydantic import BaseModel

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
    PlacementStatus: PlacementStatus
    bed_id: int
