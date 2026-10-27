import pytest
from sqlalchemy.exc import IntegrityError

import app.core.exceptions as e

# register_user

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_user_success(
  mock_security,
  mock_user_session,
  mock_user_repo,
  unit_user_service,
  mock_user_obj
):
  mock_security.get_password_hash.return_value = mock_user_obj.hashed_password
  mock_user_repo.add_user.return_value = mock_user_obj
  mock_user_session.commit.return_value = None

  result = await unit_user_service.register_user(
    username=mock_user_obj.username,
    email=mock_user_obj.email,
    password="Password123"
  )

  assert result == mock_user_obj

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_user_username_error(
  mock_security,
  mock_user_repo,
  unit_user_service,
  mock_user_obj
):
  mock_security.get_password_hash.return_value - mock_user_obj.hashed_password
  mock_user_repo.add_user.side_effect = IntegrityError(
    "stmt",
    "params",
    "username"
  )

  with pytest.raises(e.UsernameUnavailableError) as exc:
    await unit_user_service.register_user(
      username=mock_user_obj.username,
      email=mock_user_obj.email,
      password="Password123"
    )

  assert isinstance(exc.value, e.UsernameUnavailableError)
  assert exc.value.detail == e.UsernameUnavailableError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_user_email_error(
  mock_security,
  mock_user_repo,
  unit_user_service,
  mock_user_obj
):
  mock_security.get_password_hash.return_value - mock_user_obj.hashed_password
  mock_user_repo.add_user.side_effect = IntegrityError(
    "stmt",
    "params",
    "email"
  )

  with pytest.raises(e.EmailUnavailableError) as exc:
    await unit_user_service.register_user(
      username=mock_user_obj.username,
      email=mock_user_obj.email,
      password="Password123"
    )

  assert isinstance(exc.value, e.EmailUnavailableError)
  assert exc.value.detail == e.EmailUnavailableError.detail