from sqlalchemy.exc import IntegrityError

import pytest

import app.core.exceptions as e

# register_project

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_project_success(
  mock_client_repo,
  mock_project_repo,
  mock_project_session,
  unit_project_service,
  unit_project_obj,
  unit_client_obj
):
  mock_client_repo.get_by_id_and_user_id.return_value = unit_client_obj
  mock_project_repo.add_project.return_value = unit_project_obj
  mock_project_session.commit.return_value = None

  result = await unit_project_service.register_project(
    user_id=1,
    client_id=unit_project_obj.client_id,
    name=unit_project_obj.name,
    location=unit_project_obj.location,
    description=unit_project_obj.description,
    est_end_date=unit_project_obj.est_end_date,
    act_end_date=unit_project_obj.act_end_date
  )

  assert result == unit_project_obj

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_project_client_not_found_errror(
  mock_client_repo,
  unit_project_service
):
  mock_client_repo.get_by_id_and_user_id.return_value = None

  with pytest.raises(e.ClientNotFoundError) as exc:
    await unit_project_service.register_project(
      112,
      123,
      "name",
    )

  assert isinstance(exc.value, e.ClientNotFoundError)
  assert exc.value.detail == e.ClientNotFoundError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_project_required_credentials_success(
  mock_client_repo,
  mock_project_repo,
  mock_project_session,
  unit_project_service,
  unit_project_obj,
  unit_client_obj
):
  unit_project_obj.location = None
  unit_project_obj.description = None
  unit_project_obj.est_end_date = None
  unit_project_obj.act_end_date = None

  mock_client_repo.get_by_id_and_user_id.return_value = unit_client_obj
  mock_project_repo.add_project.return_value = unit_project_obj
  mock_project_session.commit.return_value = None

  result = await unit_project_service.register_project(
    user_id=1,
    client_id=unit_project_obj.client_id,
    name=unit_project_obj.name,
    location=unit_project_obj.location,
    description=unit_project_obj.description,
    est_end_date=unit_project_obj.est_end_date,
    act_end_date=unit_project_obj.act_end_date
  )

  assert result == unit_project_obj

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_client_database_integrity_error(
  mock_client_repo,
  mock_project_repo,
  mock_project_session,
  unit_project_service,
  unit_project_obj,
  unit_client_obj
):
  mock_client_repo.get_by_id_and_user_id.return_value = unit_client_obj
  mock_project_repo.add_project.side_effect = IntegrityError(
    "stmt",
    "params",
    "db_error"
  )

  mock_project_session.rollback.return_value = None

  with pytest.raises(e.DatabaseIntegrityError) as exc:
    await unit_project_service.register_project(
      user_id=1,
      client_id=unit_project_obj.client_id,
      name=unit_project_obj.name,
      location=unit_project_obj.location,
      description=unit_project_obj.description,
      est_end_date=unit_project_obj.est_end_date,
      act_end_date=unit_project_obj.act_end_date
    )

  assert isinstance(exc.value, e.DatabaseIntegrityError)
  assert exc.value.detail == e.DatabaseIntegrityError.detail