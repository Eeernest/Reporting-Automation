from app.core.security import Security
from app.models.user_model import UserRole, User
from app.repositories.user_repository import UserRepository

class UserService:
  def __init__(self, security: Security, user_repo: UserRepository):
    self.security = security
    self.user_repo = user_repo

  # Main Methods

  async def register_user(
    self,
    username: str,
    email: str,
    password: str
  ) -> User:
    hashed_password = await self.security.get_password_hash(password)

    user_obj = User(
      username=username,
      email=email,
      hashed_password=hashed_password,
      user_role=UserRole.user
    )

    return await self.user_repo.save_user(user_obj)