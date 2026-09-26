from jwt.exceptions import PyJWTError, ExpiredSignatureError
from redis.exceptions import RedisError

from app.core.config import settings
import app.core.exceptions as e
from app.core.security import Security
from app.models.user_model import User
from app.repositories.token_repository import TokenRepository
from app.repositories.user_repository import UserRepository

class AuthService:
  def __init__(
    self,
    security: Security,
    token_repo: TokenRepository,
    user_repo: UserRepository
  ):
    self.security = security
    self.token_repo = token_repo
    self.user_repo = user_repo

  # Main Methods

  async def login(self, username: str, password: str) -> dict[str, str]:
    user_obj = await self._verify_user_credentials(username, password)

    self._verify_user_status(user_obj)

    access_token_payload = self._get_access_token_payload(user_obj)
    refresh_token_payload = self._get_refresh_token_payload(user_obj)

    await self._try_store_refresh_token(
      refresh_token_payload["jti"],
      refresh_token_payload["exp"],
      refresh_token_payload["sub"]
    )

    encoded_access_token = self.security.encode_jwt_token(access_token_payload)
    encoded_refresh_token = self.security.encode_jwt_token(refresh_token_payload)

    return {
      "access_token": encoded_access_token,
      "refresh_token": encoded_refresh_token,
      "token_type": "bearer"
    }

  async def logout(self, encoded_refresh_token: str) -> None:
    try:
      decoded_refresh_token = self.security.decode_jwt_token(encoded_refresh_token)

      await self.token_repo.delete_refresh_token(decoded_refresh_token["jti"])

    except PyJWTError:
      pass

  async def restore_tokens(self, encoded_refresh_token: str) -> dict[str, str]:
    decoded_refresh_token = self._try_decode_jwt_token(encoded_refresh_token)

    self._validate_refresh_token(decoded_refresh_token["refresh"])

    await self._try_delete_refresh_token(decoded_refresh_token["jti"])

    user_obj = await self._try_get_user_by_id(int(decoded_refresh_token["sub"]))

    access_token_payload = self._get_access_token_payload(user_obj)
    refresh_token_payload = self._get_refresh_token_payload(user_obj)

    await self._try_store_refresh_token(
      refresh_token_payload["jti"],
      refresh_token_payload["exp"],
      refresh_token_payload["sub"]
    )

    encoded_access_token = self.security.encode_jwt_token(access_token_payload)
    encoded_refresh_token = self.security.encode_jwt_token(refresh_token_payload)

    return {
      "access_token": encoded_access_token,
      "refresh_token": encoded_refresh_token,
      "token_type": "bearer"
    }


  # Helper Methods

  # security

  def _get_access_token_payload(self, user_obj: User) -> dict:
    user_data = {
      "sub": user_obj.id,
      "role": user_obj.user_role
    }

    return self.security.create_access_token_payload(user_data)

  def _get_refresh_token_payload(self, user_obj: User) -> dict:
    user_data = {
      "sub": user_obj.id,
      "role": user_obj.user_role
    }

    return self.security.create_refresh_token_payload(user_data)

  def _try_decode_jwt_token(self, encoded_token: str) -> dict:
    try:
      return self.security.decode_jwt_token(encoded_token)

    except ExpiredSignatureError:
      raise e.TokenExpiredError()

    except PyJWTError:
      raise e.InvalidCredentialsError()


  # token_repo

  async def _try_store_refresh_token(self, jti: str, exp: int, sub: str) -> None:
    try:
      await self.token_repo.store_refresh_token(jti, exp, sub)

    except RedisError:
      raise e.RedisFailureError()

  async def _try_delete_refresh_token(self, jti: str) -> None:
    try:
      await self.token_repo.delete_refresh_token(jti)

    except RedisError:
      raise e.RedisFailureError()


  # user_repo

  async def _try_get_user_by_id(self, id: int) -> User:
    user_obj = await self.user_repo.get_by_id(id)
    
    if not user_obj:
      raise e.InvalidTokenError()

    return user_obj


  # Mixed Dependencies

  async def _verify_user_credentials(self, username: str, password: str) -> User | None:
    user_obj = await self.user_repo.get_by_username(username)

    if user_obj is None:
      await self.security.verify_password(password, settings.DUMMY_PASSWORD)

      return None

    is_password_correct = await self.security.verify_password(password, user_obj.hashed_password)

    if is_password_correct is False:
      return None

    return user_obj


  # User model

  def _verify_user_status(self, user_obj: User | None) -> None:
    if user_obj is None:
      raise e.InvalidCredentialsError()
    
    if not user_obj.is_active:
      raise e.UserInactiveError()

    if user_obj.is_deleted:
      raise e.UserDeletedError()


  # Token data

  def _validate_refresh_token(self, refresh: bool) -> None:
    if not refresh:
      raise e.InvalidTokenError()