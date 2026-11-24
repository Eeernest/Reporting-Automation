import pytest
from sqlalchemy.exc import IntegrityError

import app.core.exceptions as e

# register_item

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_item_success(
  mock_item_repo,
  mock_item_session,
  unit_item_service,
  unit_item_obj,
):
  mock_item_repo.add_item.return_value = unit_item_obj
  mock_item_session.commit.return_value = None

  result = await unit_item_service.register_item(
    project_id=unit_item_obj.project_id,
    name=unit_item_obj.name,
    item_type=unit_item_obj.item_type,
    item_status=unit_item_obj.item_status,
    description=unit_item_obj.description
  )

  assert result == unit_item_obj

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_item_database_error(
  mock_item_repo,
  mock_item_session,
  unit_item_service,
  unit_item_obj,
):
  mock_item_repo.add_item.side_effect = IntegrityError(
    "stmt",
    "params",
    "unknown_error"
  )

  mock_item_session.rollback.return_value = None

  with pytest.raises(e.DatabaseIntegrityError) as exc:
    await unit_item_service.register_item(
      project_id=unit_item_obj.project_id,
      name=unit_item_obj.name,
      item_type=unit_item_obj.item_type,
      item_status=unit_item_obj.item_status,
      description=unit_item_obj.description
    )

  assert isinstance(exc.value, e.DatabaseIntegrityError)
  assert exc.value.detail == e.DatabaseIntegrityError.detail


# update_item

@pytest.mark.anyio
@pytest.mark.unit
async def test_update_item_success(mock_item_session, unit_item_service, unit_item_obj):
  mock_item_session.commit.return_value = None

  result = await unit_item_service.update_item(unit_item_obj, {"name": "updated_name"})

  assert result.name == "updated_name"

@pytest.mark.anyio
@pytest.mark.unit
async def test_update_item_no_field_provided_error(unit_item_service, unit_item_obj):
  with pytest.raises(e.NoFieldProvidedError) as exc:
    await unit_item_service.update_item(unit_item_obj, {})

  assert isinstance(exc.value, e.NoFieldProvidedError)
  assert exc.value.detail == e.NoFieldProvidedError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_update_item_database_integrity_error(
  mock_item_session,
  unit_item_service,
  unit_item_obj
):
  mock_item_session.commit.side_effect = IntegrityError(
    "stmt",
    "params",
    "db_error"
  )

  mock_item_session.rollback.return_value = None

  with pytest.raises(e.DatabaseIntegrityError) as exc:
    await unit_item_service.update_item(unit_item_obj, {"name": "new name"})

  assert isinstance(exc.value, e.DatabaseIntegrityError)
  assert exc.value.detail == e.DatabaseIntegrityError.detail


# delete_item

@pytest.mark.anyio
@pytest.mark.unit
async def test_delete_item_success(
  mock_item_repo,
  mock_item_session,
  unit_item_service,
  unit_item_obj
):
  mock_item_repo.delete_item.return_value = None
  mock_item_session.commit.return_value = None

  result = await unit_item_service.delete_item(unit_item_obj)

  assert result is None

@pytest.mark.anyio
@pytest.mark.unit
async def test_delete_item_database_integrity_error(
  mock_item_repo,
  mock_item_session,
  unit_item_service,
  unit_item_obj
):
  mock_item_repo.delete_item.return_value = None
  mock_item_session.commit.side_effect = IntegrityError(
    "stmt",
    "params",
    "db_error"
  )

  mock_item_session.rollback.return_value = None

  with pytest.raises(e.DatabaseIntegrityError) as exc:
    await unit_item_service.delete_item(unit_item_obj)

  assert isinstance(exc.value, e.DatabaseIntegrityError)
  assert exc.value.detail == e.DatabaseIntegrityError.detail


# get_item

@pytest.mark.anyio
@pytest.mark.unit
async def test_get_client_success(
  mock_item_repo,
  unit_item_service,
  unit_item_obj,
  unit_project_obj
):
  mock_item_repo.get_by_id_and_owner.return_value = unit_item_obj

  result = await unit_item_service.get_item(
    unit_item_obj.id,
    unit_project_obj.id,
    unit_project_obj.user_id
  )

  assert result == unit_item_obj

@pytest.mark.anyio
@pytest.mark.unit
async def test_get_client_not_found_error(mock_item_repo, unit_item_service):
  mock_item_repo.get_by_id_and_owner.return_value = None

  with pytest.raises(e.ItemNotFoundError) as exc:
    await unit_item_service.get_item(13213, 34, 123321)

  assert isinstance(exc.value, e.ItemNotFoundError)
  assert exc.value.detail == e.ItemNotFoundError.detail


# get_all_items

@pytest.mark.anyio
@pytest.mark.unit
async def test_get_all_items_success(mock_item_repo, unit_item_service, unit_item_obj):
  mock_item_repo.get_all_by_owner.return_value = [unit_item_obj]

  result = await unit_item_service.get_all_items(unit_item_obj.project_id, 3)

  assert len(result) == 1
  assert result[0] == unit_item_obj

@pytest.mark.anyio
@pytest.mark.unit
async def test_get_items_return_empty_list_success(mock_item_repo, unit_item_service):
  mock_item_repo.get_all_by_owner.return_value = []

  result = await unit_item_service.get_all_items(13, 21)

  assert len(result) == 0
  assert result == []