import uvicorn
from fastapi import FastAPI

from app_api.BL.routes import *

app = FastAPI(title="IDF Final Test")
app.include_router(assignWithCsv)
app.include_router(appendWithCsv)
app.include_router(release)
app.include_router(space)
app.include_router(waitingList)
app.include_router(db)
app.include_router(search)

if __name__ == "__main__":
    uvicorn.run(
        "app_api.server:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
