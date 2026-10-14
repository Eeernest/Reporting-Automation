import pytest

# save

@pytest.mark.anyio
@pytest.mark.integration
async def test_save_user_obj_success(integ_user_repo, user_obj):
  result = await integ_user_repo.save(user_obj)

  assert result.id is not None
  assert result.username == user_obj.username
  assert result.email == user_obj.email


# get_by_email

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_email_success(integ_user_repo, saved_user_obj):
  result = await integ_user_repo.get_by_email(saved_user_obj.email)

  assert result == saved_user_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_email_return_none_success(integ_user_repo):
  result = await integ_user_repo.get_by_email("user2@example.com")

  assert result == None