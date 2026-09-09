from unittest.mock import AsyncMock

from httpx import AsyncClient, ASGITransport
import pytest

from app.dependencies.user_dependency import get_user_service
from app.main import app
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserRole, UserCreateRequest
from app.services.user_service import UserService

# Integration

@pytest.fixture
def user_db_repo(db_session):
  return UserRepository(db_session)


# Unit

@pytest.fixture
def mock_user_security():
  return AsyncMock()

@pytest.fixture
def mock_user_repo():
  return AsyncMock()

@pytest.fixture
def unit_user_service(mock_user_security, mock_user_repo):
  return UserService(mock_user_security, mock_user_repo)

@pytest.fixture
def mock_user_service():
  return AsyncMock()

@pytest.fixture
async def unit_user_client(mock_user_service):
  app.dependency_overrides[get_user_service] = lambda: mock_user_service

  async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
    yield c

  app.dependency_overrides.clear()

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

@pytest.fixture
def user_request_data():
  return UserCreateRequest(
    username="user1",
    email="user1@example.com",
    password="Password123",
  )

@pytest.fixture
def unit_user_obj():
  return User(
    id=1,
    username="user1",
    email="user1@example.com",
    hashed_password="Hashedpassword123",
    user_role=UserRole.user
  )