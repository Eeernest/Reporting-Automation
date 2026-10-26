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