from unittest.mock import AsyncMock, Mock

import pytest

from app.schemas.token_schema import TokenResponse
from app.services.auth_service import AuthService

# Unit

@pytest.fixture()
def unit_auth_service(mock_security, mock_token_repo, mock_user_repo):
  return AuthService(mock_security, mock_token_repo, mock_user_repo)


# Object

@pytest.fixture()
def token_response_obj():
  return TokenResponse(
    access_token="access_token",
    refresh_token="refresh_token",
    token_type="bearer"
  )

# Helper

@pytest.fixture()
def token_dict():
  return {
    "jti": "1",
    "exp": 1,
    "sub": "3"
  }