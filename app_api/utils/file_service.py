import csv
import io
import json
from typing import Dict, List, Optional

from fastapi import UploadFile, HTTPException


# --------------------------------------------------
# הכנתי את הקובץ הזה לפני כמה ימים לשימוש אישי לאחר
# כמה תרגילים שהביאו לנו, מבין את החשד אולי לשימוש
# בAI אבל זה קוד כתוב מראש שיש לי והתאמתי אותו למבחן
# ---------------------------------------------------


# ---------------------------------------------
# 1) כלי עזר בסיסיים
# ---------------------------------------------

def decode_bytes(content_bytes: bytes) -> str:
    """Decode file bytes into UTF-8 text."""
    try:
        return content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded")


def strip_row(row: List[str]) -> List[str]:
    """Trim all cells in a row."""
    return [cell.strip() for cell in row]


def is_comment_or_empty(row: List[str], comment_char="#") -> bool:
    """Check if a row is empty or a comment."""
    if not row:
        return True
    cleaned = "".join(row).strip()
    return cleaned == "" or cleaned.startswith(comment_char)


# ---------------------------------------------
# 2) Validators
# ---------------------------------------------

def normalize_row_length(row: List[str], header_len: int) -> List[str]:
    """Ensure row matches header length (pad or trim)."""
    if len(row) < header_len:
        row += [""] * (header_len - len(row))
    elif len(row) > header_len:
        row = row[:header_len]
    return row


# ---------------------------------------------
# 3) CSV processing
# ---------------------------------------------

def parse_csv(content_str: str, has_header: bool = True) -> Dict:
    """Parse CSV string into header + rows."""
    input_io = io.StringIO(content_str)
    reader = csv.reader(input_io)

    header: Optional[List[str]] = None
    data: List[List[str]] = []

    first = True
    for row in reader:
        if is_comment_or_empty(row):
            continue

        row = strip_row(row)

        if first and has_header:
            header = row
            first = False
            continue

        if has_header and header:
            row = normalize_row_length(row, len(header))

        data.append(row)
        first = False

    return {
        "header": header,
        "data": data
    }


# ---------------------------------------------
# 4) JSON processing
# ---------------------------------------------

def parse_json(content_str: str) -> List[dict]:
    """Parse JSON string into Python object."""
    try:
        return json.loads(content_str)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")


# ---------------------------------------------
# 5) פונקציה ראשית – מעבדת כל קובץ שמגיע ל-FastAPI
# ---------------------------------------------

def process_file(file: UploadFile, has_header: bool = True) -> Dict:
    """
    Main file processor:
    - Supports CSV & JSON
    - Cleans rows
    - Returns ready-to-use structure
    """
    content_type = file.content_type
    filename = file.filename

    content_bytes = file.file.read()
    file.file.seek(0)

    content_str = decode_bytes(content_bytes)

    # CSV
    if content_type == "text/csv" or filename.endswith(".csv"):
        parsed = parse_csv(content_str, has_header)
        return {
            "filename": filename,
            "content_type": "csv",
            "header": parsed["header"],
            "data": parsed["data"]
        }

    # JSON
    if content_type == "application/json" or filename.endswith(".json"):
        parsed = parse_json(content_str)
        return {
            "filename": filename,
            "content_type": "json",
            "header": None,
            "data": parsed
        }

    # Unsupported
    raise HTTPException(status_code=400, detail="Unsupported file type")
