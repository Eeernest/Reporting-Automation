import pytest

# save_client

@pytest.mark.anyio
@pytest.mark.integration
async def test_add_client(integ_client_repo, integ_client_obj):
  result = await integ_client_repo.add_client(integ_client_obj)

  assert result.id
  assert result == integ_client_obj