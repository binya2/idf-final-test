import uvicorn
from fastapi import FastAPI

from app_api.routes import assignWithCsv

app = FastAPI(title="IDF Final Test")
app.include_router(assignWithCsv)


if __name__ == "__main__":
    uvicorn.run(
        "app_api.server:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
