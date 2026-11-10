import pytest

from app.enums.expense_enum import ExpenseType
from app.models.expense_model import Expense
from app.repositories.expense_repository import ExpenseRepository

# Integration

@pytest.fixture
async def integ_expense_repo(db_session):
  return ExpenseRepository(db_session)


# Objects

@pytest.fixture
async def integ_expense_obj(registered_item_obj, registered_project_obj):
  return Expense(
    project_id=registered_project_obj.id,
    item_id=registered_item_obj.id,
    expense_type=ExpenseType.materials,
    amount=3000.12
  )