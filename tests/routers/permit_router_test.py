from fastapi import status
import pytest

# get_current_user function

@pytest.mark.anyio
@pytest.mark.integration
async def test_get_current_user_success(integ_permit_client, loggedin_user):
  access_token = loggedin_user["access_token"]

  result = await integ_permit_client.get(
    "/users/me",
    headers={"Authorization": f"Bearer {access_token}"}
  )

  data = result.json()

  assert result.status_code == status.HTTP_200_OK
  assert data["id"]
  assert data["username"]
  assert data["email"]