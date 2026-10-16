from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.exceptions as e
from app.models.user_model import User

class UserRepository:
  def __init__(self, session: AsyncSession):
    self.session = session

  # Main Methods

  async def save_user(self, user_obj: User) -> User:
    try:
      self.session.add(user_obj)
      await self.session.commit()
      await self.session.refresh(user_obj)

      return user_obj

    except IntegrityError as exc:
      await self.session.rollback()

      err_msg = str(exc.orig).lower()

      self._refine_integrity_error(err_msg, exc)

  async def get_by_id(self, id: int) -> User | None:
    result = await self.session.execute(select(User).where(User.id == id))

    return result.scalar_one_or_none()

  async def get_by_username(self, username: str) -> User | None:
    result = await self.session.execute(select(User).where(User.username == username))

    return result.scalar_one_or_none()


  # Helper Methods

  def _refine_integrity_error(self, err_msg: str, exc: Exception) -> None:
    constraint_map = {
      "username": e.UsernameUnavailableError,
      "email": e.EmailUnavailableError
    }

    for partial_msg, exc_class in constraint_map.items():
      if partial_msg in err_msg:
        raise exc_class() from exc

    raise e.DatabaseIntegrityError() from exc