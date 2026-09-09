import pytest
from sqlalchemy.exc import IntegrityError

import app.core.exceptions as e

# create_account

@pytest.mark.anyio
@pytest.mark.unit
async def test_create_account_success(mock_user_security, mock_user_repo, unit_user_service, user_request_data, unit_user_obj):
  mock_user_repo.get_by_username.return_value = None
  mock_user_repo.get_by_email.return_value = None
  mock_user_security.get_password_hash.return_value = unit_user_obj.hashed_password
  mock_user_repo.save.return_value = unit_user_obj

  result = await unit_user_service.create_account(user_request_data)

  assert result == unit_user_obj
  assert mock_user_repo.save.call_count == 1

@pytest.mark.anyio
@pytest.mark.unit
async def test_create_account_username_unavailable_error(mock_user_repo, unit_user_service, user_request_data, unit_user_obj):
  mock_user_repo.get_by_username.return_value = unit_user_obj

  with pytest.raises(e.UsernameUnavailableError) as exc:
    await unit_user_service.create_account(user_request_data)

  assert exc.value.status_code == e.UsernameUnavailableError.status_code
  assert exc.value.detail == e.UsernameUnavailableError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_create_account_email_unavailable_error(mock_user_repo, unit_user_service, user_request_data, unit_user_obj):
  mock_user_repo.get_by_username.return_value = None
  mock_user_repo.get_by_email.return_value = unit_user_obj


  with pytest.raises(e.EmailUnavailableError) as exc:
    await unit_user_service.create_account(user_request_data)

  assert exc.value.status_code == e.EmailUnavailableError.status_code
  assert exc.value.detail == e.EmailUnavailableError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_create_account_username_race_condition(mock_user_security, mock_user_repo, unit_user_service, user_request_data, unit_user_obj):
  mock_user_repo.get_by_username.return_value = None
  mock_user_repo.get_by_email.return_value = None
  mock_user_security.get_password_hash.return_value = unit_user_obj.hashed_password
  mock_user_repo.save.side_effect = IntegrityError("stmt", "params", "username")

  with pytest.raises(e.UsernameUnavailableError) as exc:
    await unit_user_service.create_account(user_request_data)

  assert exc.value.status_code == e.UsernameUnavailableError.status_code
  assert exc.value.detail == e.UsernameUnavailableError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_create_account_email_race_condition(mock_user_security, mock_user_repo, unit_user_service, user_request_data, unit_user_obj):
  mock_user_repo.get_by_username.return_value = None
  mock_user_repo.get_by_email.return_value = None
  mock_user_security.get_password_hash.return_value = unit_user_obj.hashed_password
  mock_user_repo.save.side_effect = IntegrityError("stmt", "params", "email")

  with pytest.raises(e.EmailUnavailableError) as exc:
    await unit_user_service.create_account(user_request_data)

  assert exc.value.status_code == e.EmailUnavailableError.status_code
  assert exc.value.detail == e.EmailUnavailableError.detail