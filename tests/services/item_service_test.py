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
  unit_project_obj
):
  mock_item_repo.add_item.return_value = unit_item_obj
  mock_item_session.commit.return_value = None

  result = await unit_item_service.register_item(
    user_id=unit_project_obj.user_id,
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
  unit_project_obj
):
  mock_item_repo.add_item.side_effect = IntegrityError(
    "stmt",
    "params",
    "unknown_error"
  )

  mock_item_session.rollback.return_value = None

  with pytest.raises(e.DatabaseIntegrityError) as exc:
    await unit_item_service.register_item(
      user_id=unit_project_obj.user_id,
      project_id=unit_item_obj.project_id,
      name=unit_item_obj.name,
      item_type=unit_item_obj.item_type,
      item_status=unit_item_obj.item_status,
      description=unit_item_obj.description
    )

  assert isinstance(exc.value, e.DatabaseIntegrityError)
  assert exc.value.detail == e.DatabaseIntegrityError.detail