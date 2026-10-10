from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.exceptions as e
from app.models.client_model import Client

class ClientRepository:
  def __init__(self, session: AsyncSession):
    self.session = session

  # Main Methods

  async def save_client(self, client_obj: Client) -> Client:
    try:
      self.session.add(client_obj)
      await self.session.commit()
      await self.session.refresh(client_obj)

      return client_obj

    except IntegrityError as exc:
      await self.session.rollback()

      if "name" in exc.orig:
        raise e.NameUnavailableError()

      if "company" in exc.orig:
        raise e.CompanyUnavailableError()

      if "email" in exc.orig:
        raise e.EmailUnavailableError()

      if "phone_number" in exc.orig:
        raise e.PhoneUnavailableError()

  async def get_by_name(self, name: str) -> Client | None:
    result = await self.session.execute(select(Client).where(Client.name == name))

    return result.scalar_one_or_none()

  async def get_by_company(self, company: str) -> Client | None:
    result = await self.session.execute(select(Client).where(Client.company == company))

    return result.scalar_one_or_none()

  async def get_by_email(self, email: str) -> Client | None:
    result = await self.session.execute(select(Client).where(Client.email == email))

    return result.scalar_one_or_none()

  async def get_by_phone_number(self, phone_number: str) -> Client | None:
    result = await self.session.execute(
      select(Client).where(Client.phone_number == phone_number)
    )

    return result.scalar_one_or_none()