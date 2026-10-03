from app.core.config import settings
import app.core.exceptions as e
from app.core.security import Security
from app.models.user_model import User
from app.repositories.token_repository import TokenRepository
from app.repositories.user_repository import UserRepository

class AuthService:
  def __init__(self,
    security: Security,
    token_repo: TokenRepository,
    user_repo: UserRepository
  ):
    self.security = security
    self.token_repo = token_repo
    self.user_repo = user_repo


  # Main Mehods

  async def login(self, username: str, password: str) -> dict[str, str]:
    user_obj = await self._verify_user_credentials(username, password)

    self._verify_user_status(user_obj)

    access_token_payload = self.security.create_access_token_payload(
      user_obj.id,
      user_obj.user_role
    )

    refresh_token_payload = self.security.create_refresh_token_payload(user_obj.id)

    await self.token_repo.store_refresh_token(
      refresh_token_payload["jti"],
      refresh_token_payload["sub"],
      refresh_token_payload["exp"]
    )

    encoded_access_token = self.security.get_encoded_access_token(access_token_payload)
    encoded_refresh_token = self.security.get_encoded_refresh_token(refresh_token_payload)

    return {
      "access_token": encoded_access_token,
      "refresh_token": encoded_refresh_token,
      "token_type": "bearer"
    }

  async def logout(self, encoded_refresh_token: str) -> None:
    try:
      decoded_refresh_token = self.security.get_decoded_refresh_token(encoded_refresh_token)

      await self.token_repo.delete_refresh_token(decoded_refresh_token["jti"])

    except (e.InvalidTokenError, e.TokenExpiredError):
      pass

  async def refresh(self, refresh_token: str) -> dict[str, str]:
    decoded_refresh_token = self.security.get_decoded_refresh_token(refresh_token)

    await self.token_repo.delete_refresh_token(decoded_refresh_token["jti"])

    user_obj = await self._try_get_user_by_id(int(decoded_refresh_token["sub"]))

    self._verify_user_status(user_obj)

    access_token_payload = self.security.create_access_token_payload(
      user_obj.id,
      user_obj.user_role
    )

    refresh_token_payload = self.security.create_refresh_token_payload(user_obj.id)

    await self.token_repo.store_refresh_token(
      refresh_token_payload["jti"],
      refresh_token_payload["sub"],
      refresh_token_payload["exp"]
    )

    encoded_access_token = self.security.get_encoded_access_token(access_token_payload)
    encoded_refresh_token = self.security.get_encoded_refresh_token(refresh_token_payload)

    return {
      "access_token": encoded_access_token,
      "refresh_token": encoded_refresh_token,
      "token_type": "bearer"
    }


  # Helper Methods

  # user_repo

  async def _try_get_user_by_id(self, id: int) -> User:
    user_obj = await self.user_repo.get_by_id(id)

    if not user_obj:
      raise e.InvalidTokenError()

    return user_obj


  # Mixed Dependencies

  async def _verify_user_credentials(self, username: str, password: str) -> User | None:
    user_obj = await self.user_repo.get_by_username(username)

    if not user_obj:
      await self.security.verify_password(password, settings.DUMMY_PASSWORD)

      return None

    is_password_correct = await self.security.verify_password(
      password,
      user_obj.hashed_password
    )

    if not is_password_correct:
      return None

    return user_obj


  # Uesr Model

  def _verify_user_status(self, user_obj: User) -> None:
    if not user_obj:
      raise e.InvalidCredentialsError()

    if not user_obj.is_active:
      raise e.UserInactiveError()

    if user_obj.is_deleted:
      raise e.UserDeletedError()