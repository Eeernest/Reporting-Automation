from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item_model import Item

class ItemRepository:
  def __init__(self, session: AsyncSession):
    self.session = session

  # Main Methods

  async def add_item(self, item_obj: Item) -> Item:
    self.session.add(item_obj)
    await self.session.flush()

    return item_obj

  async def get_by_id_and_project_id(self, item_id: int, project_id: int) -> Item | None:
    result = await self.session.execute(
      select(Item).where(Item.id == item_id, Item.project_id == project_id)
    )

    return result.scalar_one_or_none()