from unittest.mock import AsyncMock

import pytest

from app.enums.item_enum import ItemStatus, ItemType
from app.models.item_model import Item
from app.repositories.item_repository import ItemRepository
from app.services.item_service import ItemService

# Integration

@pytest.fixture
def integ_item_repo(db_session):
  return ItemRepository(db_session)


# Unit

@pytest.fixture
def mock_item_repo():
  return AsyncMock()

@pytest.fixture
def mock_item_session():
  return AsyncMock()

@pytest.fixture
def unit_item_service(mock_item_repo, mock_project_repo, mock_item_session):
  return ItemService(mock_item_repo, mock_project_repo, mock_item_session)


# Objects

@pytest.fixture
def integ_item_obj(registered_project_obj):
  return Item(
    project_id=registered_project_obj.id,
    name="test item",
    item_type=ItemType.wardrobe,
    item_status=ItemStatus.estimation,
    description="project dsecription",
  )

@pytest.fixture
def unit_item_obj():
  return Item(
    id=122,
    project_id=123,
    name="test item",
    item_type=ItemType.wardrobe,
    item_status=ItemStatus.estimation,
    description="project dsecription",
  )