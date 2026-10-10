import pytest

# register_client

@pytest.mark.anyio
@pytest.mark.unit
async def test_reister_client_all_arguments_success(
  mock_client_repo,
  unit_client_service,
  unit_client_obj
):
  mock_client_repo.save_client.return_value = unit_client_obj

  result = await unit_client_service.register_client(
    user_id=unit_client_obj.user_id,
    name=unit_client_obj.name,
    phone_number=unit_client_obj.phone_number,
    company=unit_client_obj.company,
    email=unit_client_obj.email,
    notes=unit_client_obj.notes
  )

  assert result == unit_client_obj
  assert result.company
  assert result.email
  assert result.notes

@pytest.mark.anyio
@pytest.mark.unit
async def test_reister_client_only_needed_arguments_success(
  mock_client_repo,
  unit_client_service,
  unit_client_obj
):
  unit_client_obj.company = None
  unit_client_obj.email = None
  unit_client_obj.notes = None

  mock_client_repo.save_client.return_value = unit_client_obj

  result = await unit_client_service.register_client(
    user_id=unit_client_obj.user_id,
    name=unit_client_obj.name,
    phone_number=unit_client_obj.phone_number,
  )

  assert result == unit_client_obj
  assert not result.company
  assert not result.email
  assert not result.notes
