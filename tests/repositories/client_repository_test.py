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
async def test_get_by_id_and_user_id_success(integ_client_repo, registered_client_obj):
  result = await integ_client_repo.get_by_id_and_user_id(
    registered_client_obj.id,
    registered_client_obj.user_id
  )

  assert result == registered_client_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_id_and_user_id_None_success(integ_client_repo):
  result = await integ_client_repo.get_by_id_and_user_id(12, 12)

  assert result == None