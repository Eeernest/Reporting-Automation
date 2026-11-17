import pytest

# add_project

@pytest.mark.anyio
@pytest.mark.integration
async def test_add_project(integ_project_repo, integ_project_obj):
  result = await integ_project_repo.add_project(integ_project_obj)

  assert result.id
  assert result == integ_project_obj


# get_by_id_and_owner

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_id_and_owner_success(
  integ_project_repo,
  registered_project_obj
):
  result = await integ_project_repo.get_by_id_and_owner(
    registered_project_obj.id,
    registered_project_obj.user_id,
    registered_project_obj.client_id
  )

  assert result == registered_project_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_id_and_owner_none_success(integ_project_repo):
  result = await integ_project_repo.get_by_id_and_owner(123, 1234, 42)

  assert result == None