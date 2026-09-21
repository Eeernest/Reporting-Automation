from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
  # PostgreSQL

  POSTGRES_URL: str


  # Redis

  REDIS_URL: str


  # Alembic

  ALEMBIC_DB_URL: str


  # Admin Credentials

  ADMIN_USERNAME: str = "ADMIN_USERNAME"
  ADMIN_EMAIL: str = "ADMIN_EMAIL"
  ADMIN_HASHED_PASSWORD: str = "ADMIN_HASHED_PASSWORD"


  # Login

  DUMMY_PASSWORD: str


  # JWT

  SECRET_KEY: str
  ALGORITHM: str


  # JWT Token

  ACCESS_TOKEN_EXPIRE_MINUTES: int
  REFRESH_TOKEN_EXPIRE_DAYS: int
  TOKEN_STORAGE_PATH: str


  # App URL

  APP_URL: str
  SERVICE_NAME: str


  # model config

  model_config = SettingsConfigDict(
    env_file=".env",
    extra="ignore",
    case_sensitive=True
  )


settings = Config()