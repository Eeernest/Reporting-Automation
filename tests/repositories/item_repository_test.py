import pytest

# Item Model

# add_item

@pytest.mark.anyio
@pytest.mark.integration
async def test_add_item_success(integ_item_repo, integ_item_obj):
  result = await integ_item_repo.add_item(integ_item_obj)

  assert result.id
  assert result == integ_item_obj


# delete_item

@pytest.mark.anyio
@pytest.mark.integration
async def test_delete_item_success(
  integ_item_repo,
  registered_item_obj,
  registered_project_obj
):
  await integ_item_repo.delete_item(registered_item_obj)

  still_exists = await integ_item_repo.get_by_id_and_owner(
    registered_item_obj.id,
    registered_item_obj.project_id,
    registered_project_obj.user_id
  )

  assert still_exists is None


# get_by_id_and_owner

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_id_and_owner_success(
  integ_item_repo,
  registered_item_obj,
  registered_project_obj
):
  result = await integ_item_repo.get_by_id_and_owner(
    registered_item_obj.id,
    registered_item_obj.project_id,
    registered_project_obj.user_id
  )

  assert result == registered_item_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_id_and_owner_return_none_success(integ_item_repo):
  result = await integ_item_repo.get_by_id_and_owner(123, 432, 123)

  assert result == None


# get_all_by_owner

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_all_by_owner_success(
  integ_item_repo,
  registered_item_obj,
  registered_project_obj
):
  result = await integ_item_repo.get_all_by_owner(
    registered_item_obj.project_id,
    registered_project_obj.user_id
  )

  assert len(result) == 1
  assert result[0] == registered_item_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_all_by_owner_return_empty_list_success(integ_item_repo):
  result = await integ_item_repo.get_all_by_owner(44, 65)

  assert len(result) == 0
  assert result == []


# ItemStatusModel

# add_status_history

@pytest.mark.anyio
@pytest.mark.integration
async def test_add_status_history(integ_item_repo, integ_item_status_obj):
  result = await integ_item_repo.add_status_history(integ_item_status_obj)

  assert result.id
  assert result == integ_item_status_obj


# get_status_history_by_id_and_owner

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_status_history_by_id_and_owner_success(
  integ_item_repo,
  commited_item_status_obj
):
  result = await integ_item_repo.get_status_history_by_id_and_owner(
    commited_item_status_obj.id,
    commited_item_status_obj.item_id
  )

  assert result == commited_item_status_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_satus_history_by_id_and_owner_return_none_success(
  integ_item_repo
):
  result = await integ_item_repo.get_status_history_by_id_and_owner(21, 13)

  assert result is None