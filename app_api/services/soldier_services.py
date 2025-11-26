from typing import Optional

from sqlmodel import Session, select

from app_api.models import Soldier
from app_api.schemas.soldier import SoldierCreate


def import_from_dict(session: Session, records):
    print("import_from_dict:")
    print(records)
    soldiers = [Soldier(**record) for record in records]
    session.add_all(soldiers)
    session.commit()

    for u in soldiers:
        session.refresh(u)

    return soldiers

def create_soldier(session: Session, soldier_in: SoldierCreate) -> Optional[Soldier]:
    statement = select(Soldier).where(Soldier.first_name == soldier_in.first_name,
                                      Soldier.last_name == soldier_in.last_name,
                                      Soldier.gender == soldier_in.gender,
                                      Soldier.age == soldier_in.age,
                                      Soldier.city_residence == soldier_in.city_residence,
                                      Soldier.distance_from_base_km == soldier_in.distance_from_base_km,)

    existing_user = session.exec(statement).first()

    if existing_user:
        return None

    soldier = Soldier(**soldier_in.dict())
    session.add(soldier)
    session.commit()
    session.refresh(soldier)
    return soldier
