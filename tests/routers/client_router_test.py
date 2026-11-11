from fastapi import status
import pytest

import app.core.exceptions as e

# register_client

@pytest.mark.anyio
@pytest.mark.integration
async def test_register_client_success(integ_client_router):
  
  result = await integ_client_router.post(
    "/clients",
    json={
      "name": "test client",
      "email": "testclient@example.com",
      "phone_number": "+48123456789",
      "notes": "test notes"
    }
  )

  data = result.json()

  assert result.status_code == status.HTTP_201_CREATED
  assert data["user_id"]
  assert data["name"]
  assert data["email"]
  assert data["phone_number"]

@pytest.mark.anyio
@pytest.mark.integration
async def test_register_client_credentials_validation_error(integ_client_router):
  result = await integ_client_router.post(
    "/clients",
    json={
      "name": "a" * 33,
      "phone_number": "123",
      "email": "wrong email",
      "notes": "a" * 301
    }
  )

  data = result.json()

  assert result.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
  assert data["detail"][0]["field_name"] == "name"
  assert data["detail"][1]["field_name"] == "phone_number"
  assert data["detail"][2]["field_name"] == "email"
  assert data["detail"][3]["field_name"] == "notes"

@pytest.mark.anyio
@pytest.mark.integration
async def test_register_client_name_unavailable_error(integ_client_router):
  request = {
    "name": "test client",
    "phone_number": "+48123456789",
  }

  await integ_client_router.post("/clients", json=request)

  bad_request = {
    "name": "test client",
    "phone_number": "+48456765412",
  }

  result = await integ_client_router.post("/clients", json=bad_request)

  data = result.json()

  assert result.status_code == status.HTTP_409_CONFLICT
  assert data["detail"] == e.NameUnavailableError.detail


# get_client

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_client_success(integ_client_router, registered_client_obj):
  result = await integ_client_router.get(f"/clients/{registered_client_obj.id}")

  data = result.json()

  assert result.status_code == status.HTTP_200_OK
  assert data["id"] == registered_client_obj.id
  assert data["user_id"] == registered_client_obj.user_id
  assert data["name"] == registered_client_obj.name
  assert data["email"] == registered_client_obj.email
  assert data["phone_number"] == registered_client_obj.phone_number
  assert data["notes"] == registered_client_obj.notes

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_client_not_found_error(integ_client_router):
  result = await integ_client_router.get(f"/clients/{1}")

  data = result.json()

  assert result.status_code == status.HTTP_404_NOT_FOUND
  assert data["detail"] == e.ClientNotFoundError.detail