from unittest.mock import AsyncMock, MagicMock

from httpx import AsyncClient, ASGITransport
import pytest

from app.core.security import Security
from app.dependencies.user_dependency import get_user_service
from app.main import app
from app.models.user_model import UserRole, User
from app.repositories.user_repository import UserRepository
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
async def integ_user_router(integ_user_service):
  app.dependency_overrides[get_user_service] = lambda: integ_user_service

  async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
    yield c

  app.dependency_overrides.clear()


# Unit

@pytest.fixture
def mock_user_repo():
  return AsyncMock()

@pytest.fixture
def mock_user_session():
  return AsyncMock()

@pytest.fixture
def unit_user_service(mock_security, mock_user_session, mock_user_repo):
  return UserService(mock_security, mock_user_session, mock_user_repo)

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
def integ_user_obj():
  return User(
    username="user1",
    email="user1@example.com",
    hashed_password="Hashedpassword123",
    user_role=UserRole.user
  )

@pytest.fixture
async def saved_user_obj(integ_user_repo, integ_user_obj, db_session):
  security = Security()

  user_service = UserService(security, db_session, integ_user_repo)

  return await user_service.register_user(
    username=integ_user_obj.username,
    email=integ_user_obj.email,
    password="Password123"
  )


# Helpers

# router

@pytest.fixture
async def registered_user_response(integ_user_router):
  request = {
    "username": "user1",
    "email": "user1@example.com",
    "password": "Password123"
  }

  return await integ_user_router.post("/register_user", json=request)