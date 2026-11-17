import pytest

# save_client

@pytest.mark.anyio
@pytest.mark.integration
async def test_add_client(integ_client_repo, integ_client_obj):
  result = await integ_client_repo.add_client(integ_client_obj)

  assert result.id
  assert result == integ_client_obj


# get_by_id_and_user_id

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_id_and_owner_success(integ_client_repo, registered_client_obj):
  result = await integ_client_repo.get_by_id_and_owner(
    registered_client_obj.id,
    registered_client_obj.user_id
  )

  assert result == registered_client_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_id_and_owner_none_success(integ_client_repo):
  result = await integ_client_repo.get_by_id_and_owner(12, 12)

  assert result == None

# get_all_by_owner

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_all_by_owner_success(integ_client_repo, registered_client_obj):
  result = await integ_client_repo.get_all_by_owner(registered_client_obj.user_id)

  assert len(result) == 1
  assert result[0] == registered_client_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_all_by_owner_return_none_success(integ_client_repo):
  result = await integ_client_repo.get_all_by_owner(11235813)

  assert len(result) == 0