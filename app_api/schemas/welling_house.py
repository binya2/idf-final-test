from typing import  List

from pydantic import BaseModel



class WellingHouse(BaseModel):
    id: int
    num_of_rooms: int
    room_ids: List[int]