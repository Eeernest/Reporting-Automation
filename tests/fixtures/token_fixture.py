from unittest.mock import AsyncMock

import pytest

from app.repositories.token_repository import TokenRepository

# Integration

@pytest.fixture
def int_token_repo(redis_container):
  return TokenRepository(redis_container)


# Unit

@pytest.fixture
def mock_redis_client():
  return AsyncMock()

@pytest.fixture
def unit_token_repo(mock_redis_client):
  return TokenRepository(mock_redis_client)