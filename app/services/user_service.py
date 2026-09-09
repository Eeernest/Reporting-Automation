from sqlalchemy.exc import IntegrityError

import app.core.exceptions as e
from app.core.security import Security
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserRole, UserCreateRequest

class UserService:
  def __init__(self, security: Security, user_repo: UserRepository):
    self.security = security
    self.user_repo = user_repo

  # Main Methods

  async def create_account(self, user_request_data: UserCreateRequest) -> User:
    await self._check_username(user_request_data.username)
    await self._check_email(user_request_data.email)

    hashed_password = await self.security.get_password_hash(user_request_data.password)

    user_obj = User(
      username=user_request_data.username,
      email=user_request_data.email,
      hashed_password=hashed_password,
      user_role=UserRole.user
    )
    
    return await self._try_save_user(user_obj)


  # UserRepository Helper Methods

  async def _check_username(self, username: str) -> None:
    if await self.user_repo.get_by_username(username) is not None:
      raise e.UsernameUnavailableError()

  async def _check_email(self, email: str) -> None:
    if await self.user_repo.get_by_email(email) is not None:
      raise e.EmailUnavailableError()

  async def _try_save_user(self, user_obj: User) -> User:
    try:
      
      return await self.user_repo.save(user_obj)

    except IntegrityError as exc:
      if "username" in exc.orig:
        raise e.UsernameUnavailableError()

      if "email" in exc.orig:
        raise e.EmailUnavailableError()