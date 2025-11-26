from pydantic import BaseModel


class RoomCreate(BaseModel):
    id: int
    num_of_bad: int
    welling_house_id: int
