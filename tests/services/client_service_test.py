import pytest
from sqlalchemy.exc import IntegrityError

import app.core.exceptions as e

# register_client

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_client_succness(
  mock_client_repo,
  mock_client_session,
  unit_client_service,
  unit_client_obj
):
  mock_client_repo.add_client.return_value = unit_client_obj
  mock_client_session.commit.return_value = None

  result = await unit_client_service.register_client(
    user_id=unit_client_obj.user_id,
    name=unit_client_obj.name,
    phone_number=unit_client_obj.phone_number,
    email=unit_client_obj.email,
    notes=unit_client_obj.notes
  )

  assert result == unit_client_obj

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_client_name_error(
  mock_client_repo,
  unit_client_service,
  unit_client_obj
):
  mock_client_repo.add_client.side_effect = IntegrityError(
    "stmt",
    "params",
    "user_client_name"
  )

  with pytest.raises(e.NameUnavailableError) as exc:
    await unit_client_service.register_client(
      user_id=unit_client_obj.user_id,
      name=unit_client_obj.name,
      phone_number=unit_client_obj.phone_number,
      email=unit_client_obj.email,
      notes=unit_client_obj.notes
    )

  assert isinstance(exc.value, e.NameUnavailableError)
  assert exc.value.detail == e.NameUnavailableError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_client_email_error(
  mock_client_repo,
  unit_client_service,
  unit_client_obj
):
  mock_client_repo.add_client.side_effect = IntegrityError(
    "stmt",
    "params",
    "user_client_email"
  )

  with pytest.raises(e.EmailUnavailableError) as exc:
    await unit_client_service.register_client(
      user_id=unit_client_obj.user_id,
      name=unit_client_obj.name,
      phone_number=unit_client_obj.phone_number,
      email=unit_client_obj.email,
      notes=unit_client_obj.notes
    )

  assert isinstance(exc.value, e.EmailUnavailableError)
  assert exc.value.detail == e.EmailUnavailableError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_client_phone_number_error(
  mock_client_repo,
  unit_client_service,
  unit_client_obj
):
  mock_client_repo.add_client.side_effect = IntegrityError(
    "stmt",
    "params",
    "user_client_phone_number"
  )

  with pytest.raises(e.PhoneUnavailableError) as exc:
    await unit_client_service.register_client(
      user_id=unit_client_obj.user_id,
      name=unit_client_obj.name,
      phone_number=unit_client_obj.phone_number,
      email=unit_client_obj.email,
      notes=unit_client_obj.notes
    )

  assert isinstance(exc.value, e.PhoneUnavailableError)
  assert exc.value.detail == e.PhoneUnavailableError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_client_database_error(
  mock_client_repo,
  unit_client_service,
  unit_client_obj
):
  mock_client_repo.add_client.side_effect = IntegrityError(
    "stmt",
    "params",
    "unknown"
  )

  with pytest.raises(e.DatabaseIntegrityError) as exc:
    await unit_client_service.register_client(
      user_id=unit_client_obj.user_id,
      name=unit_client_obj.name,
      phone_number=unit_client_obj.phone_number,
      email=unit_client_obj.email,
      notes=unit_client_obj.notes
    )

  assert isinstance(exc.value, e.DatabaseIntegrityError)
  assert exc.value.detail == e.DatabaseIntegrityError.detail
