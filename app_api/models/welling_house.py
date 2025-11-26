from typing import List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app_api.models.room import Room



class WellingHouse(SQLModel, table=True):
    __tablename__ = "welling_house"

    name: str = Field(primary_key=True)
    rooms_count: int = Field(default=10)
    room_capacity: int = Field(default=8)

    rooms: List["Room"] = Relationship(back_populates="dorm")

