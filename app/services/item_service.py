from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import app.core.exceptions as e
from app.enums.item_enum import ItemStatus, ItemType
from app.models.item_model import Item
from app.repositories.item_repository import ItemRepository
from app.repositories.project_repository import ProjectRepository

class ItemService:
  def __init__(
    self,
    item_repo: ItemRepository,
    session: AsyncSession
  ):
    self.item_repo = item_repo
    self.session = session

  # Main Methods

  async def register_item(
    self,
    user_id: int,
    project_id: int,
    name: str,
    item_type: ItemType,
    item_status: ItemStatus,
    description: str | None = None
  ) -> Item:
    item_obj = Item(
      project_id=project_id,
      name=name,
      item_type=item_type,
      item_status=item_status,
      description=description
    )

    return await self._commit_item_or_raise(item_obj)


  # Helper Methods

  # item_repo and session

  async def _commit_item_or_raise(self, item_obj: Item) -> Item:
    try:
      added_item_obj = await self.item_repo.add_item(item_obj)

      await self.session.commit()

      return added_item_obj

    except IntegrityError as exc:
      await self.session.rollback()

      raise e.DatabaseIntegrityError() from exc