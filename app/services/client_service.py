from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.exceptions as e
import app.core.exception_mapper as exc_map
from app.models.client_model import Client
from app.repositories.client_repository import ClientRepository

class ClientService:
  def __init__(self, client_repo: ClientRepository, session: AsyncSession):
    self.client_repo = client_repo
    self.session = session

  # Main Methods

  async def register_client(
    self,
    user_id: int,
    name: str,
    phone_number: str,
    email: str | None = None,
    notes: str | None = None
  ) -> Client:
    client_obj = Client(
      user_id=user_id,
      name=name,
      email=email,
      phone_number=phone_number,
      notes=notes
    )

    return await self._commit_client_or_raise(client_obj)

  async def get_client(self, client_id: int, user_id: int) -> Client:
    return await self._get_client_or_raise(client_id, user_id)


  # Helper Methods

  # client_repo

  async def _get_client_or_raise(self, client_id: int, user_id: int) -> Client:
    client_obj = await self.client_repo.get_by_id_and_user_id(client_id, user_id)

    if not client_obj:
      raise e.ClientNotFoundError()

    return client_obj


  # client_repo and session

  async def _commit_client_or_raise(self, client_obj: Client) -> Client:
    try:
      added_client_obj = await self.client_repo.add_client(client_obj)

      await self.session.commit()

      return added_client_obj
    
    except IntegrityError as exc:
      await self.session.rollback()

      err_msg = str(exc.orig).lower()

      exc_map.refine_integrity_error(err_msg, exc)