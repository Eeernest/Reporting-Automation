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

  def create_access_token_payload(self, user_data: dict) -> dict:
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token_payload = {
      "sub": str(user_data["sub"]),
      "role": user_data["role"],
      "exp": int(expires.timestamp()),
      "jti": str(uuid.uuid4()),
      "refresh": False
    }

    return access_token_payload

  def create_refresh_token_payload(self, user_data: dict) -> dict:
    expires = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    refresh_token_payload = {
      "sub": str(user_data["sub"]),
      "role": user_data["role"],
      "exp": int(expires.timestamp()),
      "jti": str(uuid.uuid4()),
      "refresh": True
    }

    return refresh_token_payload

  def encode_jwt_token(self, token_payload: dict) -> str:
    return jwt.encode(token_payload, settings.SECRET_KEY, settings.ALGORITHM)