
from enum import Enum
from typing import Optional, List

from sqlmodel import Field, Relationship, SQLModel


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


class WellingHouse(SQLModel, table=True):
    __tablename__ = "welling_house"

    name: str = Field(primary_key=True)
    rooms_count: int = Field(default=10)
    room_capacity: int = Field(default=8)

    rooms: List["Room"] = Relationship(back_populates="dorm")


class Room(SQLModel, table=True):
    __tablename__ = "rooms"

    id: int = Field(primary_key=True)
    dorm_name: str = Field(foreign_key="dorms.name", index=True)
    room_number: int
    capacity: int = Field(default=8)

    dorm: WellingHouse = Relationship(back_populates="rooms")
    soldiers: List[Soldier] = Relationship(
        back_populates="room", sa_relationship_kwargs={"lazy": "selectin"}
    )

    Soldier.room = Relationship(
        back_populates="soldiers", sa_relationship_kwargs={"lazy": "selectin"}
    )
