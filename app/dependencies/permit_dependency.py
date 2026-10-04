from typing import Annotated

from fastapi import Depends

from app.core.security import oauth2_scheme, Security
from app.db.database import SessionDep
from app.repositories.user_repository import UserRepository
from app.services.permit_service import PermitService

# Main functions

def get_permit_service(session: SessionDep) -> PermitService:
  security = Security()
  user_repo = UserRepository(session)

  return PermitService(security, user_repo)


# Alias Variables

PermitServiceDep = Annotated[PermitService, Depends(get_permit_service)]

TokenDep = Annotated[str, Depends(oauth2_scheme)]