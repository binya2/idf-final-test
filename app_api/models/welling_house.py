from typing import Optional, List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .room import Room


class WellingHouse(SQLModel, table=True):
    __tablename__ = "welling_house"
    id: Optional[int] = Field(default=None, primary_key=True)
    num_of_rooms: Optional[int] = Field(default=None)

    rooms: List["Room"] = Relationship(back_populates="welling_house", link_model=Room)
