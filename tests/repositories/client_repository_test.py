import pytest
from sqlalchemy.exc import IntegrityError

import app.core.exceptions as e

# save_client

@pytest.mark.anyio
@pytest.mark.integration
async def test_save_client_success(integ_client_repo, integ_client_obj):
  result = await integ_client_repo.save_client(integ_client_obj)

  assert result.id
  assert result.name == integ_client_obj.name
  assert result.phone_number == integ_client_obj.phone_number

@pytest.mark.anyio
@pytest.mark.integration
async def test_save_client_duplicate_name_error(integ_client_repo, duplicate_client_obj):
  with pytest.raises(e.NameUnavailableError) as exc:
    await integ_client_repo.save_client(duplicate_client_obj)

  assert exc.value.status_code == e.NameUnavailableError.status_code
  assert exc.value.detail == e.NameUnavailableError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_save_client_name_error(
  mock_client_session,
  unit_client_repo,
  unit_client_obj
):
  mock_client_session.commit.side_effect = IntegrityError(
    "stmt",
    "params",
    "user_client_name"
  )

  with pytest.raises(e.NameUnavailableError) as exc:
    await unit_client_repo.save_client(unit_client_obj)

  assert exc.value.status_code == e.NameUnavailableError.status_code
  assert exc.value.detail == e.NameUnavailableError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_save_client_company_error(
  mock_client_session,
  unit_client_repo,
  unit_client_obj
):
  mock_client_session.commit.side_effect = IntegrityError(
    "stmt",
    "params",
    "user_client_company"
  )

  with pytest.raises(e.CompanyUnavailableError) as exc:
    await unit_client_repo.save_client(unit_client_obj)

  assert exc.value.status_code == e.CompanyUnavailableError.status_code
  assert exc.value.detail == e.CompanyUnavailableError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_save_client_email_error(
  mock_client_session,
  unit_client_repo,
  unit_client_obj
):
  mock_client_session.commit.side_effect = IntegrityError(
    "stmt",
    "params",
    "user_client_email"
  )

  with pytest.raises(e.EmailUnavailableError) as exc:
    await unit_client_repo.save_client(unit_client_obj)

  assert exc.value.status_code == e.EmailUnavailableError.status_code
  assert exc.value.detail == e.EmailUnavailableError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_save_client_phone_number_error(
  mock_client_session,
  unit_client_repo,
  unit_client_obj
):
  mock_client_session.commit.side_effect = IntegrityError(
    "stmt",
    "params",
    "user_client_phone_number"
  )

  with pytest.raises(e.PhoneUnavailableError) as exc:
    await unit_client_repo.save_client(unit_client_obj)

  assert exc.value.status_code == e.PhoneUnavailableError.status_code
  assert exc.value.detail == e.PhoneUnavailableError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_save_client_database_integrity_error(
  mock_client_session,
  unit_client_repo,
  unit_client_obj
):
  mock_client_session.commit.side_effect = IntegrityError("stmt", "params", "unknown")

  with pytest.raises(e.DatabaseIntegrityError) as exc:
    await unit_client_repo.save_client(unit_client_obj)

  assert exc.value.status_code == e.DatabaseIntegrityError.status_code
  assert exc.value.detail == e.DatabaseIntegrityError.detail


# get_by_phone_number

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_phone_number_return_obj_success(
  integ_client_repo,
  saved_client_obj
):
  result = await integ_client_repo.get_by_phone_number(saved_client_obj.phone_number)

  assert result == saved_client_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_phone_number_return_none_success(integ_client_repo):
  result = await integ_client_repo.get_by_phone_number("phone_number")

  assert result == None