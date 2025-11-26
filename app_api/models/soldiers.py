from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


class AssignmentStatusEnum(str, Enum):
    ASSIGNED = "ASSIGNED"
    WAITING = "WAITING"


class Soldier(SQLModel, table=True):
    __tablename__ = "soldiers"

    personal_number: str = Field(primary_key=True, index=True)
    first_name: str
    last_name: str
    gender: str
    city: str
    distance_km: int
    rank: Optional[int] = Field(default=None)

    status: AssignmentStatusEnum = Field(
        default=AssignmentStatusEnum.WAITING, index=True
    )
    dorm_name: Optional[str] = Field(default=None, foreign_key="dorms.name")
    room_id: Optional[int] = Field(default=None, foreign_key="rooms.id")
