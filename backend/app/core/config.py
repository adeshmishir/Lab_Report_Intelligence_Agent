from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "LabLens"
    APP_VERSION: str = "0.2.0"
    DEBUG: bool = False

    DATABASE_URL: str = "postgresql://lablens:lablens@localhost:5432/lablens"
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_MIME_TYPES: list[str] = ["application/pdf", "image/jpeg", "image/png"]

    # LLM-based parsing. Leave LLM_API_KEY empty to use the deterministic parser.
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_BASE_URL: str = ""
    EXTRACTION_MODE: str = "auto"  # auto | llm | deterministic

    # OCR backend. rapidocr runs fully locally with bundled models.
    OCR_BACKEND: str = "rapidocr"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()