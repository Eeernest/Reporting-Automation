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