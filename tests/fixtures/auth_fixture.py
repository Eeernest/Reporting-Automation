import pytest

from app.services.auth_service import AuthService

# Unit

@pytest.fixture()
def unit_auth_service(mock_security, mock_token_repo, mock_user_repo):
  return AuthService(mock_security, mock_token_repo, mock_user_repo)


# Helper

@pytest.fixture()
def token_dict():
  return {
    "jti": "1",
    "exp": 1,
    "sub": "3"
  }