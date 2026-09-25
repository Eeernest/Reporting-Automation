import pytest

from app.core.security import Security
from app.repositories.token_repository import TokenRepository
from app.schemas.token_schema import TokenLogoutRequest, TokenRestoreRequest, TokenResponse

# Integration

@pytest.fixture
def token_repo(redis_container):
  return TokenRepository(redis_container)


# Object

@pytest.fixture
def token_logout_obj():
  return TokenLogoutRequest(refresh_token="refresh_token")

@pytest.fixture
def token_restore_obj():
  return TokenRestoreRequest(refresh_token="refresh_token")

@pytest.fixture
def token_response_obj():
  return TokenResponse(
    access_token="access_token",
    refresh_token="refresh_token",
    token_type="bearer"
  )


# Helper

@pytest.fixture
def token_dict():
  return {
    "jti": "1",
    "exp": 1,
    "sub": "3",
    "refresh": True
  }

@pytest.fixture
def refresh_token_payload():
  security = Security()

  user_data = {
    "sub": "1",
    "role": "user"
  }

  return security.create_refresh_token_payload(user_data)