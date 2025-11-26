from __future__ import annotations

import csv
from io import StringIO
from typing import List

from app_api.models import Soldier

CSV_HEADERS = [
    "מספר אישי",
    "שם פרטי",
    "שם משפחה",
    "מין",
    "עיר מגורים",
    "מרחק מהבסיס",
]


def parse_soldiers_csv(content: str) -> List[Soldier]:
    reader = csv.DictReader(StringIO(content))
    _validate_headers(reader.fieldnames)

    result: List[Soldier] = []
    for index, row in enumerate(reader, start=2):
        soldier = _parse_row_to_soldier(row, line_number=index)
        if soldier is not None:
            result.append(soldier)

    return result


def _validate_headers(fieldnames: list[str] | None) -> None:
    if fieldnames is None:
        return
    if "מספר אישי" not in fieldnames:
        raise ValueError("CSV חסר שדה חובה: 'מספר אישי'")


def _parse_row_to_soldier(row: dict[str, str], line_number: int, ) -> Soldier | None:
    personal_number = (row.get("מספר אישי") or "").strip()
    if not personal_number:
        return None

    first_name = (row.get("שם פרטי") or "").strip()
    last_name = (row.get("שם משפחה") or "").strip()
    gender = (row.get("מין") or "").strip()
    city = (row.get("עיר מגורים") or "").strip()
    distance_raw = (row.get("מרחק מהבסיס") or "").strip()

    try:
        distance_km = int(distance_raw)
    except ValueError:
        return None

    return Soldier(
        personal_number=personal_number,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        city=city,
        distance_km=distance_km,
        rank=None,
    )
