from app.models.client_model import Client
from app.repositories.client_repository import ClientRepository

class ClientService:
  def __init__(self, client_repo: ClientRepository):
    self.client_repo = client_repo

  # Main Methods

  async def register_client(
    self,
    user_id: int,
    name: str,
    phone_number: str,
    company: str | None = None,
    email: str | None = None,
    notes: str | None = None
  ):
    client_obj = Client(
      user_id=user_id,
      name=name,
      phone_number=phone_number,
      company=company,
      email=email,
      notes=notes
    )

    return await self.client_repo.save_client(client_obj)