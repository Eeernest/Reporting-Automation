import pytest

# add_user

@pytest.mark.anyio
@pytest.mark.integration
async def test_add_user_success(integ_user_repo, integ_user_obj):
  result = await integ_user_repo.add_user(integ_user_obj)

  assert result.id
  assert result == integ_user_obj


# get_by_id

# @pytest.mark.anyio
# @pytest.mark.integration
# async def test_get_by_id_return_obj_success(integ_user_repo, saved_user_obj):
#   result = await integ_user_repo.get_by_id(saved_user_obj.id)

#   assert result == saved_user_obj

# @pytest.mark.anyio
# @pytest.mark.integration
# async def test_get_by_id_return_none(integ_user_repo):
#   result = await integ_user_repo.get_by_id(1)

#   assert result == None


# # get_by_username

# @pytest.mark.anyio
# @pytest.mark.integration
# async def test_get_by_username_return_obj_success(integ_user_repo, saved_user_obj):
#   result = await integ_user_repo.get_by_username(saved_user_obj.username)

#   assert result == saved_user_obj

# @pytest.mark.anyio
# @pytest.mark.integration
# async def test_get_by_username_return_none(integ_user_repo):
#   result = await integ_user_repo.get_by_username("user123")

#   assert result == None