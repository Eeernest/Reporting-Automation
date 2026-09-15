from datetime import datetime, timezone, timedelta
import uuid

from fastapi.concurrency import run_in_threadpool
import jwt
from pwdlib import PasswordHash

from app.core.config import settings

class Security:
  def __init__(self):
    self.hasher = PasswordHash.recommended()

  # Main Methods

  async def get_password_hash(self, password: str) -> str:
    return await run_in_threadpool(self.hasher.hash, password)

  async def verify_password(self, password: str, hashed_password: str) -> bool:
    return await run_in_threadpool(self.hasher.verify, password, hashed_password)

  async def create_access_token(self, user_data: dict) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
      "sub": user_data["sub"],
      "role": user_data["role"],
      "exp": expires,
      "jti": str(uuid.uuid4()),
      "refresh": False
    }

    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

  async def create_refresh_token(self, user_data: dict) -> str:
    expires = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    payload = {
      "sub": user_data["sub"],
      "role": user_data["role"],
      "exp": expires,
      "jti": str(uuid.uuid4()),
      "refresh": True
    }

    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)