from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.exceptions as e
from app.models.user_model import User

class UserRepository:
  def __init__(self, session: AsyncSession):
    self.session = session

  # Main Methods

  async def add_user(self, user_obj: User) -> User:
    self.session.add(user_obj)
    await self.session.flush()

    return user_obj

  async def get_by_id(self, id: int) -> User | None:
    result = await self.session.execute(select(User).where(User.id == id))

    return result.scalar_one_or_none()

  async def get_by_username(self, username: str) -> User | None:
    result = await self.session.execute(select(User).where(User.username == username))

    return result.scalar_one_or_none()