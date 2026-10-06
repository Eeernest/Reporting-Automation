from unittest.mock import AsyncMock, MagicMock

from httpx import AsyncClient, ASGITransport
import pytest

from app.core.security import Security
from app.dependencies.user_dependency import get_user_service
from app.main import app
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserRole, RegisterRequest
from app.services.user_service import UserService

# Integration

@pytest.fixture
def integ_user_repo(db_session):
  return UserRepository(db_session)

@pytest.fixture
def integ_user_service(integ_user_repo):
  security = Security()

  return UserService(security, integ_user_repo)

@pytest.fixture
async def integ_user_client(integ_user_service):
  app.dependency_overrides[get_user_service] = lambda: integ_user_service

  async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
    yield c

  app.dependency_overrides.clear()


# Unit

@pytest.fixture
def mock_user_repo():
  return AsyncMock()

@pytest.fixture
def unit_user_service(mock_security, mock_user_repo):
  return UserService(mock_security, mock_user_repo)

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
def mock_user_obj():
  user = MagicMock(spec=User)
  user.id = 1
  user.username = "user1"
  user.email = "user1@example.com"
  user.hashed_password = "Hashedpassword123"
  user.user_role = UserRole.user
  user.is_active = True
  user.is_deleted = False

  return user

@pytest.fixture
def user_obj():
  return User(
    username="user1",
    email="user1@example.com",
    hashed_password="Hashedpassword123",
    user_role=UserRole.user
  )

@pytest.fixture
async def saved_user_obj(integ_user_repo, user_obj):
  return await integ_user_repo.save(user_obj)

@pytest.fixture
def user_register_request():
  return RegisterRequest(
    username="user1",
    email="user1@example.com",
    password="Password123",
  )