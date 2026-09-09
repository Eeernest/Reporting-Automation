from typing import Annotated

from fastapi import Depends

from app.core.security import Security
from app.db.database import SessionDep
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

def get_user_service(session: SessionDep):
  security = Security()
  user_repo = UserRepository(session)

  return UserService(security, user_repo)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]