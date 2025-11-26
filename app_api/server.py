import uvicorn
from fastapi import FastAPI

from app_api.routes import appendWithCsv, assignWithCsv, release

app = FastAPI(title="IDF Final Test")
app.include_router(assignWithCsv)
app.include_router(appendWithCsv)
app.include_router(release)

if __name__ == "__main__":
    uvicorn.run(
        "app_api.server:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
