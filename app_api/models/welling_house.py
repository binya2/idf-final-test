from typing import List

from sqlmodel import SQLModel, Field, Relationship


class WellingHouse(SQLModel, table=True):
    __tablename__ = "welling_house"
    id: int = Field(primary_key=True)
    name: str
    rooms_count: int = Field(default=10)
    room_capacity: int = Field(default=8)

    rooms: List["Room"] = Relationship(back_populates="welling_house")
