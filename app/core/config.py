from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
  # PostgreSQL

  POSTGRES_URL: str


  # Alembic

  ALEMBIC_DB_URL: str


  # Admin Credentials

  ADMIN_USERNAME: str = "ADMIN_USERNAME"
  ADMIN_EMAIL: str = "ADMIN_EMAIL"
  ADMIN_HASHED_PASSWORD: str = "ADMIN_HASHED_PASSWORD"


  # model config

  model_config = SettingsConfigDict(
    env_file=".env",
    extra="ignore",
    case_sensitive=True
  )


settings = Config()