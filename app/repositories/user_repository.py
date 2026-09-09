from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User

class UserRepository:
  def __init__(self, session: AsyncSession):
    self.session = session

  # Main Methods

  async def save(self, user_obj: User) -> User:
    try:
      self.session.add(user_obj)
      await self.session.commit()
      await self.session.refresh(user_obj)

      return user_obj

    except IntegrityError as exc:
      await self.session.rollback()

      raise exc

  async def get_by_username(self, username: str) -> User | None:
    result = await self.session.execute(select(User).where(User.username == username))

    return result.scalar_one_or_none()

  async def get_by_email(self, email: str) -> User | None:
    result = await self.session.execute(select(User).where(User.email == email))

    return result.scalar_one_or_none()