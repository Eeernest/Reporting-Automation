from fastapi import status
import pytest

import app.core.exceptions as e

# register_user

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_user_success(mock_user_service, unit_user_client, unit_user_obj):
  mock_user_service.create_account.return_value = unit_user_obj
  
  result = await unit_user_client.post("/register_user", json={
    "username": "user1",
    "email": "user1@example.com",
    "password": "Password123"
  })

  data = result.json()

  assert result.status_code == status.HTTP_201_CREATED
  assert data["id"] is not None

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_user_password_too_short_error(unit_user_client):
  result = await unit_user_client.post("/register_user", json={
    "username": "user1",
    "email": "user1@example.com",
    "password": "Short1"
  })

  data = result.json()

  assert result.status_code == e.PasswordTooShortError.status_code
  assert data["detail"] == e.PasswordTooShortError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_user_password_no_number_error(unit_user_client):
  result = await unit_user_client.post("/register_user", json={
    "username": "user1",
    "email": "user1@example.com",
    "password": "Password"
  })

  data = result.json()

  assert result.status_code == e.PasswordNumberError.status_code
  assert data["detail"] == e.PasswordNumberError.detail

@pytest.mark.anyio
@pytest.mark.unit
async def test_register_user_password_no_uppercase_error(unit_user_client):
  result = await unit_user_client.post("/register_user", json={
    "username": "user1",
    "email": "user1@example.com",
    "password": "password123"
  })

  data = result.json()

  assert result.status_code == e.PasswordNoUppercaseError.status_code
  assert data["detail"] == e.PasswordNoUppercaseError.detail