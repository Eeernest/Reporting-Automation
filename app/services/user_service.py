from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.exception_mapper as exc_map
from app.core.security import Security
from app.models.user_model import UserRole, User
from app.repositories.user_repository import UserRepository

class UserService:
  def __init__(self, security: Security, session: AsyncSession, user_repo: UserRepository):
    self.security = security
    self.session = session
    self.user_repo = user_repo

  # Main Methods

  async def register_user(
    self,
    username: str,
    email: str,
    password: str
  ) -> User:
    hashed_password = await self.security.get_password_hash(password)

    user_obj = User(
      username=username,
      email=email,
      hashed_password=hashed_password,
      user_role=UserRole.user
    )

    return await self._try_commit_user_obj(user_obj)


  # Helper Methods

  # session and user_repo

  async def _try_commit_user_obj(self, user_obj: User) -> User:
    try:
      added_user_obj = await self.user_repo.add_user(user_obj)

      await self.session.commit()

      return added_user_obj

    except IntegrityError as exc:
      await self.session.rollback()

      err_msg = str(exc.orig).lower()

      exc_map.refine_integrity_error(err_msg, exc)