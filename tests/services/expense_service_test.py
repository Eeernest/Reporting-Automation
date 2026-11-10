import pytest
from sqlalchemy.exc import IntegrityError

import app.core.exceptions as e

# register_expense

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_expense_success(
  mock_expense_repo,
  mock_item_repo,
  mock_project_repo,
  mock_expense_session,
  unit_expense_service,
  unit_expense_obj,
  unit_project_obj,
  unit_item_obj
):
  mock_project_repo.get_by_id_and_user_id.return_value = unit_project_obj
  mock_item_repo.get_by_id_and_project_id.return_value = unit_item_obj
  mock_expense_repo.add_expense.return_value = unit_expense_obj
  mock_expense_session.commit.return_value = None

  result = await unit_expense_service.register_expense(
    user_id=unit_project_obj.user_id,
    project_id=unit_project_obj.id,
    item_id=unit_item_obj.id,
    expense_type=unit_expense_obj.expense_type,
    amount=unit_expense_obj.amount
  )

  assert result == unit_expense_obj

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_project_not_found_error(
  mock_project_repo,
  unit_expense_service,
  unit_expense_obj
):
  mock_project_repo.get_by_id_and_user_id.return_value = None

  with pytest.raises(e.ProjectNotFoundError) as exc:
    await unit_expense_service.register_expense(
    user_id=123,
    project_id=12,
    item_id=15,
    expense_type=unit_expense_obj.expense_type,
    amount=unit_expense_obj.amount
    )

  assert isinstance(exc.value, e.ProjectNotFoundError)
  assert exc.value.detail == e.ProjectNotFoundError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_expense_item_not_found_error(
  mock_item_repo,
  mock_project_repo,
  unit_expense_service,
  unit_expense_obj,
  unit_project_obj
):
  mock_project_repo.get_by_id_an_user_id.return_value = unit_project_obj
  mock_item_repo.get_by_id_and_project_id.return_value = None

  with pytest.raises(e.ItemNotFoundError) as exc:
    await unit_expense_service.register_expense(
      user_id=unit_project_obj.user_id,
      project_id=unit_project_obj.id,
      item_id=1234,
      expense_type=unit_expense_obj.expense_type,
      amount=unit_expense_obj.amount 
    )

  assert isinstance(exc.value, e.ItemNotFoundError)
  assert exc.value.detail == e.ItemNotFoundError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_expense_database_error(
  mock_expense_repo,
  mock_item_repo,
  mock_project_repo,
  mock_expense_session,
  unit_expense_service,
  unit_expense_obj,
  unit_project_obj,
  unit_item_obj
):
  mock_project_repo.get_by_id_and_user_id.return_value = unit_project_obj
  mock_item_repo.get_by_id_and_project_id.retun_value = unit_item_obj
  mock_expense_repo.add_expense.side_effect = IntegrityError(
    "stmt",
    "params",
    "unknown_error"
  )

  mock_expense_session.rollback.return_value = None

  with pytest.raises(e.DatabaseIntegrityError) as exc:
    await unit_expense_service.register_expense(
      user_id=unit_project_obj.user_id,
      project_id=unit_project_obj.id,
      item_id=unit_item_obj.id,
      expense_type=unit_expense_obj.expense_type,
      amount=unit_expense_obj.amount
    )

  assert isinstance(exc.value, e.DatabaseIntegrityError)
  assert exc.value.detail == e.DatabaseIntegrityError.detail