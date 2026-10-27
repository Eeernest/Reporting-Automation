from typing import Annotated

from fastapi import Depends

from app.db.database import SessionDep
from app.repositories.client_repository import ClientRepository
from app.services.client_service import ClientService

# Main Functions

def get_client_service(session: SessionDep):
  client_repo = ClientRepository(session)

  return ClientService(client_repo, session)


# Alias Variables

ClientServiceDep = Annotated[ClientService, Depends(get_client_service)]