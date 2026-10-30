from fastapi import status
import pytest

import app.core.exceptions as e

# get_current_user function

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_current_user_success(integ_permit_router, loggedin_user_response):
  access_token = loggedin_user_response["access_token"]

  result = await integ_permit_router.get(
    "/users/me",
    headers={"Authorization": f"Bearer {access_token}"}
  )

  data = result.json()

  assert result.status_code == status.HTTP_200_OK
  assert data["id"]
  assert data["username"]
  assert data["email"]

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_current_user_invalid_token_error(integ_permit_router):
  result = await integ_permit_router.get(
    "/users/me",
    headers={"Authorization": f"Bearer wrong token"}
  )

  data = result.json()

  assert result.status_code == status.HTTP_401_UNAUTHORIZED
  assert data["detail"] == e.InvalidTokenError.detail