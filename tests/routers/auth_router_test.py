from fastapi import status
import pytest

import app.schemas.auth_schema as s

# login function

@pytest.mark.anyio
@pytest.mark.integration
async def test_login_success(
  integ_user_client,
  integ_auth_client,
  user_register_request
):
  await integ_user_client.post("/register", json=user_register_request.model_dump())

  result = await integ_auth_client.post("/login", data={
    "username": user_register_request.username,
    "password": user_register_request.password
  })

  assert result.status_code == status.HTTP_200_OK

@pytest.mark.anyio
@pytest.mark.integration
async def test_login_(integ_user_client, integ_auth_client, user_register_request):
  await integ_user_client.post("/register", json=user_register_request.model_dump())

  result = await integ_auth_client.post("/login", data={
    "username": user_register_request.username,
    "password": user_register_request.password
  })

  assert result.status_code == status.HTTP_200_OK


# logout function

@pytest.mark.anyio
@pytest.mark.integration
async def test_logout_success(
  integ_user_client,
  integ_auth_client,
  user_register_request
):
  await integ_user_client.post("/register", json=user_register_request.model_dump())
  
  login = await integ_auth_client.post("/login", data={
    "username": user_register_request.username,
    "password": user_register_request.password
  })

  login_data = login.json()

  refresh_token = login_data["refresh_token"]

  result = await integ_auth_client.post(
    "/logout",
    json=s.LogoutRequest(refresh_token=refresh_token).model_dump()
  )

  assert result.status_code == status.HTTP_204_NO_CONTENT


# refresh function

@pytest.mark.anyio
@pytest.mark.integration
async def test_refresh_success(
  integ_user_client,
  integ_auth_client,
  user_register_request
):
  await integ_user_client.post("/register", json=user_register_request.model_dump())
    
  login = await integ_auth_client.post("/login", data={
    "username": user_register_request.username,
    "password": user_register_request.password
  })

  login_data = login.json()

  refresh_token = login_data["refresh_token"]

  result = await integ_auth_client.post(
    "refresh",
    json=s.RefreshRequest(refresh_token=refresh_token).model_dump()
  )

  result_data = result.json()

  assert result.status_code == status.HTTP_200_OK
  assert result_data["token_type"] == "bearer"