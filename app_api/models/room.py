from typing import List

from sqlmodel import Field, Relationship, SQLModel

from app_api.models.soldiers import Soldier
from app_api.models.welling_house import WellingHouse


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
