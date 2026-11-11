from fastapi import status
import pytest

import app.core.exceptions as e

@pytest.mark.anyio
@pytest.mark.integration
async def test_register_project_success(integ_project_router, registered_client_obj):
  request = {"name": "test project"}
  
  result = await integ_project_router.post(
    f"/clients/{registered_client_obj.id}/projects",
    json=request
  )

  data = result.json()

  assert result.status_code == status.HTTP_201_CREATED
  assert data["id"]
  assert data["user_id"]
  assert data["client_id"]
  assert data["name"]

@pytest.mark.anyio
@pytest.mark.integration
async def test_register_project_credentials_validation_error(
  integ_project_router,
  registered_client_obj
):
  request = {
    "name": "a" * 101,
    "location": "b" * 256,
    "description": "c" * 301
  }

  result = await integ_project_router.post(
    f"/clients/{registered_client_obj.id}/projects",
    json=request
  )

  data = result.json()

  assert result.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
  assert data["detail"][0]["field_name"] == "name"
  assert data["detail"][1]["field_name"] == "location"
  assert data["detail"][2]["field_name"] == "description"

# get_project

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_project_success(integ_project_router, registered_project_obj):
  result = await integ_project_router.get(f"/projects/{registered_project_obj.id}")

  data = result.json()

  assert result.status_code == status.HTTP_200_OK
  assert data["id"] == registered_project_obj.id
  assert data["user_id"] == registered_project_obj.user_id
  assert data["client_id"] == registered_project_obj.client_id
  assert data["name"] == registered_project_obj.name
  assert data["description"] == registered_project_obj.description
  assert data["est_end_date"] == registered_project_obj.est_end_date
  assert data["act_end_date"] == registered_project_obj.act_end_date

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_project_not_found_error(integ_project_router):
  result = await integ_project_router.get(f"/projects/{1}")

  data = result.json()

  assert result.status_code == status.HTTP_404_NOT_FOUND
  assert data["detail"] == e.ProjectNotFoundError.detail