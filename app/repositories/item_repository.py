from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item_model import Item
from app.models.project_model import Project

class ItemRepository:
  def __init__(self, session: AsyncSession):
    self.session = session

  # Main Methods

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