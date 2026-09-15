import pytest

# Happy path test for store_refresh_token, delete_refresh_token and get_sub_by_jti methods 

@pytest.mark.anyio
@pytest.mark.integration
async def test_token_repository_full_cycle(token_repo, refresh_token_payload):
  await token_repo.store_refresh_token(
    refresh_token_payload["jti"],
    refresh_token_payload["exp"],
    refresh_token_payload["sub"]
  )

  stored_token = await token_repo.get_sub_by_jti(refresh_token_payload["jti"])

  assert stored_token == refresh_token_payload["sub"]

  await token_repo.delete_refresh_token(refresh_token_payload["jti"])

  deleted_token = await token_repo.get_sub_by_jti(refresh_token_payload["jti"])

  assert deleted_token == None