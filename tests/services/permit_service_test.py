import pytest

import app.core.exceptions as e

# get_current_user method

@pytest.mark.anyio
@pytest.mark.unit
async def test_get_current_user_success(
  mock_security,
  mock_user_repo,
  unit_permit_service,
  access_payload_obj,
  mock_user_obj
):
  mock_security.get_decoded_access_token.return_value = access_payload_obj
  mock_user_repo.get_by_id.return_value = mock_user_obj

  result = await unit_permit_service.get_current_user("encoded_access_token")

  assert result == mock_user_obj

@pytest.mark.anyio
@pytest.mark.unit
async def test_get_current_user_invalid_token_error(
  mock_security,
  mock_user_repo,
  unit_permit_service,
  access_payload_obj
):
  mock_security.get_decoded_access_token.return_value = access_payload_obj
  mock_user_repo.get_by_id.return_value = None

  with pytest.raises(e.InvalidTokenError) as exc:
    await unit_permit_service.get_current_user("encoded_access_token")

  assert exc.value.status_code == e.InvalidTokenError.status_code
  assert exc.value.detail == e.InvalidTokenError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_get_current_user_inactive_error(
  mock_security,
  mock_user_repo,
  unit_permit_service,
  access_payload_obj,
  mock_user_obj
):
  mock_user_obj.is_active = False
  
  mock_security.get_decoded_access_token.return_value = access_payload_obj
  mock_user_repo.get_by_id.return_value = mock_user_obj

  with pytest.raises(e.UserInactiveError) as exc:
    await unit_permit_service.get_current_user("encoded_access_token")

  assert exc.value.status_code == e.UserInactiveError.status_code
  assert exc.value.detail == e.UserInactiveError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_get_current_user_deleted_error(
  mock_security,
  mock_user_repo,
  unit_permit_service,
  access_payload_obj,
  mock_user_obj
):
  mock_user_obj.is_deleted = True

  mock_security.get_decoded_access_token.return_value = access_payload_obj
  mock_user_repo.get_by_id.return_value = mock_user_obj

  with pytest.raises(e.UserDeletedError) as exc:
    await unit_permit_service.get_current_user("encoded_access_token")

  assert exc.value.status_code == e.UserDeletedError.status_code
  assert exc.value.detail == e.UserDeletedError.detail