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


# get_by_id_and_owner

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_id_and_owner_success(
  integ_expense_repo,
  registered_expense_obj
):
  result = await integ_expense_repo.get_by_id_and_owner(
    registered_expense_obj.id,
    project_id=registered_expense_obj.project_id,
    item_id=registered_expense_obj.item_id
  )

  assert result == registered_expense_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_id_and_owner_no_item_id_success(
  integ_expense_repo,
  registered_expense_obj
):
  registered_expense_obj.item_id = None

  result = await integ_expense_repo.get_by_id_and_owner(
    registered_expense_obj.id,
    registered_expense_obj.project_id,
    registered_expense_obj.item_id
  )

  assert result == registered_expense_obj
  assert result.item_id is None

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_id_and_owner_return_none(integ_expense_repo):
  result = await integ_expense_repo.get_by_id_and_owner(1231, 4324, 1231)

  assert result is None


# get_all_by_owner

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_all_by_owner_success(integ_expense_repo, registered_expense_obj):
  result = await integ_expense_repo.get_all_by_owner(
    registered_expense_obj.project_id,
    registered_expense_obj.item_id
  )

  assert len(result) == 1
  assert result[0] == registered_expense_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_all_by_owner_no_item_id_success(
  integ_expense_repo,
  registered_expense_obj
):
  registered_expense_obj.item_id = None
  
  result = await integ_expense_repo.get_all_by_owner(registered_expense_obj.project_id)

  assert len(result) == 1
  assert result[0] == registered_expense_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_all_by_owner_return_empty_list_success(integ_expense_repo):
  result = await integ_expense_repo.get_all_by_owner(5, 8)

  assert len(result) == 0
  assert result == []