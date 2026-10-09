import pytest
from redis.exceptions import RedisError

import app.core.exceptions as e

# store_refresh_token method

@pytest.mark.anyio
@pytest.mark.integration
async def test_store_refresh_token_success(integ_token_repo, refresh_payload_obj):
  await integ_token_repo.store_refresh_token(
    refresh_payload_obj["jti"],
    refresh_payload_obj["sub"],
    refresh_payload_obj["exp"]
  )

  result = await integ_token_repo.get_sub_by_jti(refresh_payload_obj["jti"])

  assert result == refresh_payload_obj["sub"]

@pytest.mark.anyio
@pytest.mark.unit
async def test_store_refresh_token_redis_error(
  mock_redis_client,
  unit_token_repo,
  refresh_payload_obj
):
  mock_redis_client.set.side_effect = RedisError

  with pytest.raises(e.RedisFailureError) as exc:
    await unit_token_repo.store_refresh_token(
      refresh_payload_obj["jti"],
      refresh_payload_obj["sub"],
      refresh_payload_obj["exp"]
    )

  assert exc.value.status_code == e.RedisFailureError.status_code
  assert exc.value.detail == e.RedisFailureError.detail


# delete_refresh_token method

@pytest.mark.anyio
@pytest.mark.integration
async def test_delete_refresh_token_success(integ_token_repo, refresh_payload_obj):
  await integ_token_repo.store_refresh_token(
      refresh_payload_obj["jti"],
      refresh_payload_obj["sub"],
      refresh_payload_obj["exp"]
    )

  await integ_token_repo.delete_refresh_token(refresh_payload_obj["jti"])

  result = await integ_token_repo.get_sub_by_jti(refresh_payload_obj["jti"])

  assert result == None

@pytest.mark.anyio
@pytest.mark.unit
async def test_delete_refresh_token_redis_error(
  mock_redis_client,
  unit_token_repo,
  refresh_payload_obj
):
  mock_redis_client.delete.side_effect = RedisError

  with pytest.raises(e.RedisFailureError) as exc:
    await unit_token_repo.delete_refresh_token(refresh_payload_obj["jti"])

  assert exc.value.status_code == e.RedisFailureError.status_code
  assert exc.value.detail == e.RedisFailureError.detail