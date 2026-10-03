from fastapi import status
import pytest

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
  user_register_request,
  auth_logout_request
):
  await integ_user_client.post("/register", json=user_register_request.model_dump())
  
  await integ_auth_client.post("/login", data={
    "username": user_register_request.username,
    "password": user_register_request.password
  })

  result = await integ_auth_client.post("/logout", json=auth_logout_request.model_dump())

  assert result.status_code == status.HTTP_204_NO_CONTENT