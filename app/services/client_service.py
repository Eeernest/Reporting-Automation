from typing import Any

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

    added_client_obj = await self._add_client_or_raise(client_obj)

    await self._commit_client_or_raise(client_obj)

    return added_client_obj

  async def update_client(
    self,
    client_obj: Client,
    update_data: dict[str, Any]
  ) -> Client:
    updated_client_obj = self._update_client_or_raise(client_obj, update_data)

    await self._commit_client_or_raise(updated_client_obj)

    return updated_client_obj

  async def get_client(self, client_id: int, user_id: int) -> Client:
    return await self._get_client_or_raise(client_id, user_id)

  async def get_all_clients(self, user_id: int) -> list[Client]:
    return await self.client_repo.get_all_by_owner(user_id)


  # Helper Methods

  # client_repo

  async def _get_client_or_raise(self, client_id: int, user_id: int) -> Client:
    client_obj = await self.client_repo.get_by_id_and_owner(client_id, user_id)

    if not client_obj:
      raise e.ClientNotFoundError()

    return client_obj


  # client_repo and session

  async def _add_client_or_raise(self, client_obj: Client) -> Client:
    try:
      return await self.client_repo.add_client(client_obj)

    except IntegrityError as exc:
      await self.session.rollback()

      err_msg = str(exc.orig).lower()

      exc_map.refine_integrity_error(err_msg, exc)


  # session

  async def _commit_client_or_raise(self, client_obj: Client | None = None) -> None:
    try:
      await self.session.commit()

      if client_obj:
        await self.session.refresh(client_obj)
    
    except IntegrityError as exc:
      await self.session.rollback()

      err_msg = str(exc.orig).lower()

      exc_map.refine_integrity_error(err_msg, exc)


  # Object

  def _update_client_or_raise(
      self, client_obj: Client,
      update_data: dict[str, Any]
  ) -> Client:
    if not update_data:
      raise e.NoFieldProvidedError()

    for field, value in update_data.items():
      setattr(client_obj, field, value)

    return client_obj