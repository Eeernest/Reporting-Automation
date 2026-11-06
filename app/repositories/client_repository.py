from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client_model import Client

class ClientRepository:
  def __init__(self, session: AsyncSession):
    self.session = session

  # Main Methods

  async def add_client(self, client_obj: Client) -> Client:
    self.session.add(client_obj)
    await self.session.flush()

    return client_obj

  async def get_by_id_and_user_id(self, client_id: int, user_id: int) -> Client | None:
    result = await self.session.execute(
      select(Client).where(Client.id == client_id, Client.user_id == user_id)
    )

    return result.scalar_one_or_none()