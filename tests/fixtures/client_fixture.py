from unittest.mock import AsyncMock

import pytest

from app.models.client_model import Client
from app.repositories.client_repository import ClientRepository

# Integration

@pytest.fixture
def integ_client_repo(db_session):
  return ClientRepository(db_session)


# Unit

@pytest.fixture
def mock_client_repo():
  return AsyncMock()

@pytest.fixture
def mock_client_session():
  return AsyncMock()

@pytest.fixture
def unit_client_repo(mock_client_session):
  return ClientRepository(mock_client_session)


# Object

@pytest.fixture
def client_obj():
  return Client(
    id=1,
    user_id=1,
    name="client1",
    company="company1",
    email="company1@example.com",
    phone_number="+4812345678",
    notes="notes",
  )