import pytest

from app.models.item_model import ItemStatus, ItemType, Item
from app.repositories.item_repository import ItemRepository

# Integration

@pytest.fixture
def integ_item_repo(db_session):
  return ItemRepository(db_session)


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