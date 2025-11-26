from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .room import Room
    from .soldier import Soldier


class Bed(SQLModel, table=True):
    __tablename__ = "bed"
    id: Optional[int] = Field(default=None, primary_key=True)
    room_id: Optional[int] = Field(default=None, foreign_key="Room.id")
    room: Optional["Room"] = Relationship(back_populates="bed", sa_relationship_kwargs={"uselist": False})
    soldier_id: Optional[int] = Field(default=None, foreign_key="Soldier.id")
    soldier: Optional["Soldier"] = Relationship(back_populates="bed", sa_relationship_kwargs={"uselist": False})
