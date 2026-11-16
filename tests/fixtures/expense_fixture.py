from unittest.mock import AsyncMock

from httpx import AsyncClient, ASGITransport
import pytest

from app.dependencies.expense_dependency import get_expense_service
from app.dependencies.item_dependency import get_verified_item
from app.dependencies.project_dependency import get_verified_project
from app.enums.expense_enum import ExpenseType
from app.main import app
from app.models.expense_model import Expense
from app.repositories.expense_repository import ExpenseRepository
from app.services.expense_service import ExpenseService

# Integration

@pytest.fixture
async def integ_expense_repo(db_session):
  return ExpenseRepository(db_session)

@pytest.fixture
def integ_expense_service(integ_expense_repo, db_session):
  return ExpenseService(integ_expense_repo, db_session)

@pytest.fixture
async def integ_expense_router(
  integ_expense_service,
  registered_project_obj,
  registered_item_obj
):
  app.dependency_overrides[get_verified_project] = lambda: registered_project_obj
  app.dependency_overrides[get_verified_item] = lambda: registered_item_obj
  app.dependency_overrides[get_expense_service] = lambda: integ_expense_service

  async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
    yield c

  app.dependency_overrides.clear()


# Unit

@pytest.fixture
async def mock_expense_repo():
  return AsyncMock()

@pytest.fixture
async def mock_expense_session():
  return AsyncMock()

@pytest.fixture
def unit_expense_service(
  mock_expense_repo,
  mock_expense_session
):
  return ExpenseService(
    mock_expense_repo,
    mock_expense_session
  ) 


# Objects

@pytest.fixture
def integ_expense_obj(registered_item_obj, registered_project_obj):
  return Expense(
    project_id=registered_project_obj.id,
    item_id=registered_item_obj.id,
    expense_type=ExpenseType.materials,
    amount=3000.12
  )

@pytest.fixture
def unit_expense_obj():
  return Expense(
    project_id=12,
    item_id=13,
    expense_type=ExpenseType.materials,
    amount=3000.12
  )