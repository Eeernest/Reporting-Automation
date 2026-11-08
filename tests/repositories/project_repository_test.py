import pytest

# add_project

@pytest.mark.anyio
@pytest.mark.integration
async def test_add_project(integ_project_repo, integ_project_obj):
  result = await integ_project_repo.add_project(integ_project_obj)

  assert result.id
  assert result == integ_project_obj


# get_by_id_and_user_id

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_id_and_user_id_success(
  integ_project_repo,
  registered_project_obj
):
  result = await integ_project_repo.get_by_id_and_user_id(
    registered_project_obj.id,
    registered_project_obj.user_id
  )

  assert result == registered_project_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_id_and_user_id_none_success(integ_project_repo):
  result = await integ_project_repo.get_by_id_and_user_id(123, 1234)

  assert result == None