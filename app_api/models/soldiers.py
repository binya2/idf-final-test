from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from app_api.models import Room


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

    status: AssignmentStatusEnum = Field(default=AssignmentStatusEnum.WAITING)

    welling_house_id: Optional[int] = Field(default=None, foreign_key="welling_house.id")
    room_id: Optional[int] = Field(default=None, foreign_key="rooms.id")

    room: Optional["Room"] = Relationship(back_populates="soldiers")
