from typing import Annotated

from fastapi import Depends

from app.db.database import SessionDep
from app.dependencies.permit_dependency import CurrentUserDep
from app.models.client_model import Client
from app.repositories.client_repository import ClientRepository
from app.services.client_service import ClientService

# Main Functions

def get_client_service(session: SessionDep):
  client_repo = ClientRepository(session)

  return ClientService(client_repo, session)

async def get_verified_client(
  client_id: int,
  current_user: CurrentUserDep,
  service: ClientServiceDep
) -> Client:
  return await service.get_client(client_id, current_user.id)


# Alias Variables

ClientServiceDep = Annotated[ClientService, Depends(get_client_service)]

VerifiedClientDep = Annotated[Client, Depends(get_verified_client)]