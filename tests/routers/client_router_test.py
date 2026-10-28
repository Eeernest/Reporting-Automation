from fastapi import status
import pytest

import app.core.exceptions as e

# register_client

@pytest.mark.anyio
@pytest.mark.integration
async def test_register_client_success(integ_client_router):
  
  result = await integ_client_router.post(
    "/register_client",
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
    "/register_client",
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

  await integ_client_router.post("/register_client", json=request)

  bad_request = {
    "name": "test client",
    "phone_number": "+48456765412",
  }

  result = await integ_client_router.post("/register_client", json=bad_request)

  data = result.json()

  assert result.status_code == status.HTTP_409_CONFLICT
  assert data["detail"] == e.NameUnavailableError.detail