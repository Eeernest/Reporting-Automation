import pytest

from app.services.permit_service import PermitService

# Unit

@pytest.fixture
def unit_permit_service(mock_security, mock_user_repo):
  return PermitService(mock_security, mock_user_repo)