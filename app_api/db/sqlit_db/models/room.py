from typing import Optional, List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .bed import Bed
    from .welling_house import WellingHouse


class Room(SQLModel, table=True):
    __tablename__ = "room"
    id: Optional[int] = Field(default=None, primary_key=True)
    num_of_bad: Optional[int] = Field(default=None)

    welling_house_id: Optional[int] = Field(default=None, foreign_key="WellingHouse.id")
    welling_house: "WellingHouse" = Relationship(back_populates="room")

    bed: List["Bed"] = Relationship(back_populates="room")
