from pydantic import BaseModel


class BedCreate(BaseModel):
    __tablename__ = "bed"
    id: int
    room_id: int
    welling_house_id: int
    soldier_id: int
