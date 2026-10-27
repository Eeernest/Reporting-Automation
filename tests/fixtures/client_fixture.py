from unittest.mock import AsyncMock

from httpx import AsyncClient, ASGITransport
import pytest

from app.dependencies.client_dependency import get_client_service
from app.dependencies.permit_dependency import get_current_user
from app.main import app
from app.models.client_model import Client
from app.repositories.client_repository import ClientRepository
from app.services.client_service import ClientService

# Integration

@pytest.fixture
def integ_client_repo(db_session):
  return ClientRepository(db_session)

@pytest.fixture
def integ_client_service(integ_client_repo, db_session):
  return ClientService(integ_client_repo, db_session)

@pytest.fixture
async def integ_client_router(integ_client_service, saved_user_obj):
  app.dependency_overrides[get_current_user] = lambda: saved_user_obj
  app.dependency_overrides[get_client_service] = lambda: integ_client_service

  async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
    yield c

  app.dependency_overrides.clear()


# Unit

@pytest.fixture
def mock_client_repo():
  return AsyncMock()

@pytest.fixture
def mock_client_session():
  return AsyncMock()

@pytest.fixture
def unit_client_service(mock_client_repo, mock_client_session):
  return ClientService(mock_client_repo, mock_client_session)


# Object

@pytest.fixture
def integ_client_obj(saved_user_obj):
  return Client(
    user_id=saved_user_obj.id,
    name="client1",
    email="company1@example.com",
    phone_number="+4812345678",
    notes="notes",
  )

@pytest.fixture
def unit_client_obj():
  return Client(
    id=1,
    user_id=1,
    name="client1",
    email="company1@example.com",
    phone_number="+4812345678",
    notes="notes",
  )