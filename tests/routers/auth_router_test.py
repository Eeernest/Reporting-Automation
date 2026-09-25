from fastapi import status
import pytest

import app.core.exceptions as e

# login

@pytest.mark.anyio
@pytest.mark.unit
async def test_login_success(mock_auth_service, unit_auth_client, token_response_obj):
  mock_auth_service.login.return_value = token_response_obj

  result = await unit_auth_client.post("/login", data={
    "username": "user1",
    "password": "Password123"
  })

  data = result.json()

  assert result.status_code == status.HTTP_200_OK
  assert data["access_token"] == token_response_obj.access_token
  assert data["refresh_token"] == token_response_obj.refresh_token
  assert data["token_type"] == token_response_obj.token_type

@pytest.mark.anyio
@pytest.mark.unit
async def test_login_invalid_credentials_error(mock_auth_service, unit_auth_client):
  mock_auth_service.login.side_effect = e.InvalidCredentialsError()

  result = await unit_auth_client.post("/login", data={
    "username": "user1",
    "password": "wrongpassword"
  })

  data = result.json()

  assert result.status_code == e.InvalidCredentialsError.status_code
  assert data["detail"] == e.InvalidCredentialsError.detail


# logout

@pytest.mark.anyio
@pytest.mark.unit
async def test_logout_success(mock_auth_service, unit_auth_client):
  mock_auth_service.logout.return_value = None

  result = await unit_auth_client.post("/logout", json={"refresh_token": "refresh_token"})

  assert result.status_code == status.HTTP_204_NO_CONTENT