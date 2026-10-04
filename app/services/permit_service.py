import app.core.exceptions as e
from app.core.security import Security
from app.models.user_model import User
from app.repositories.user_repository import UserRepository

class PermitService:
  def __init__(self, security: Security, user_repo: UserRepository):
    self.security = security
    self.user_repo = user_repo


  # Main Methods

  async def get_current_user(self, access_token: str) -> User:
    decoded_access_token = self.security.get_decoded_access_token(access_token)

    user_obj = await self._try_get_user_by_id(int(decoded_access_token["sub"]))

    self._verify_user_status(user_obj)

    return user_obj


  # Helper Methods

  # user_repo

  async def _try_get_user_by_id(self, id: int) -> User:
    user_obj = await self.user_repo.get_by_id(id)

    if not user_obj:
      raise e.InvalidTokenError()

    return user_obj


  # User Model

  def _verify_user_status(self, user_obj: User) -> None:
    if not user_obj.is_active:
      raise e.UserInactiveError()

    if user_obj.is_deleted:
      raise e.UserDeletedError()