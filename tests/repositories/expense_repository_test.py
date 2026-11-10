import pytest

# add_expense

@pytest.mark.anyio
@pytest.mark.integration
async def test_add_expense_success(integ_expense_repo, integ_expense_obj):
  result = await integ_expense_repo.add_expense(integ_expense_obj)

  assert result == integ_expense_obj
  assert result.id

@pytest.mark.anyio
@pytest.mark.integration
async def test_add_expense_only_required_success(integ_expense_repo, integ_expense_obj):
  integ_expense_obj.item_id = None
  integ_expense_obj.amount = None

  result = await integ_expense_repo.add_expense(integ_expense_obj)

  assert result == integ_expense_obj
  assert result.id