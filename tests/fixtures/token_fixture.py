import pytest

from app.core.security import Security
from app.repositories.token_repository import TokenRepository

# Integration

@pytest.fixture()
def token_repo(redis_container):
  return TokenRepository(redis_container)


# Payload

@pytest.fixture()
def refresh_token_payload(mock_user_obj):
  security = Security()

  return security.create_refresh_token_payload(mock_user_obj.id)