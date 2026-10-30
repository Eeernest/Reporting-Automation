from fastapi import status
import pytest

import app.core.exceptions as e

# login function

@pytest.mark.anyio
@pytest.mark.integration
async def test_login_success(
  integ_auth_router,
  registered_user_response
):
  user = registered_user_response.json()

  request = {"username": user["username"], "password": "Password123"}

  result = await integ_auth_router.post("/login", data=request)

  assert result.status_code == status.HTTP_200_OK

# # logout function

# @pytest.mark.anyio
# @pytest.mark.integration
# async def test_logout_success(
#   integ_auth_router,
#   loggedin_user_response
# ):
#   request = {"refresh_token": loggedin_user_response["refresh_token"]}

#   result = await integ_auth_router.post("/logout", json=request)

#   assert result.status_code == status.HTTP_204_NO_CONTENT


# # # refresh function

# @pytest.mark.anyio
# @pytest.mark.integration
# async def test_refresh_success(
#   integ_auth_client,
#   loggedin_user_response
# ):
#   refresh_token = loggedin_user_response["refresh_token"]

#   result = await integ_auth_client.post(
#     "refresh",
#     json=s.RefreshRequest(refresh_token=refresh_token).model_dump()
#   )

#   result_data = result.json()

#   assert result.status_code == status.HTTP_200_OK
#   assert result_data["token_type"] == "bearer"