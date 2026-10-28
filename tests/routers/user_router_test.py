from fastapi import status
import pytest

import app.core.exceptions as e

# register_user

@pytest.mark.anyio
@pytest.mark.integration
async def test_register_user_success(integ_user_router):
  request = {
    "username": "user1",
    "email": "user1@example.com",
    "password": "Password123"
  }

  result = await integ_user_router.post("/register_user", json=request)

  data = result.json()

  assert result.status_code == status.HTTP_201_CREATED
  assert data["id"]

@pytest.mark.anyio
@pytest.mark.integration
async def test_register_user_credentials_validation_error(integ_user_router):
  request = {
    "username": "a" * 31,
    "email": "wrong email",
    "password": "Password123"
  }

  result = await integ_user_router.post("/register_user", json=request)

  data = result.json()

  assert result.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
  assert data["detail"][0]["field_name"] == "username"
  assert data["detail"][1]["field_name"] == "email"

@pytest.mark.anyio
@pytest.mark.integration
async def test_register_user_password_too_short_error(integ_user_router):
  request = {
    "username": "user1",
    "email": "user1@example.com",
    "password": "Short1"
  }

  result = await integ_user_router.post("/register_user", json=request)

  data = result.json()

  assert result.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
  assert data["detail"] == e.PasswordTooShortError.detail

@pytest.mark.anyio
@pytest.mark.integration
async def test_register_user_password_uppercase_error(integ_user_router):
  request = {
    "username": "user1",
    "email": "user1@example.com",
    "password": "nouppercase1"
  }

  result = await integ_user_router.post("/register_user", json=request)

  data = result.json()

  assert result.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
  assert data["detail"] == e.PasswordNoUppercaseError.detail

@pytest.mark.anyio
@pytest.mark.integration
async def test_register_user_password_number_error(integ_user_router):
  request = {
    "username": "user1",
    "email": "user1@example.com",
    "password": "Nonumbers"
  }

  result = await integ_user_router.post("/register_user", json=request)

  data = result.json()

  assert result.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
  assert data["detail"] == e.PasswordNumberError.detail

@pytest.mark.anyio
@pytest.mark.integration
async def test_register_user_username_unavailable_error(integ_user_router):
  request = {
    "username": "user1",
    "email": "user1@example.com",
    "password": "Password123"
  }

  await integ_user_router.post("/register_user", json=request)

  bad_request = {
    "username": "user1",
    "email": "user2@example.com",
    "password": "Password123"
  }

  result = await integ_user_router.post("/register_user", json=bad_request)

  data = result.json()

  assert result.status_code == status.HTTP_409_CONFLICT
  assert data["detail"] == e.UsernameUnavailableError.detail