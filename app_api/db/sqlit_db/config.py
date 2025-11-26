from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Intelligence Reports API"
    database_url: str = "sqlite:///sqliteDB.db"


settings = Settings()