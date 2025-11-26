from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from app_api.models.bed import Bed

if TYPE_CHECKING:
    from .bed import Bed


class Soldier(SQLModel, table=True):
    __tablename__ = "soldier"
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    gender: str
    age: int
    city_residence: str
    distance_from_base_km: int
    placement_status: str
    bed: Optional["Bed"] = Relationship(back_populates="soldier", sa_relationship_kwargs={"uselist": False})
