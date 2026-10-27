from typing import Annotated

from fastapi import Depends

from app.core.security import oauth2_scheme, Security
from app.db.database import SessionDep
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.services.permit_service import PermitService

# Main functions

def get_permit_service(session: SessionDep) -> PermitService:
  security = Security()
  user_repo = UserRepository(session)

  return PermitService(security, user_repo)

async def get_current_user(service: PermitServiceDep, access_token: TokenDep) -> User:
  return await service.get_current_user(access_token)


# Alias Variables

PermitServiceDep = Annotated[PermitService, Depends(get_permit_service)]

TokenDep = Annotated[str, Depends(oauth2_scheme)]

CurrentUserDep = Annotated[User, Depends(get_current_user)]