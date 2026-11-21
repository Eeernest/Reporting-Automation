from sqlalchemy.exc import IntegrityError

import pytest

import app.core.exceptions as e

# register_project

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_project_success(
  mock_project_repo,
  mock_project_session,
  unit_project_service,
  unit_project_obj,
):
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
async def test_register_project_required_credentials_success(
  mock_project_repo,
  mock_project_session,
  unit_project_service,
  unit_project_obj,
):
  unit_project_obj.location = None
  unit_project_obj.description = None
  unit_project_obj.est_end_date = None
  unit_project_obj.act_end_date = None

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
  mock_project_repo,
  mock_project_session,
  unit_project_service,
  unit_project_obj,
):
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


# update_project

@pytest.mark.anyio
@pytest.mark.unit
async def test_update_project_success(
  mock_project_session,
  unit_project_service,
  unit_project_obj
):
  mock_project_session.commit.return_value = None

  result = await unit_project_service.update_project(unit_project_obj, {"name": "updated name"})

  assert result.name == "updated name"

@pytest.mark.anyio
@pytest.mark.unit
async def test_update_project_no_field_provided_error(
  unit_project_service,
  unit_project_obj
):
  with pytest.raises(e.NoFieldProvidedError) as exc:
    await unit_project_service.update_project(unit_project_obj, {})

  assert isinstance(exc.value, e.NoFieldProvidedError)
  assert exc.value.detail == e.NoFieldProvidedError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_update_project_integrity_error(
  mock_project_session,
  unit_project_service,
  unit_project_obj
):
  mock_project_session.commit.side_effect = IntegrityError(
    "stmt",
    "params",
    "db_error"
  )

  mock_project_session.rollback.return_value = None

  with pytest.raises(e.DatabaseIntegrityError) as exc:
    await unit_project_service.update_project(unit_project_obj, {"name": "test"})

  assert isinstance(exc.value, e.DatabaseIntegrityError)
  assert exc.value.detail == e.DatabaseIntegrityError.detail


# get_project

@pytest.mark.anyio
@pytest.mark.unit
async def test_get_project_success(
  mock_project_repo,
  unit_project_service,
  unit_project_obj
):
  mock_project_repo.get_by_id_and_owner.return_value = unit_project_obj

  result = await unit_project_service.get_project(
    unit_project_obj.id,
    unit_project_obj.user_id,
    unit_project_obj.client_id
  )

  assert result == unit_project_obj

@pytest.mark.anyio
@pytest.mark.unit
async def test_get_project_return_none_success(
  mock_project_repo,
  unit_project_service,
):
  mock_project_repo.get_by_id_and_owner.return_value = None

  with pytest.raises(e.ProjectNotFoundError) as exc:
    await unit_project_service.get_project(1311, 132, 33122)

  assert isinstance(exc.value, e.ProjectNotFoundError)
  assert exc.value.detail == e.ProjectNotFoundError.detail


# get_all_projects

@pytest.mark.anyio
@pytest.mark.unit
async def test_get_all_projects_success(
  mock_project_repo,
  unit_project_service,
  unit_project_obj
):
  mock_project_repo.get_all_by_owner.return_value = [unit_project_obj]

  result = await unit_project_service.get_all_projects(
    unit_project_obj.user_id,
    unit_project_obj.client_id
  )

  assert len(result) == 1
  assert result[0] == unit_project_obj

@pytest.mark.anyio
@pytest.mark.unit
async def test_get_all_projects_return_empty_list_success(
  mock_project_repo,
  unit_project_service
):
  mock_project_repo.get_all_by_owner.return_value = []

  result = await unit_project_service.get_all_projects(21, 34)

  assert len(result) == 0
  assert result == []