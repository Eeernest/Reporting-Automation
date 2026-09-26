from datetime import datetime, timezone, timedelta

import pytest

from app.core.security import Security
from app.repositories.token_repository import TokenRepository

# Integration

@pytest.fixture()
def token_repo(redis_container):
  return TokenRepository(redis_container)


# Payload

@pytest.fixture()
def refresh_token_payload():
  security = Security()

  user_data = {
    "sub": "1",
    "role": "user"
  }

  return security.create_refresh_token_payload(user_data)