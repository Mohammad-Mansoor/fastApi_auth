from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"   # prevents crash from unknown fields
    )
    # =====================
    # APP SETTINGS
    # =====================
    APP_NAME: str
    APP_ENV: str
    DEBUG: bool
    PORT: int

    # =====================
    # DATABASE
    # =====================
    DATABASE_URL: str

    # =====================
    # REDIS
    # =====================
    REDIS_URL: str

    # =====================
    # RABBITMQ
    # =====================
    RABBITMQ_URL: str

    # =====================
    # JWT AUTH
    # =====================
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # =========================
    # SECURITY
    # =========================
    BCRYPT_ROUNDS: int =12

    # =====================
    # FILE STORAGE (optional but useful)
    # =====================
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 10


settings = Settings()
