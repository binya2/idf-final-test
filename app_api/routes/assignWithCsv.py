from fastapi import APIRouter, UploadFile, File

from app_api.utils.file_service import process_file

router = APIRouter(prefix="/assignWithCsv", tags=["assignWithCsv"])


@router.post("/upload")
def upload_users_file(file: UploadFile = File(...), has_header: bool = True):
    file_details = process_file(file, has_header)
    if file_details["content_type"] == "csv":
        header = file_details["header"]
        data = [
            dict(zip(header, row))
            for row in file_details["data"]
        ]
    else:
        data = file_details["data"]
    print(file_details)
    return data
