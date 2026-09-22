from unittest.mock import AsyncMock

from httpx import AsyncClient, ASGITransport
import pytest

from app.dependencies.auth_dependency import get_auth_service
from app.main import app
from app.services.auth_service import AuthService

# Unit

@pytest.fixture
def unit_auth_service(mock_security, mock_token_repo, mock_user_repo):
  return AuthService(mock_security, mock_token_repo, mock_user_repo)

@pytest.fixture
def mock_auth_service():
  return AsyncMock()

@pytest.fixture
async def unit_auth_client(mock_auth_service):
  app.dependency_overrides[get_auth_service] = lambda: mock_auth_service
  
  async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
    yield c

  app.dependency_overrides.clear()