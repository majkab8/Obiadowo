from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = ROOT_DIR / ".env"

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    PINECONE_API_KEY: str
    HF_TOKEN: str
    ALLOWED_ORIGINS: str = ""

    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, value: str) -> List[str]:
        return value.split(",") if value else []

    class Config:
        env_file = ENV_PATH
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()
