import pytest

# add_project

@pytest.mark.anyio
@pytest.mark.integration
async def test_add_project(integ_project_repo, integ_project_obj):
  result = await integ_project_repo.add_project(integ_project_obj)

  assert result.id
  assert result == integ_project_obj


# delete_project

@pytest.mark.anyio
@pytest.mark.integration
async def test_delete_project_success(integ_project_repo, registered_project_obj, db_session):
  result = await integ_project_repo.delete_project(registered_project_obj)

  await db_session.commit()

  still_exists = await integ_project_repo.get_by_id_and_owner(
    project_id=registered_project_obj.id,
    user_id=registered_project_obj.user_id,
    client_id=registered_project_obj.client_id
  )

  assert result == None
  assert still_exists is None


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


# get_all_by_owner

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_all_by_owner_success(integ_project_repo, registered_project_obj):
  result = await integ_project_repo.get_all_by_owner(
    registered_project_obj.user_id,
    registered_project_obj.client_id
  )

  assert len(result) == 1
  assert result[0] == registered_project_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_all_by_owner_return_empty_list_success(integ_project_repo):
  result = await integ_project_repo.get_all_by_owner(13, 21)

  assert len(result) == 0
  assert result == []