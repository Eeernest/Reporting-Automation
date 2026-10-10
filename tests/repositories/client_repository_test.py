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
@pytest.mark.unit
async def test_save_client_name_error(
  mock_client_session,
  unit_client_repo,
  unit_client_obj
):
  mock_client_session.commit.side_effect = IntegrityError("stmt", "params", "name")

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
  mock_client_session.commit.side_effect = IntegrityError("stmt", "params", "company")

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
  mock_client_session.commit.side_effect = IntegrityError("stmt", "params", "email")

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
  mock_client_session.commit.side_effect = IntegrityError("stmt", "params", "phone_number")

  with pytest.raises(e.PhoneUnavailableError) as exc:
    await unit_client_repo.save_client(unit_client_obj)

  assert exc.value.status_code == e.PhoneUnavailableError.status_code
  assert exc.value.detail == e.PhoneUnavailableError.detail


# get_by_name

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_name_return_obj_success(integ_client_repo, saved_client_obj):
  result = await integ_client_repo.get_by_name(saved_client_obj.name)

  assert result == saved_client_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_name_return_none_success(integ_client_repo):
  result = await integ_client_repo.get_by_name("name")

  assert result == None


# get_by_company

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_company_return_obj_success(integ_client_repo, saved_client_obj):
  result = await integ_client_repo.get_by_company(saved_client_obj.company)

  assert result == saved_client_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_company_return_none_success(integ_client_repo):
  result = await integ_client_repo.get_by_company("company")

  assert result == None


# get_by_email

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_email_return_obj_success(integ_client_repo, saved_client_obj):
  result = await integ_client_repo.get_by_email(saved_client_obj.email)

  assert result == saved_client_obj

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_by_email_return_none_success(integ_client_repo):
  result = await integ_client_repo.get_by_email("email")

  assert result == None