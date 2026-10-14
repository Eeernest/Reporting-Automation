import pytest

# save

@pytest.mark.anyio
@pytest.mark.integration
async def test_save_user_obj_success(integ_user_repo, user_obj):
  result = await integ_user_repo.save(user_obj)

  assert result.id is not None
  assert result.username == user_obj.username
  assert result.email == user_obj.email