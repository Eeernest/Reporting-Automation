from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
  # PostgreSQL

  POSTGRES_URL: str


  # Alembic

  ALEMBIC_DB_URL: str


  # model config

  model_config = SettingsConfigDict(
    env_file=".env",
    extra="ignore",
    case_sensitive=True
  )


settings = Config()