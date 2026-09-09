import pytest

from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserRole

# Integration

@pytest.fixture
def user_db_repo(db_session):
  return UserRepository(db_session)


# Objects

@pytest.fixture
def user_obj():
  return User(
    username="user1",
    email="user1@example.com",
    hashed_password="Hashedpassword123",
    user_role=UserRole.user
  )

@pytest.fixture
async def saved_user_obj(user_db_repo, user_obj):
  return await user_db_repo.save(user_obj)