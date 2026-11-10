import pytest

# add_item

@pytest.mark.anyio
@pytest.mark.integration
async def test_add_item_success(integ_item_repo, integ_item_obj):
  result = await integ_item_repo.add_item(integ_item_obj)

  assert result.id
  assert result == integ_item_obj


# get_by_id_and_project_id

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_id_and_project_id_success(integ_item_repo, registered_item_obj):
  result = await integ_item_repo.get_by_id_and_project_id(
    registered_item_obj.id,
    registered_item_obj.project_id
  )

  assert result == registered_item_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_id_and_project_id_return_none_success(integ_item_repo):
  result = await integ_item_repo.get_by_id_and_project_id(113, 123)

  assert result == None