import pytest
from sqlalchemy.exc import IntegrityError

import app.core.exceptions as e

# register_expense

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_expense_success(
  mock_expense_repo,
  mock_expense_session,
  unit_expense_service,
  unit_expense_obj,
):
  mock_expense_repo.add_expense.return_value = unit_expense_obj
  mock_expense_session.commit.return_value = None

  result = await unit_expense_service.register_expense(
    project_id=unit_expense_obj.id,
    item_id=unit_expense_obj.id,
    expense_type=unit_expense_obj.expense_type,
    amount=unit_expense_obj.amount
  )

  assert result == unit_expense_obj

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_expense_database_error(
  mock_expense_repo,
  mock_expense_session,
  unit_expense_service,
  unit_expense_obj,
):
  mock_expense_repo.add_expense.side_effect = IntegrityError(
    "stmt",
    "params",
    "unknown_error"
  )

  mock_expense_session.rollback.return_value = None

  with pytest.raises(e.DatabaseIntegrityError) as exc:
    await unit_expense_service.register_expense(
      project_id=unit_expense_obj.id,
      item_id=unit_expense_obj.id,
      expense_type=unit_expense_obj.expense_type,
      amount=unit_expense_obj.amount
    )

  assert isinstance(exc.value, e.DatabaseIntegrityError)
  assert exc.value.detail == e.DatabaseIntegrityError.detail


# get_expense

@pytest.mark.anyio
@pytest.mark.unit
async def test_get_expense_success(
  mock_expense_repo,
  unit_expense_service,
  unit_expense_obj
):
  mock_expense_repo.get_by_id_and_owner.return_value = unit_expense_obj

  result = await unit_expense_service.get_expense(
    unit_expense_obj.id,
    unit_expense_obj.project_id,
    unit_expense_obj.item_id
  )

  assert result == unit_expense_obj

@pytest.mark.anyio
@pytest.mark.unit
async def test_get_expense_no_item__id_success(
  mock_expense_repo,
  unit_expense_service,
  unit_expense_obj
):
  unit_expense_obj.item_id = None
  
  mock_expense_repo.get_by_id_and_owner.return_value = unit_expense_obj

  result = await unit_expense_service.get_expense(
    unit_expense_obj.id,
    unit_expense_obj.project_id,
    unit_expense_obj.item_id
  )

  assert result == unit_expense_obj

@pytest.mark.anyio
@pytest.mark.unit
async def test_get_expense_not_found_error(mock_expense_repo, unit_expense_service):
  mock_expense_repo.get_by_id_and_owner.return_value = None

  with pytest.raises(e.ExpenseNotFoundError) as exc:
    await unit_expense_service.get_expense(1231, 213, 12)

  assert isinstance(exc.value, e.ExpenseNotFoundError)
  assert exc.value.detail == e.ExpenseNotFoundError.detail