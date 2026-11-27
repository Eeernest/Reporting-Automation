from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item_model import Item
from app.models.item_status_history_model import ItemStatusHistory
from app.models.project_model import Project

class ItemRepository:
  def __init__(self, session: AsyncSession):
    self.session = session

  # Main Methods

  # Item Model

  async def add_item(self, item_obj: Item) -> Item:
    self.session.add(item_obj)
    await self.session.flush()

    return item_obj

  async def get_by_id_and_owner(
    self,
    item_id: int,
    project_id: int,
    user_id: int
  ) -> Item | None:
    stmt = (
      select(Item)
      .join(Project, Item.project_id == Project.id)
      .where(
        Item.id == item_id,
        Item.project_id == project_id,
        Project.user_id == user_id
      )
    )

    result = await self.session.execute(stmt)

    return result.scalar_one_or_none()

  async def get_all_by_owner(self, project_id: int, user_id: int) -> list[Item]:
    stmt = (
      select(Item)
      .join(Project, Item.project_id == Project.id)
      .where(
        Item.project_id == project_id,
        Project.user_id == user_id
      )
    )

    result = await self.session.execute(stmt)

    return list(result.scalars().all())

  async def delete_item(self, item_obj: Item) -> None:
    await self.session.delete(item_obj)

  # ItemStatusHistory Model

  async def add_status_history(
    self,
    item_status_obj: ItemStatusHistory
  ) -> ItemStatusHistory:
    self.session.add(item_status_obj)
    await self.session.flush()

    return item_status_obj

  async def get_status_history_by_id_and_owner(
    self,
    status_history_id: int,
    item_id: int
  ) -> ItemStatusHistory | None:
    stmt = (
      select(ItemStatusHistory)
      .where(
        ItemStatusHistory.id == status_history_id,
        ItemStatusHistory.item_id == item_id
      )
    )

    result = await self.session.execute(stmt)

    return result.scalar_one_or_none()

  async def get_all_status_histories_by_owner(
    self,
    item_id: int
  ) -> list[ItemStatusHistory]:
    stmt = (
      select(ItemStatusHistory)
      .where(
        ItemStatusHistory.item_id == item_id
      )
    )

    result = await self.session.execute(stmt)

    return list(result.scalars().all())