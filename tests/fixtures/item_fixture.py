from unittest.mock import AsyncMock

from httpx import AsyncClient, ASGITransport
import pytest

from app.dependencies.item_dependency import get_item_service
from app.dependencies.permit_dependency import get_current_user
from app.enums.item_enum import ItemStatus, ItemType
from app.main import app
from app.models.item_model import Item
from app.repositories.item_repository import ItemRepository
from app.services.item_service import ItemService

# Integration

@pytest.fixture
def integ_item_repo(db_session):
  return ItemRepository(db_session)

@pytest.fixture
def integ_item_service(integ_item_repo, db_session):
  return ItemService(integ_item_repo, db_session)

@pytest.fixture
async def integ_item_router(integ_item_service, saved_user_obj):
  app.dependency_overrides[get_current_user] = lambda: saved_user_obj
  app.dependency_overrides[get_item_service] = lambda: integ_item_service

  async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
    yield c

  app.dependency_overrides.clear()


# Unit

@pytest.fixture
def mock_item_repo():
  return AsyncMock()

@pytest.fixture
def mock_item_session():
  return AsyncMock()

@pytest.fixture
def unit_item_service(mock_item_repo, mock_item_session):
  return ItemService(mock_item_repo, mock_item_session)


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
async def registered_item_obj(
  integ_item_service,
  integ_item_obj,
  registered_project_obj
):
  return await integ_item_service.register_item(
    user_id=registered_project_obj.user_id,
    project_id=registered_project_obj.id,
    name=integ_item_obj.name,
    item_type=integ_item_obj.item_type,
    item_status=integ_item_obj.item_status,
    description=integ_item_obj.description
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