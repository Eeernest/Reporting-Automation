from jwt.exceptions import PyJWTError
from redis.exceptions import RedisError

from app.core.config import settings
import app.core.exceptions as e
from app.core.security import Security
from app.models.user_model import User
from app.repositories.token_repository import TokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.token_schema import TokenLogoutRequest, TokenResponse

class AuthService:
  def __init__(self, security: Security, token_repo: TokenRepository, user_repo: UserRepository):
    self.security = security
    self.token_repo = token_repo
    self.user_repo = user_repo

  # Main Methods

  async def login(self, username: str, password: str) -> TokenResponse:
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

    return TokenResponse(
      access_token=encoded_access_token,
      refresh_token=encoded_refresh_token,
      token_type="bearer"
    )

  async def logout(self, logout_request: TokenLogoutRequest) -> None:
    try:
      decoded_refresh_token = self.security.decode_jwt_token(logout_request.refresh_token)

      await self.token_repo.delete_refresh_token(decoded_refresh_token["jti"])

    except PyJWTError:
      pass


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


  # token_repo

  async def _try_store_refresh_token(self, jti: str, exp: int, sub: str) -> None:
    try:
      await self.token_repo.store_refresh_token(jti, exp, sub)

    except RedisError:
      raise e.RedisFailureError()


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