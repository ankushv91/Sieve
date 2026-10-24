from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "SoloBuildAI"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    POSTGRES_HOST: str = ""
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str = ""

    AWS_BUCKET_NAME: str = ""
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = ""

    AI_EMBEDDING_PROVIDER: str = "gemini"
    GEMINI_API_KEY: str = ""
    CORS_ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]
    GEMINI_EXTRACTION_MODEL: str = ""
    GEMINI_CHAT_MODEL: str = "gemini-2.0-flash"
    GEMINI_SUMMARY_MODEL: str = "gemini-2.0-flash-lite"
    LLM_REQUEST_TIMEOUT_SECONDS: int = 180
    LLM_MAX_RETRIES: int = 2
    LLM_RETRY_DELAY_SECONDS: float = 2.0
    WORKER_MAX_TRIES: int = 3
    ARQ_JOB_TIMEOUT_SECONDS: int = 1800

    REDIS_URL: str = "redis://localhost:6379"

    # Resume & CSV pipeline
    CSV_CHUNK_SIZE: int = 50
    RESUME_MAX_FILE_COUNT: int = 500
    ZIP_MAX_UNCOMPRESSED_BYTES: int = 500 * 1024 * 1024
    ZIP_MAX_RATIO: int = 50

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


settings = Settings()