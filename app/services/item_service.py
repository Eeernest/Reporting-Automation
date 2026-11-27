from datetime import date
from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.exceptions as e
from app.enums.item_enum import ItemStatus, ItemType
from app.models.item_model import Item
from app.models.item_status_history_model import ItemStatusHistory
from app.repositories.item_repository import ItemRepository

class ItemService:
  def __init__(
    self,
    item_repo: ItemRepository,
    session: AsyncSession
  ):
    self.item_repo = item_repo
    self.session = session

  # Main Methods

  # Item Model

  async def register_item(
    self,
    project_id: int,
    name: str,
    item_type: ItemType,
    item_status: ItemStatus,
    description: str | None = None,
    execution_date: date | None = None
  ) -> Item:
    item_obj = Item(
      project_id=project_id,
      name=name,
      item_type=item_type,
      item_status=item_status,
      description=description
    )

    added_item_obj = await self._add_item_or_raise(item_obj)

    status_history_obj = ItemStatusHistory(
      item_id=added_item_obj.id,
      item_status=added_item_obj.item_status,
      execution_date=execution_date
    )

    added_status_history_obj = await self._add_status_history_or_raise(status_history_obj)

    await self._commit_item_or_raise(
      item_obj=added_item_obj,
      status_history_obj=added_status_history_obj
    )

    return added_item_obj

  async def get_item(self, item_id: int, project_id: int, user_id: int) -> Item:
    return await self._get_item_or_raise(item_id, project_id, user_id)

  async def get_all_items(self, project_id: int, user_id: int) -> list[Item]:
    return await self.item_repo.get_all_by_owner(project_id, user_id)

  async def change_item_status(
    self,
    item_obj: Item,
    item_status: ItemStatus,
    execution_date: date | None = None
  ) -> Item:
    self._validate_item_status(item_obj, item_status)

    item_obj.item_status = item_status

    status_history_obj = ItemStatusHistory(
      item_id=item_obj.id,
      item_status=item_obj.item_status,
      execution_date=execution_date
    )

    added_status_history_obj = await self._add_status_history_or_raise(status_history_obj)

    await self._commit_item_or_raise(
      item_obj=item_obj,
      status_history_obj=added_status_history_obj
    )

    return item_obj    

  async def update_item(self, item_obj: Item, update_data: dict[str, Any]) -> Item:
    updated_item_obj = self._update_item_or_raise(item_obj, update_data)

    await self._commit_item_or_raise(item_obj=updated_item_obj, status_history_obj=None)

    return updated_item_obj

  async def delete_item(self, item_obj: Item) -> None:
    await self.item_repo.delete_item(item_obj)

    await self._commit_item_or_raise(item_obj=None)


  # ItemStatusHistory Model

  async def get_status_history(
    self,
    status_history_id: int,
    item_id: int
  ) -> ItemStatusHistory:
    return await self._get_status_history_or_raise(
      status_history_id,
      item_id
    )

  async def get_all_status_histories(self, item_id: int) -> list[ItemStatusHistory]:
    return await self.item_repo.get_all_status_histories_by_owner(item_id)


  # Helper Methods

  # item_repo

  async def _get_item_or_raise(self, item_id: int, project_id: int, user_id: int) -> Item:
    item_obj = await self.item_repo.get_by_id_and_owner(item_id, project_id, user_id)

    if not item_obj:
      raise e.ItemNotFoundError()

    return item_obj

  async def _get_status_history_or_raise(
    self,
    status_history_id: int,
    item_id: int
  ) -> ItemStatusHistory:
    status_history_obj = await self.item_repo.get_status_history_by_id_and_owner(
      status_history_id,
      item_id
    )

    if not status_history_obj:
      raise e.ItemStatusHistoryNotFoundError()

    return status_history_obj


  # item_repo and session

  async def _add_item_or_raise(self, item_obj: Item) -> Item:
    try:
      return await self.item_repo.add_item(item_obj)

    except IntegrityError as exc:
      await self.session.rollback()

      raise e.DatabaseIntegrityError() from exc

  async def _add_status_history_or_raise(
    self,
    status_history_obj: ItemStatusHistory
  ) -> ItemStatusHistory:
    try:
      return await self.item_repo.add_status_history(status_history_obj)

    except IntegrityError as exc:
      await self.session.rollback()

      raise e.DatabaseIntegrityError() from exc


  # session

  async def _commit_item_or_raise(
    self,
    item_obj: Item | None = None,
    status_history_obj: ItemStatusHistory | None = None
  ) -> None:
    try:
      await self.session.commit()

      if item_obj:
        await self.session.refresh(item_obj)

      if status_history_obj:
        await self.session.refresh(status_history_obj)

    except IntegrityError as exc:
      await self.session.rollback()

      raise e.DatabaseIntegrityError() from exc


  # Object

  def _update_item_or_raise(self, item_obj: Item, update_data: dict[str, Any]) -> Item:
    if not update_data:
      raise e.NoFieldProvidedError()

    for field, value in update_data.items():
      setattr(item_obj, field, value)

    return item_obj

  def _validate_item_status(self, item_obj: Item, item_status: ItemStatus) -> None:
    if item_obj.item_status == item_status:
      raise e.StatusAlreadyAssignedError()