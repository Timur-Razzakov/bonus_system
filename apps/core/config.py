from pathlib import Path

from pydantic_settings import BaseSettings


PROJECT_ROOT = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    PROJECT_NAME: str = "bonus-system"
    PORT: int = 8000

    # Logging configs
    ECHO_SQL: bool = True
    DEBUG_FAST_API: bool = False

    # Database configs
    DATABASE_URL: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    class Config:
        env_file = PROJECT_ROOT / ".env"


settings = Settings()
