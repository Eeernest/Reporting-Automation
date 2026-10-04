from datetime import datetime, timezone, timedelta
from typing import Any
import uuid

from fastapi.concurrency import run_in_threadpool
from fastapi.security import OAuth2PasswordBearer
import jwt
from pwdlib import PasswordHash

from app.core.config import settings
import app.core.exceptions as e
from app.core.security_types import AccessTokenPayload, RefreshTokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

access_token_header = {"typ": "at+jwt"}
refresh_token_header = {"typ": "rt+jwt"}


class Security:
  def __init__(self):
    self.hasher = PasswordHash.recommended()

  # Main Methods

  async def get_password_hash(self, password: str) -> str:
    return await run_in_threadpool(self.hasher.hash, password)

  async def verify_password(self, password: str, hashed_password: str) -> bool:
    return await run_in_threadpool(self.hasher.verify, password, hashed_password)

  def create_access_token_payload(self, user_id: int, user_role: str) -> AccessTokenPayload:
    issued = datetime.now(timezone.utc)
    expires = issued + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return AccessTokenPayload(
      iss=settings.ISS,
      sub=str(user_id),
      role=user_role,
      aud=settings.AUD,
      iat=int(issued.timestamp()),
      exp=int(expires.timestamp()),
      jti=str(uuid.uuid4())
    )

  def create_refresh_token_payload(self, user_id: int) -> RefreshTokenPayload:
    issued = datetime.now(timezone.utc)
    expires = issued + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    return RefreshTokenPayload(
      iss=settings.ISS,
      sub=str(user_id),
      aud=settings.AUD,
      iat=int(issued.timestamp()),
      exp=int(expires.timestamp()),
      jti=str(uuid.uuid4())
    )

  def get_encoded_access_token(self, access_token_payload: AccessTokenPayload) -> str:
    return self._encode_token(access_token_payload, access_token_header)

  def get_encoded_refresh_token(self, refresh_token_payload: RefreshTokenPayload) -> str:
    return self._encode_token(refresh_token_payload, refresh_token_header)

  def get_decoded_access_token(self, encoded_access_token: str) -> AccessTokenPayload:
    self._validate_token_header(encoded_access_token, access_token_header["typ"])

    decoded_access_token = self._try_decode_token(encoded_access_token)

    return AccessTokenPayload(decoded_access_token)

  def get_decoded_refresh_token(self, encoded_refresh_token: str) -> RefreshTokenPayload:
    self._validate_token_header(encoded_refresh_token, refresh_token_header["typ"])

    decoded_refresh_token = self._try_decode_token(encoded_refresh_token)

    return RefreshTokenPayload(decoded_refresh_token)


  # Helper Methods

  # JWT

  def _encode_token(
    self,
    token_payload: dict[str, Any],
    expected_header: dict[str, str]
  ) -> str:
    return jwt.encode(
      payload=token_payload,
      key=settings.SECRET_KEY,
      algorithm=settings.ALGORITHM,
      headers=expected_header
    )

  def _validate_token_header(self, encoded_token: str, expected_header: str) -> None:
    try:
      header = jwt.get_unverified_header(encoded_token)

    except jwt.InvalidTokenError:
      raise e.InvalidTokenError()

    if header["typ"] != expected_header:
      raise e.InvalidTokenError()

  def _try_decode_token(self, encoded_token: str) -> dict[str, Any]:
    try:
      return jwt.decode(
        jwt=encoded_token,
        key=settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
        audience=settings.AUD,
        issuer=settings.ISS
      )

    except jwt.ExpiredSignatureError:
      raise e.TokenExpiredError()

    except jwt.PyJWTError:
      raise e.InvalidTokenError()