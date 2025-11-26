from typing import List

from sqlmodel import Field, Relationship, SQLModel

from app_api.models.welling_house import WellingHouse


class Room(SQLModel, table=True):
    __tablename__ = "rooms"

    id: int = Field(primary_key=True)
    room_number: int
    capacity: int = Field(default=8)

    welling_house_id: int = Field(foreign_key="welling_house.id")
    welling_house: WellingHouse = Relationship(back_populates="rooms")

    soldiers: List["Soldier"] = Relationship(back_populates="room")
