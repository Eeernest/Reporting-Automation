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