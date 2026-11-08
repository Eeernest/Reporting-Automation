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