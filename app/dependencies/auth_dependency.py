from typing import Annotated

from fastapi import Depends

from app.core.security import Security
from app.db.database import SessionDep
from app.redis.redis_client import RedisDep
from app.repositories.token_repository import TokenRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

def get_auth_service(client: RedisDep, session: SessionDep):
  security = Security()
  token_repo = TokenRepository(client)
  user_repo = UserRepository(session)

  return AuthService(security, token_repo, user_repo)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]