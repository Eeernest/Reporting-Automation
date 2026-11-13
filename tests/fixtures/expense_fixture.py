from unittest.mock import AsyncMock

import pytest

from app.enums.expense_enum import ExpenseType
from app.models.expense_model import Expense
from app.repositories.expense_repository import ExpenseRepository
from app.services.expense_service import ExpenseService

# Integration

@pytest.fixture
async def integ_expense_repo(db_session):
  return ExpenseRepository(db_session)


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