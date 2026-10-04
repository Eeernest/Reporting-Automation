from httpx import AsyncClient, ASGITransport
import pytest

from app.core.security import Security
from app.dependencies.permit_dependency import get_permit_service
from app.main import app
from app.services.permit_service import PermitService

# Integration

@pytest.fixture
def integ_permit_service(integ_user_repo) -> PermitService:
  security = Security()

  return PermitService(security, integ_user_repo)

@pytest.fixture
async def integ_permit_client(integ_permit_service):
  app.dependency_overrides[get_permit_service] = lambda: integ_permit_service

  async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
    yield c

  app.dependency_overrides.clear()


# Unit

@pytest.fixture
def unit_permit_service(mock_security, mock_user_repo):
  return PermitService(mock_security, mock_user_repo)