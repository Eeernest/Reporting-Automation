import pytest

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_user_success(
  mock_security,
  mock_user_repo,
  unit_user_service,
  mock_user_obj
):
  mock_security.get_password_hash.return_value = mock_user_obj.hashed_password
  mock_user_repo.save_user.return_value = mock_user_obj

  result = await unit_user_service.register_user(
    mock_user_obj.username,
    mock_user_obj.email,
    "Password123"
  )

  assert result == mock_user_obj