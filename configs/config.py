from pydantic import MongoDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DATABASE: str = "legal-chatbot"
    NUM_WORKER: int = 8

    class Config:
        env_file = ".env"


settings = Settings()
