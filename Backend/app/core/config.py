from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Bullock Backend"
    DEBUG: bool = True

    # Database (async)
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@db:5432/bullock"
    )

    # Redis & Celery
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"

    # Auth
    SECRET_KEY: str = "CHANGE_ME_TO_A_LONG_RANDOM_SECRET"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    JWT_ALGORITHM: str = "HS256"

    # LLM / Embeddings
    OPENAI_API_KEY: str = ""          # set in .env
    LLM_MODEL: str = "gpt-4o-mini"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"


settings = Settings()
