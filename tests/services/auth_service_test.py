import pytest

import app.core.exceptions as e

# login method

@pytest.mark.anyio
@pytest.mark.unit
async def test_login_success(
  mock_security,
  mock_token_repo,
  mock_user_repo,
  unit_auth_service,
  access_payload_obj,
  refresh_payload_obj,
  mock_user_obj
):
  mock_user_repo.get_by_username.return_value = mock_user_obj
  mock_security.verify_password.return_value = True
  mock_security.create_access_token_payload.return_value = access_payload_obj
  mock_security.create_refresh_token_payload.return_value = refresh_payload_obj
  mock_token_repo.sore_refresh_token.return_value = None
  mock_security.get_encoded_access_token.return_value = "access_token"
  mock_security.get_encoded_refresh_token.return_value = "refresh_token"

  result = await unit_auth_service.login(mock_user_obj.username, "Password123")

  assert result["access_token"] == "access_token"
  assert result["refresh_token"] == "refresh_token"
  assert result["token_type"] == "bearer"

@pytest.mark.anyio
@pytest.mark.unit
async def test_login_user_not_found(
  mock_security,
  mock_user_repo,
  unit_auth_service
):
  mock_user_repo.get_by_username.return_value = None
  mock_security.verify_password.return_value = False

  with pytest.raises(e.InvalidCredentialsError) as exc:
    await unit_auth_service.login("user", "Password123")

  assert exc.value.status_code == e.InvalidCredentialsError.status_code
  assert exc.value.detail == e.InvalidCredentialsError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_login_wrong_password(
  mock_security,
  mock_user_repo,
  unit_auth_service,
  mock_user_obj
):
  mock_user_repo.get_by_username.return_value = mock_user_obj
  mock_security.verify_password.return_value = False

  with pytest.raises(e.InvalidCredentialsError) as exc:
    await unit_auth_service.login(mock_user_obj.username, "Wrongpassword")

  assert exc.value.status_code == e.InvalidCredentialsError.status_code
  assert exc.value.detail == e.InvalidCredentialsError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_login_user_inactive(
  mock_security,
  mock_user_repo,
  unit_auth_service,
  mock_user_obj
):
  mock_user_obj.is_active = False

  mock_user_repo.get_by_username.return_value = mock_user_obj
  mock_security.verify_password.return_value = True

  with pytest.raises(e.UserInactiveError) as exc:
    await unit_auth_service.login(mock_user_obj.username, "Password123")

  assert exc.value.status_code == e.UserInactiveError.status_code
  assert exc.value.detail == e.UserInactiveError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_login_user_deleted(
  mock_security,
  mock_user_repo,
  unit_auth_service,
  mock_user_obj
):
  mock_user_obj.is_deleted = True

  mock_user_repo.get_by_username.return_value = mock_user_obj
  mock_security.verify_password.return_value = True

  with pytest.raises(e.UserDeletedError) as exc:
    await unit_auth_service.login(mock_user_obj.username, "Password123")

  assert exc.value.status_code == e.UserDeletedError.status_code
  assert exc.value.detail == e.UserDeletedError.detail