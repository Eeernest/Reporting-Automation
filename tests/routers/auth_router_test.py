from fastapi import status
import pytest

import app.schemas.auth_schema as s

# login function

@pytest.mark.anyio
@pytest.mark.integration
async def test_login_success(
  integ_auth_client,
  registered_user_response
):
  user = registered_user_response.json()

  result = await integ_auth_client.post("/login", data={
    "username": user["username"],
    "password": "Password123"
  })

  assert result.status_code == status.HTTP_200_OK


# logout function

# @pytest.mark.anyio
# @pytest.mark.integration
# async def test_logout_success(
#   integ_auth_client,
#   loggedin_user
# ):
#   refresh_token = loggedin_user["refresh_token"]

#   result = await integ_auth_client.post(
#     "/logout",
#     json=s.LogoutRequest(refresh_token=refresh_token).model_dump()
#   )

#   assert result.status_code == status.HTTP_204_NO_CONTENT


# # refresh function

# @pytest.mark.anyio
# @pytest.mark.integration
# async def test_refresh_success(
#   integ_auth_client,
#   loggedin_user
# ):
#   refresh_token = loggedin_user["refresh_token"]

#   result = await integ_auth_client.post(
#     "refresh",
#     json=s.RefreshRequest(refresh_token=refresh_token).model_dump()
#   )

#   result_data = result.json()

#   assert result.status_code == status.HTTP_200_OK
#   assert result_data["token_type"] == "bearer"