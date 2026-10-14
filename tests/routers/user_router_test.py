# from fastapi import status
# import pytest

# import app.core.exceptions as e

# # register_user

# @pytest.mark.anyio
# @pytest.mark.unit
# async def test_register_user_success(
#   mock_user_service,
#   unit_user_client,
#   mock_user_obj
# ):
#   mock_user_service.create_account.return_value = mock_user_obj
  
#   result = await unit_user_client.post("/register", json={
#     "username": "user1",
#     "email": "user1@example.com",
#     "password": "Password123"
#   })

#   data = result.json()

#   assert result.status_code == status.HTTP_201_CREATED
#   assert data["id"] is not None