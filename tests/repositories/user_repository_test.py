import pytest
from sqlalchemy.exc import IntegrityError

import app.core.exceptions as e

# save

@pytest.mark.anyio
@pytest.mark.integration
async def test_save_user_success(integ_user_repo, integ_user_obj):
  result = await integ_user_repo.save_user(integ_user_obj)

  assert result.id is not None
  assert result.username == integ_user_obj.username
  assert result.email == integ_user_obj.email

@pytest.mark.anyio
@pytest.mark.integration
async def test_save_user_duplicate_username_error(
  integ_user_repo,
  duplicate_user_obj
):
  with pytest.raises(e.UsernameUnavailableError) as exc:
    await integ_user_repo.save_user(duplicate_user_obj)

  assert isinstance(exc.value, e.UsernameUnavailableError)
  assert exc.value.detail == e.UsernameUnavailableError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_save_user_username_error(
  mock_user_session,
  unit_user_repo,
  mock_user_obj
):
  mock_user_session.commit.side_effect = IntegrityError(
    "stmt",
    "params",
    "username"
  )

  with pytest.raises(e.UsernameUnavailableError) as exc:
    await unit_user_repo.save_user(mock_user_obj)

  assert isinstance(exc.value, e.UsernameUnavailableError)
  assert exc.value.detail == e.UsernameUnavailableError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_save_user_email_error(
  mock_user_session,
  unit_user_repo,
  mock_user_obj
):
  mock_user_session.commit.side_effect = IntegrityError(
    "stmt",
    "params",
    "email"
  )

  with pytest.raises(e.EmailUnavailableError) as exc:
    await unit_user_repo.save_user(mock_user_obj)

  assert isinstance(exc.value, e.EmailUnavailableError)
  assert exc.value.detail == e.EmailUnavailableError.detail


# get_by_id

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_id_return_obj_success(integ_user_repo, saved_user_obj):
  result = await integ_user_repo.get_by_id(saved_user_obj.id)

  assert result == saved_user_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_id_return_none(integ_user_repo):
  result = await integ_user_repo.get_by_id(1)

  assert result == None


# get_by_username

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_username_return_obj_success(integ_user_repo, saved_user_obj):
  result = await integ_user_repo.get_by_username(saved_user_obj.username)

  assert result == saved_user_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_username_return_none(integ_user_repo):
  result = await integ_user_repo.get_by_username("user123")

  assert result == None