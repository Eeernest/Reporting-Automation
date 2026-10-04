from httpx import AsyncClient, ASGITransport
import pytest

from app.core.security import Security
from app.dependencies.auth_dependency import get_auth_service
from app.main import app
from app.services.auth_service import AuthService

# Integration

@pytest.fixture
def integ_auth_service(integ_token_repo, integ_user_repo):
  security = Security()

  return AuthService(security, integ_token_repo, integ_user_repo)

@pytest.fixture
async def integ_auth_client(integ_auth_service):
  app.dependency_overrides[get_auth_service] = lambda: integ_auth_service

  async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
    yield c

  app.dependency_overrides.clear()


# Unit

@pytest.fixture
def unit_auth_service(mock_security, mock_token_repo, mock_user_repo):
  return AuthService(mock_security, mock_token_repo, mock_user_repo)