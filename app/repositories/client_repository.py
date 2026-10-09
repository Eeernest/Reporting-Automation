from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.exceptions as e
from app.models.client_model import Client

class ClientRepository:
  def __init__(self, session: AsyncSession):
    self.session = session

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